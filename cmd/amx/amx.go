package amx

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
	AMX = "amx"
	watch bool
	interval time.Duration
	count int
	AMXInfoCmd = &cobra.Command{
		Use:   AMX,
		Short: "Prints amx utlization",
		Long:  `Prints amx utlization`,
		RunE: func(cmd *cobra.Command, args []string) error {
			if watch {
				return watchAMX(cmd.Context())
			}
			err := amxInfo()
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

	for {
		select {
		case <-ctx.Done():
			return ctx.Err()
		case <-sigChan:
			return nil
		case <-ticker.C:
			fmt.Print("\033[H\033[2J")
			fmt.Printf("Sys CLI: watch %.1fs\n", interval.Seconds())
			err := amxInfo()
			if err != nil {
				return err
			}
		}
	}
}

func amxInfo() error {
	// TODO: use cmd.SysProcAttr to add root user creds and skip sudo usage
	cmd := exec.Command("/bin/bash", "-c", "sudo processwatch -n 1")
	out, err := cmd.Output()
	if err != nil {
		return err
	}

	fmt.Println(string(out))

	err = pkg.WriteOutput(out, AMX)
	if err != nil {
		return err
	}
	return nil
}


func init() {
	AMXInfoCmd.Flags().BoolVarP(&watch, "watch", "w", false, "After listing/getting the requested object, watch for changes")
	AMXInfoCmd.Flags().DurationVarP(&interval, "interval", "i", 3*time.Second, "Refresh interval (e.g, 500ms, 3s etc)")
}

