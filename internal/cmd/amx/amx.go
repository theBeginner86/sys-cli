package amx

import (
	"context"
	"fmt"
	"os"
	"os/exec"
	"os/signal"
	"strconv"
	"strings"
	"syscall"
	"time"

	"github.com/spf13/cobra"

	"sys-cli/pkg"
)

// ProcessStats holds utilization data for one process
type ProcessStats struct {
	AVX, AVX2, AVX512, AMXTile, PercentTotal, Total float64
}

// ProcessStatTracker holds cumulative stats for a process
type ProcessStatTracker struct {
	Stats    ProcessStats
	Count    int
	MaxStats ProcessStats
}

var (
	AMX        = "amx"
	watch      bool
	interval   time.Duration
	count      int
	AMXInfoCmd = &cobra.Command{
		Use:   AMX,
		Short: "Prints amx utlization",
		Long:  `Prints amx utlization`,
		PreRun: func(cmd *cobra.Command, args []string) {
			pkg.CreateOutputFile(AMX)
		},
		RunE: func(cmd *cobra.Command, args []string) error {
			if watch {
				return watchAMX(cmd.Context())
			}
			out, err := amxInfo()
			if err != nil {
				return err
			}
			err = pkg.WriteBytesToFile(out, AMX)
			if err != nil {
				return err
			}
			return nil
		},
	}
)

func watchAMX(ctx context.Context) error {
	ticker := time.NewTicker(interval)
	defer ticker.Stop()

	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM)

	// Track stats per process (PID + NAME) over time
	processStats := make(map[string]ProcessStatTracker) // Keyed by "PID:NAME"

	for {
		select {
		case <-ctx.Done():
			return ctx.Err()
		case <-sigChan:
			printStats(processStats)
			return nil
		case <-ticker.C:
			fmt.Print("\033[H\033[2J")
			fmt.Printf("Sys CLI: watch %.1fs\n", interval.Seconds())
			out, err := amxInfo()
			if err != nil {
				return err
			}
			// Parse and store per-process stats
			perProcessStats, err := parseProcessWatchOutput(out)
			if err != nil {
				return err
			}
			updateProcessStats(processStats, perProcessStats)
		}
	}
}

func amxInfo() ([]byte, error) {
	// TODO: use cmd.SysProcAttr to add root user creds and skip sudo usage
	cmd := exec.Command("/bin/bash", "-c", "sudo processwatch -n 1")
	out, err := cmd.Output()
	if err != nil {
		return nil, err
	}

	fmt.Print(string(out))
	return out, nil
}

func parseProcessWatchOutput(out []byte) (map[string]ProcessStats, error) {
	lines := strings.Split(string(out), "\n")
	
	if len(lines) < 2 { // Need header + at least 1 data line
		return nil, fmt.Errorf("invalid processwatch output: too few lines")
	}

	// Skip header (first line)
	dataLines := lines[1:]
	if !strings.Contains(dataLines[0], "PID") || !strings.Contains(dataLines[0], "NAME") {
		return nil, fmt.Errorf("invalid processwatch output: missing header")
	}

	// Parse each process line
	processStats := make(map[string]ProcessStats)
	for  i := 1; i < len(dataLines); i++ {
		fields := strings.Fields(dataLines[i])
		if len(fields) < 8 { // Expecting PID, NAME, and 6 metrics
			continue // Skip malformed or empty lines
		}
		pid := fields[0]
		name := fields[1]
		key := pid + ":" + name // Unique key for PID:NAME

		stats := ProcessStats{}
		var err error
		stats.AVX, err = strconv.ParseFloat(fields[2], 64)
		if err != nil {
			return nil, fmt.Errorf("failed to parse AVX for %s: %v", key, err)
		}
		stats.AVX2, err = strconv.ParseFloat(fields[3], 64)
		if err != nil {
			return nil, fmt.Errorf("failed to parse AVX2 for %s: %v", key, err)
		}
		stats.AVX512, err = strconv.ParseFloat(fields[4], 64)
		if err != nil {
			return nil, fmt.Errorf("failed to parse AVX512 for %s: %v", key, err)
		}
		stats.AMXTile, err = strconv.ParseFloat(fields[5], 64)
		if err != nil {
			return nil, fmt.Errorf("failed to parse AMX_TILE for %s: %v", key, err)
		}
		stats.PercentTotal, err = strconv.ParseFloat(fields[6], 64)
		if err != nil {
			return nil, fmt.Errorf("failed to parse %%TOTAL for %s: %v", key, err)
		}
		stats.Total, err = strconv.ParseFloat(fields[7], 64)
		if err != nil {
			return nil, fmt.Errorf("failed to parse TOTAL for %s: %v", key, err)
		}

		processStats[key] = stats
	}

	if len(processStats) == 0 {
		return nil, fmt.Errorf("no valid process data found")
	}
	return processStats, nil
}

