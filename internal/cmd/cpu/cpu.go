package cpu

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

	"systat/pkg"
)

type CPUStats struct {
	Usr, Nice, Sys, Iowait, Irq, Soft, Steal, Guest, Gnice, Idle float64
}

type CPUStatTracker struct {
	Stats    CPUStats
	Count    int
	MaxStats CPUStats
}

var (
	CPU        = "cpu"
	watch      bool
	cpuList    string
	interval   time.Duration
	CPUInfoCmd = &cobra.Command{
		Use:   CPU,
		Short: "Prints cpu utlization",
		Long:  `Prints cpu utlization`,
		PreRun: func(cmd *cobra.Command, args []string) {
			pkg.CreateOutputFile(CPU)
		},
		RunE: func(cmd *cobra.Command, args []string) error {
			if watch {
				return watchCPU(cmd.Context())
			}
			out, err := cpuInfo()
			if err != nil {
				return err
			}
			err = pkg.WriteBytesToFile(out, CPU)
			if err != nil {
				return err
			}
			return nil
		},
	}
)

func watchCPU(ctx context.Context) error {
	ticker := time.NewTicker(interval)
	defer ticker.Stop()

	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM)
	cpuStats := make(map[string]CPUStatTracker) // Keyed by CPU ID (e.g., "1", "2")

	for {
		select {
		case <-ctx.Done():
			return ctx.Err()
		case <-sigChan:
			printStats(cpuStats)
			return nil
		case <-ticker.C:
			fmt.Print("\033[H\033[2J")
			fmt.Printf("Sys CLI: watch %.1fs\n", interval.Seconds())

			out, err := cpuInfo()
			if err != nil {
				return err
			}

			// Parse and store per-CPU stats
			perCPUStats, err := parseCPUOutput(out)
			if err != nil {
				return err
			}
			updateCPUStats(cpuStats, perCPUStats)
		}
	}
}

func cpuInfo() ([]byte, error) {
	mpstat := "mpstat"
	if cpuList != "" {
		mpstat += fmt.Sprintf(" -P %s", cpuList)
	}
	cmd := exec.Command("/bin/bash", "-c", mpstat)
	out, err := cmd.Output()
	if err != nil {
		return nil, err
	}

	fmt.Println(string(out))

	return out, nil
}

func parseCPUOutput(out []byte) (map[string]CPUStats, error) {
	lines := strings.Split(string(out), "\n")
	if len(lines) < 4 { // Need at least 2 system lines + header + 1 data line
		return nil, fmt.Errorf("invalid CPU output: too few lines")
	}

	// Skip first two lines (system info), start from third line (header)
	dataLines := lines[2:] // Header is dataLines[0], data starts at dataLines[1]
	if len(dataLines) < 2 || !strings.Contains(dataLines[0], "%usr") {
		return nil, fmt.Errorf("invalid CPU output: missing header")
	}

	// Parse each CPU line
	cpuStats := make(map[string]CPUStats)
	for i := 1; i < len(dataLines); i++ {
		fields := strings.Fields(dataLines[i])
		if len(fields) < 12 { // Expecting timestamp, CPU, and 10 metrics
			continue // Skip malformed lines
		}

		cpuID := fields[1] // e.g., "1", "2"
		stats := CPUStats{}
		var err error
		stats.Usr, err = strconv.ParseFloat(fields[2], 64)
		if err != nil {
			return nil, fmt.Errorf("failed to parse %%usr for CPU %s: %v", cpuID, err)
		}
		stats.Nice, err = strconv.ParseFloat(fields[3], 64)
		if err != nil {
			return nil, fmt.Errorf("failed to parse %%nice for CPU %s: %v", cpuID, err)
		}
		stats.Sys, err = strconv.ParseFloat(fields[4], 64)
		if err != nil {
			return nil, fmt.Errorf("failed to parse %%sys for CPU %s: %v", cpuID, err)
		}
		stats.Iowait, err = strconv.ParseFloat(fields[5], 64)
		if err != nil {
			return nil, fmt.Errorf("failed to parse %%iowait for CPU %s: %v", cpuID, err)
		}
		stats.Irq, err = strconv.ParseFloat(fields[6], 64)
		if err != nil {
			return nil, fmt.Errorf("failed to parse %%irq for CPU %s: %v", cpuID, err)
		}
		stats.Soft, err = strconv.ParseFloat(fields[7], 64)
		if err != nil {
			return nil, fmt.Errorf("failed to parse %%soft for CPU %s: %v", cpuID, err)
		}
		stats.Steal, err = strconv.ParseFloat(fields[8], 64)
		if err != nil {
			return nil, fmt.Errorf("failed to parse %%steal for CPU %s: %v", cpuID, err)
		}
		stats.Guest, err = strconv.ParseFloat(fields[9], 64)
		if err != nil {
			return nil, fmt.Errorf("failed to parse %%guest for CPU %s: %v", cpuID, err)
		}
		stats.Gnice, err = strconv.ParseFloat(fields[10], 64)
		if err != nil {
			return nil, fmt.Errorf("failed to parse %%gnice for CPU %s: %v", cpuID, err)
		}
		stats.Idle, err = strconv.ParseFloat(fields[11], 64)
		if err != nil {
			return nil, fmt.Errorf("failed to parse %%idle for CPU %s: %v", cpuID, err)
		}

		cpuStats[cpuID] = stats
	}

	if len(cpuStats) == 0 {
		return nil, fmt.Errorf("no valid CPU data found")
	}
	return cpuStats, nil
}

