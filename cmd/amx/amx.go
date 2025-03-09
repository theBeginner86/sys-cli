package amx

import (
	"fmt"
	"os/exec"
	
	"github.com/spf13/cobra"

	"sys-cli/pkg"
)

var (
	AMX = "amx"
)

var AMXInfoCmd = &cobra.Command{
  Use:   AMX,
  Short: "Prints amx utlization",
  Long:  `Prints amx utlization`,
  RunE: func(cmd *cobra.Command, args []string) error {
    err := amxInfo()
		if err != nil {
			return err
		}
		return nil
  },
}


func amxInfo() error {
	// TODO: use cmd.SysProcAttr to add root user creds
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

