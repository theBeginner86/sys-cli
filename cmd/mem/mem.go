package mem

import (
	"os/exec"
	"fmt"

	"github.com/spf13/cobra"

	"sys-cli/pkg"
)

var (
	MEM = "mem"
)

var MemInfoCmd = &cobra.Command{
  Use:   MEM,
  Short: "Prints memory utlization",
  Long:  `Prints memory utlization`,
  RunE: func(cmd *cobra.Command, args []string) error {
    err := memInfo()
		if err != nil {
			return err
		}
		return nil
  },
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