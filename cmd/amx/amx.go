package amx

import (
	"fmt"
	"os/exec"

	"github.com/spf13/cobra"
)

var AMXInfoCmd = &cobra.Command{
  Use:   "amx",
  Short: "Prints amx utlization",
  Long:  `Prints amx utlization`,
  Run: func(cmd *cobra.Command, args []string) {
    amxInfo()
  },
}


func amxInfo() {
	// TODO: use cmd.SysProcAttr to add root user creds
	cmd := exec.Command("/bin/bash", "-c", "sudo processwatch -n 1")
	out, err := cmd.Output()

	if err != nil {
		panic(err)
	}

	fmt.Println(string(out))
}

