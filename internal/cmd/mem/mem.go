package mem

import (
	"context"
	"fmt"
	"os"
	"os/exec"
	"os/signal"
	"syscall"
	"time"
	"strings"
	"strconv"

	"github.com/spf13/cobra"

	"sys-cli/pkg"
)

// MemStats holds memory utilization data
type MemStats struct {
    Total, Used, Free, Shared, BuffCache, Available float64 // In GiB
    SwapTotal, SwapUsed, SwapFree                   float64 // In GiB
}

var (
	MEM        = "mem"
	watch      bool
	interval   time.Duration
	MemInfoCmd = &cobra.Command{
		Use:   MEM,
		Short: "Prints memory utlization",
		Long:  `Prints memory utlization`,
		RunE: func(cmd *cobra.Command, args []string) error {
			if watch {
				return watchMem(cmd.Context())
			}
			out, err := memInfo()
			if err != nil {
				return err
			}
			err = pkg.WriteBytesToFile(out, MEM)
			if err != nil {
				return err
			}
			return nil
		},
	}
)

func watchMem(ctx context.Context) error {
	ticker := time.NewTicker(interval)
	defer ticker.Stop()

	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM)

	var statsList []MemStats

	for {
		select {
		case <-ctx.Done():
			return ctx.Err()
		case <-sigChan:
			printStats(statsList)
			return nil
		case <-ticker.C:
			fmt.Print("\033[H\033[2J")
			fmt.Printf("Sys CLI: watch %.1fs\n", interval.Seconds())
			out, err := memInfo()
			if err != nil {
				return err
			}
			 // Parse and store stats
            stats, err := parseMemOutput(out)
            if err != nil {
                return err
            }
            statsList = append(statsList, stats)
		}
	}
}

func memInfo() ([]byte, error) {
	cmd := exec.Command("/bin/bash", "-c", "free -h")
	out, err := cmd.Output()

	if err != nil {
		return nil, err
	}

	fmt.Println(string(out))
	return out, nil
}


func parseMemOutput(out []byte) (MemStats, error) {
    lines := strings.Split(string(out), "\n")
    if len(lines) < 3 { // Need header, Mem, and Swap lines
        return MemStats{}, fmt.Errorf("invalid memory output: too few lines")
    }

    // Parse Mem line (second line)
    memFields := strings.Fields(lines[1])
    if len(memFields) < 7 || memFields[0] != "Mem:" {
        return MemStats{}, fmt.Errorf("invalid Mem line format")
    }

    // Parse Swap line (third line)
    swapFields := strings.Fields(lines[2])
    if len(swapFields) < 4 || swapFields[0] != "Swap:" {
        return MemStats{}, fmt.Errorf("invalid Swap line format")
    }

    stats := MemStats{}
    var err error
    stats.Total, err = parseSize(memFields[1])
    if err != nil {
        return MemStats{}, fmt.Errorf("failed to parse total: %v", err)
    }
    stats.Used, err = parseSize(memFields[2])
    if err != nil {
        return MemStats{}, fmt.Errorf("failed to parse used: %v", err)
    }
    stats.Free, err = parseSize(memFields[3])
    if err != nil {
        return MemStats{}, fmt.Errorf("failed to parse free: %v", err)
    }
    stats.Shared, err = parseSize(memFields[4])
    if err != nil {
        return MemStats{}, fmt.Errorf("failed to parse shared: %v", err)
    }
    stats.BuffCache, err = parseSize(memFields[5])
    if err != nil {
        return MemStats{}, fmt.Errorf("failed to parse buff/cache: %v", err)
    }
    stats.Available, err = parseSize(memFields[6])
    if err != nil {
        return MemStats{}, fmt.Errorf("failed to parse available: %v", err)
    }

    stats.SwapTotal, err = parseSize(swapFields[1])
    if err != nil {
        return MemStats{}, fmt.Errorf("failed to parse swap total: %v", err)
    }
    stats.SwapUsed, err = parseSize(swapFields[2])
    if err != nil {
        return MemStats{}, fmt.Errorf("failed to parse swap used: %v", err)
    }
    stats.SwapFree, err = parseSize(swapFields[3])
    if err != nil {
        return MemStats{}, fmt.Errorf("failed to parse swap free: %v", err)
    }

    return stats, nil
}

