package mem

import (
	"context"
	"fmt"
	"os"
	"os/exec"
	"os/signal"
	"strings"
	"syscall"
	"time"

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
		PreRun: func(cmd *cobra.Command, args []string) {
			pkg.CreateOutputFile(MEM)
		},
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
	stats.Total, err = pkg.ParseSize(memFields[1])
	if err != nil {
		return MemStats{}, fmt.Errorf("failed to parse total: %v", err)
	}
	stats.Used, err = pkg.ParseSize(memFields[2])
	if err != nil {
		return MemStats{}, fmt.Errorf("failed to parse used: %v", err)
	}
	stats.Free, err = pkg.ParseSize(memFields[3])
	if err != nil {
		return MemStats{}, fmt.Errorf("failed to parse free: %v", err)
	}
	stats.Shared, err = pkg.ParseSize(memFields[4])
	if err != nil {
		return MemStats{}, fmt.Errorf("failed to parse shared: %v", err)
	}
	stats.BuffCache, err = pkg.ParseSize(memFields[5])
	if err != nil {
		return MemStats{}, fmt.Errorf("failed to parse buff/cache: %v", err)
	}
	stats.Available, err = pkg.ParseSize(memFields[6])
	if err != nil {
		return MemStats{}, fmt.Errorf("failed to parse available: %v", err)
	}

	stats.SwapTotal, err = pkg.ParseSize(swapFields[1])
	if err != nil {
		return MemStats{}, fmt.Errorf("failed to parse swap total: %v", err)
	}
	stats.SwapUsed, err = pkg.ParseSize(swapFields[2])
	if err != nil {
		return MemStats{}, fmt.Errorf("failed to parse swap used: %v", err)
	}
	stats.SwapFree, err = pkg.ParseSize(swapFields[3])
	if err != nil {
		return MemStats{}, fmt.Errorf("failed to parse swap free: %v", err)
	}

	return stats, nil
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

		max.Total = pkg.MaxFloat(max.Total, stats.Total)
		max.Used = pkg.MaxFloat(max.Used, stats.Used)
		max.Free = pkg.MaxFloat(max.Free, stats.Free)
		max.Shared = pkg.MaxFloat(max.Shared, stats.Shared)
		max.BuffCache = pkg.MaxFloat(max.BuffCache, stats.BuffCache)
		max.Available = pkg.MaxFloat(max.Available, stats.Available)
		max.SwapTotal = pkg.MaxFloat(max.SwapTotal, stats.SwapTotal)
		max.SwapUsed = pkg.MaxFloat(max.SwapUsed, stats.SwapUsed)
		max.SwapFree = pkg.MaxFloat(max.SwapFree, stats.SwapFree)
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


func init() {
	MemInfoCmd.Flags().BoolVarP(&watch, "watch", "w", false, "After listing/getting the requested object, watch for changes")
	MemInfoCmd.Flags().DurationVarP(&interval, "interval", "i", 2*time.Second, "Refresh interval (e.g, 500ms, 3s etc)")
}
