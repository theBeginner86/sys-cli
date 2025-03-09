package cpu

import (
	"fmt"
	"os/exec"
	
	"github.com/spf13/cobra"

	"sys-cli/pkg"
)

var (
	CPU = "cpu"
)

var CPUInfoCmd = &cobra.Command{
  Use:   CPU,
  Short: "Prints cpu utlization",
  Long:  `Prints cpu utlization`,
  RunE: func(cmd *cobra.Command, args []string) error {
    err := cpuInfo()
		if err != nil {
			return err
		}
		return nil
  },
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