package mem

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
	MEM = "mem"
	watch bool
	interval time.Duration
 	MemInfoCmd = &cobra.Command{
		Use:   MEM,
		Short: "Prints memory utlization",
		Long:  `Prints memory utlization`,
		RunE: func(cmd *cobra.Command, args []string) error {
			if watch {
				return watchMem(cmd.Context())
			}
			err := memInfo()
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

	for {
		select {
		case <- ctx.Done():
			return ctx.Err()
		case <-sigChan:
			// fmt.Println("\nWatch stopped by signal")
			return nil
		case <-ticker.C:
			fmt.Print("\033[H\033[2J")
			fmt.Printf("Sys CLI: watch %.1fs\n", interval.Seconds())
			err := memInfo()
			if err != nil {
				return err
			}
		}
	}	
}


func memInfo() error {
	cmd := exec.Command("/bin/bash", "-c", "free -h")
	out, err := cmd.Output()

	if err != nil {
		return err
	}

	fmt.Println(string(out))

	err = pkg.WriteOutput(out, MEM)
	if err != nil {
		return err
	}
	return nil
}

func init() {
	MemInfoCmd.Flags().BoolVarP(&watch, "watch", "w", false, "After listing/getting the requested object, watch for changes")	
	MemInfoCmd.Flags().DurationVarP(&interval, "interval", "i", 2*time.Second, "Refresh interval (e.g, 500ms, 3s etc)")
}