func updateProcessStats(processStats map[string]ProcessStatTracker, perProcessStats map[string]ProcessStats) {
	for key, stats := range perProcessStats {
		tracker, exists := processStats[key]
		if !exists {
			tracker = ProcessStatTracker{}
		}

		// Update cumulative stats
		tracker.Stats.AVX += stats.AVX
		tracker.Stats.AVX2 += stats.AVX2
		tracker.Stats.AVX512 += stats.AVX512
		tracker.Stats.AMXTile += stats.AMXTile
		tracker.Stats.PercentTotal += stats.PercentTotal
		tracker.Stats.Total += stats.Total
		tracker.Count++

		// Update maximums
		tracker.MaxStats.AVX = pkg.MaxFloat(tracker.MaxStats.AVX, stats.AVX)
		tracker.MaxStats.AVX2 = pkg.MaxFloat(tracker.MaxStats.AVX2, stats.AVX2)
		tracker.MaxStats.AVX512 = pkg.MaxFloat(tracker.MaxStats.AVX512, stats.AVX512)
		tracker.MaxStats.AMXTile = pkg.MaxFloat(tracker.MaxStats.AMXTile, stats.AMXTile)
		tracker.MaxStats.PercentTotal = pkg.MaxFloat(tracker.MaxStats.PercentTotal, stats.PercentTotal)
		tracker.MaxStats.Total = pkg.MaxFloat(tracker.MaxStats.Total, stats.Total)

		processStats[key] = tracker
	}
}

func printStats(processStats map[string]ProcessStatTracker) {
	if len(processStats) == 0 {
		pkg.WriteStringToFile(fmt.Sprintf("No stats collected \n"), AMX)
		return
	}

	pkg.WriteStringToFile(fmt.Sprintf("\nPer-Process Utilization Statistics:"), AMX)
	for key, tracker := range processStats {
		avg := ProcessStats{
			AVX:          tracker.Stats.AVX / float64(tracker.Count),
			AVX2:         tracker.Stats.AVX2 / float64(tracker.Count),
			AVX512:       tracker.Stats.AVX512 / float64(tracker.Count),
			AMXTile:      tracker.Stats.AMXTile / float64(tracker.Count),
			PercentTotal: tracker.Stats.PercentTotal / float64(tracker.Count),
			Total:        tracker.Stats.Total / float64(tracker.Count),
		}

		pkg.WriteStringToFile(fmt.Sprintf("%s (%d samples):\n", key, tracker.Count), AMX)
		pkg.WriteStringToFile(fmt.Sprintf("  Avg: AVX: %.2f, AVX2: %.2f, AVX512: %.2f, AMX_TILE: %.2f, %%TOTAL: %.2f, TOTAL: %.2f\n",
			avg.AVX, avg.AVX2, avg.AVX512, avg.AMXTile, avg.PercentTotal, avg.Total), AMX)
		pkg.WriteStringToFile(fmt.Sprintf("  Max: AVX: %.2f, AVX2: %.2f, AVX512: %.2f, AMX_TILE: %.2f, %%TOTAL: %.2f, TOTAL: %.2f\n",
			tracker.MaxStats.AVX, tracker.MaxStats.AVX2, tracker.MaxStats.AVX512, tracker.MaxStats.AMXTile,
			tracker.MaxStats.PercentTotal, tracker.MaxStats.Total), AMX)
	}
}

func init() {
	AMXInfoCmd.Flags().BoolVarP(&watch, "watch", "w", false, "After listing/getting the requested object, watch for changes")
	AMXInfoCmd.Flags().DurationVarP(&interval, "interval", "i", 3*time.Second, "Refresh interval (e.g, 500ms, 3s etc)")

}