func updateCPUStats(cpuStats map[string]CPUStatTracker, perCPUStats map[string]CPUStats) {
	for cpuID, stats := range perCPUStats {
		tracker, exists := cpuStats[cpuID]
		if !exists {
			tracker = CPUStatTracker{}
		}

		// Update cumulative stats
		tracker.Stats.Usr += stats.Usr
		tracker.Stats.Nice += stats.Nice
		tracker.Stats.Sys += stats.Sys
		tracker.Stats.Iowait += stats.Iowait
		tracker.Stats.Irq += stats.Irq
		tracker.Stats.Soft += stats.Soft
		tracker.Stats.Steal += stats.Steal
		tracker.Stats.Guest += stats.Guest
		tracker.Stats.Gnice += stats.Gnice
		tracker.Stats.Idle += stats.Idle
		tracker.Count++

		// Update maximums
		tracker.MaxStats.Usr = pkg.MaxFloat(tracker.MaxStats.Usr, stats.Usr)
		tracker.MaxStats.Nice = pkg.MaxFloat(tracker.MaxStats.Nice, stats.Nice)
		tracker.MaxStats.Sys = pkg.MaxFloat(tracker.MaxStats.Sys, stats.Sys)
		tracker.MaxStats.Iowait = pkg.MaxFloat(tracker.MaxStats.Iowait, stats.Iowait)
		tracker.MaxStats.Irq = pkg.MaxFloat(tracker.MaxStats.Irq, stats.Irq)
		tracker.MaxStats.Soft = pkg.MaxFloat(tracker.MaxStats.Soft, stats.Soft)
		tracker.MaxStats.Steal = pkg.MaxFloat(tracker.MaxStats.Steal, stats.Steal)
		tracker.MaxStats.Guest = pkg.MaxFloat(tracker.MaxStats.Guest, stats.Guest)
		tracker.MaxStats.Gnice = pkg.MaxFloat(tracker.MaxStats.Gnice, stats.Gnice)
		tracker.MaxStats.Idle = pkg.MaxFloat(tracker.MaxStats.Idle, stats.Idle)

		cpuStats[cpuID] = tracker
	}
}

func printStats(cpuStats map[string]CPUStatTracker) {
	if len(cpuStats) == 0 {
		pkg.WriteStringToFile("No stats collected", CPU)
		return
	}

	pkg.WriteStringToFile("\nPer-CPU Utilization Statistics:\n", CPU)
	for cpuID, tracker := range cpuStats {
		avg := CPUStats{
			Usr:    tracker.Stats.Usr / float64(tracker.Count),
			Nice:   tracker.Stats.Nice / float64(tracker.Count),
			Sys:    tracker.Stats.Sys / float64(tracker.Count),
			Iowait: tracker.Stats.Iowait / float64(tracker.Count),
			Irq:    tracker.Stats.Irq / float64(tracker.Count),
			Soft:   tracker.Stats.Soft / float64(tracker.Count),
			Steal:  tracker.Stats.Steal / float64(tracker.Count),
			Guest:  tracker.Stats.Guest / float64(tracker.Count),
			Gnice:  tracker.Stats.Gnice / float64(tracker.Count),
			Idle:   tracker.Stats.Idle / float64(tracker.Count),
		}

		pkg.WriteStringToFile(fmt.Sprintf("CPU %s (%d samples):\n", cpuID, tracker.Count), CPU)
		pkg.WriteStringToFile(fmt.Sprintf("  Avg: %%usr: %.2f, %%nice: %.2f, %%sys: %.2f, %%iowait: %.2f, %%irq: %.2f, %%soft: %.2f, %%steal: %.2f, %%guest: %.2f, %%gnice: %.2f, %%idle: %.2f\n",
			avg.Usr, avg.Nice, avg.Sys, avg.Iowait, avg.Irq, avg.Soft, avg.Steal, avg.Guest, avg.Gnice, avg.Idle), CPU)
		pkg.WriteStringToFile(fmt.Sprintf("  Max: %%usr: %.2f, %%nice: %.2f, %%sys: %.2f, %%iowait: %.2f, %%irq: %.2f, %%soft: %.2f, %%steal: %.2f, %%guest: %.2f, %%gnice: %.2f, %%idle: %.2f\n",
			tracker.MaxStats.Usr, tracker.MaxStats.Nice, tracker.MaxStats.Sys, tracker.MaxStats.Iowait, tracker.MaxStats.Irq,
			tracker.MaxStats.Soft, tracker.MaxStats.Steal, tracker.MaxStats.Guest, tracker.MaxStats.Gnice, tracker.MaxStats.Idle), CPU)
	}
}

func init() {
	CPUInfoCmd.Flags().BoolVarP(&watch, "watch", "w", false, "After listing/getting the requested object, watch for changes")
	CPUInfoCmd.Flags().DurationVarP(&interval, "interval", "i", 2*time.Second, "Refresh interval (e.g, 500ms, 3s etc)")
	CPUInfoCmd.Flags().StringVarP(&cpuList, "cpu", "c", "", "CPU list to track (e.g, '1', '1,2,3', '3-9', 'ALL')")	
}
