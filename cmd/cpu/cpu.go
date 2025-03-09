package cpu

import (
	"context"
	"fmt"
	"os"
	"os/exec"
	"os/signal"
	"syscall"
	"time"

	"github.com/spf13/cobra"

	"sys-cli/pkg"
)

var (
	CPU = "cpu"
	watch bool
	interval time.Duration
	CPUInfoCmd = &cobra.Command{
		Use:   CPU,
		Short: "Prints cpu utlization",
		Long:  `Prints cpu utlization`,
		RunE: func(cmd *cobra.Command, args []string) error {
			if watch {
				return watchCPU(cmd.Context())
			}
			err := cpuInfo()
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

	for {
		select {
		case <-ctx.Done():
			return ctx.Err()
		case <-sigChan:
			return nil
		case <-ticker.C:
			fmt.Print("\033[H\033[2J")
			fmt.Printf("Sys CLI: watch %.1fs\n", interval.Seconds())
			err := cpuInfo()
			if err != nil {
				return err
			}
		}
	}
}


func cpuInfo() error {
	cmd := exec.Command("/bin/bash", "-c", "mpstat -P ALL")
	out, err := cmd.Output()

	if err != nil {
		return err
	}

	fmt.Println(string(out))

	err = pkg.WriteOutput(out, CPU)
	if err != nil {
		return err
	}
	return nil
}

func init() {
	CPUInfoCmd.Flags().BoolVarP(&watch, "watch", "w", false, "After listing/getting the requested object, watch for changes")
	CPUInfoCmd.Flags().DurationVarP(&interval, "interval", "i", 2*time.Second, "Refresh interval (e.g, 500ms, 3s etc)")
}