// parseSize converts human-readable sizes (e.g., "7.6Gi", "903Mi", "0B") to GiB
func parseSize(sizeStr string) (float64, error) {
    if sizeStr == "" {
        return 0, fmt.Errorf("empty size string")
    }

    // Extract number and unit
    numStr := ""
    unit := ""
    for _, r := range sizeStr {
        if r >= '0' && r <= '9' || r == '.' {
            numStr += string(r)
        } else {
            unit += string(r)
        }
    }

    num, err := strconv.ParseFloat(numStr, 64)
    if err != nil {
        return 0, fmt.Errorf("invalid number in size: %v", err)
    }

    // Convert to GiB based on unit
    switch strings.ToLower(unit) {
    case "gi", "gib":
        return num, nil
    case "mi", "mib":
        return num / 1024, nil // MiB to GiB
    case "ki", "kib":
        return num / (1024 * 1024), nil // KiB to GiB
    case "b":
        return num / (1024 * 1024 * 1024), nil // Bytes to GiB
    case "":
        return num, nil // Assume GiB if no unit (unlikely)
    default:
        return 0, fmt.Errorf("unknown unit: %s", unit)
    }
}

func printStats(statsList []MemStats) {
    if len(statsList) == 0 {
        pkg.WriteStringToFile("No stats collected", MEM)
        return
    }

    // Calculate averages and maximums
    var avg, max MemStats
    for _, stats := range statsList {
        avg.Total += stats.Total
        avg.Used += stats.Used
        avg.Free += stats.Free
        avg.Shared += stats.Shared
        avg.BuffCache += stats.BuffCache
        avg.Available += stats.Available
        avg.SwapTotal += stats.SwapTotal
        avg.SwapUsed += stats.SwapUsed
        avg.SwapFree += stats.SwapFree

        max.Total = maxFloat(max.Total, stats.Total)
        max.Used = maxFloat(max.Used, stats.Used)
        max.Free = maxFloat(max.Free, stats.Free)
        max.Shared = maxFloat(max.Shared, stats.Shared)
        max.BuffCache = maxFloat(max.BuffCache, stats.BuffCache)
        max.Available = maxFloat(max.Available, stats.Available)
        max.SwapTotal = maxFloat(max.SwapTotal, stats.SwapTotal)
        max.SwapUsed = maxFloat(max.SwapUsed, stats.SwapUsed)
        max.SwapFree = maxFloat(max.SwapFree, stats.SwapFree)
    }

    n := float64(len(statsList))
    avg.Total /= n
    avg.Used /= n
    avg.Free /= n
    avg.Shared /= n
    avg.BuffCache /= n
    avg.Available /= n
    avg.SwapTotal /= n
    avg.SwapUsed /= n
    avg.SwapFree /= n

    // Print results
    pkg.WriteStringToFile(fmt.Sprintln("\nMemory Utilization Statistics (in GiB):"), MEM)
    pkg.WriteStringToFile(fmt.Sprintf("  Avg: total: %.2f, used: %.2f, free: %.2f, shared: %.2f, buff/cache: %.2f, available: %.2f\n",
        avg.Total, avg.Used, avg.Free, avg.Shared, avg.BuffCache, avg.Available), MEM)
    pkg.WriteStringToFile(fmt.Sprintf("       swap total: %.2f, swap used: %.2f, swap free: %.2f\n",
        avg.SwapTotal, avg.SwapUsed, avg.SwapFree), MEM)
    pkg.WriteStringToFile(fmt.Sprintf("  Max: total: %.2f, used: %.2f, free: %.2f, shared: %.2f, buff/cache: %.2f, available: %.2f\n",
        max.Total, max.Used, max.Free, max.Shared, max.BuffCache, max.Available), MEM)
    pkg.WriteStringToFile(fmt.Sprintf("       swap total: %.2f, swap used: %.2f, swap free: %.2f\n",
        max.SwapTotal, max.SwapUsed, max.SwapFree), MEM)
}

func maxFloat(a, b float64) float64 {
    if a > b {
        return a
    }
    return b
}

func init() {
	MemInfoCmd.Flags().BoolVarP(&watch, "watch", "w", false, "After listing/getting the requested object, watch for changes")
	MemInfoCmd.Flags().DurationVarP(&interval, "interval", "i", 2*time.Second, "Refresh interval (e.g, 500ms, 3s etc)")
}
