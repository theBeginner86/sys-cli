package cpu

import (
	"fmt"
	"os/exec"

	"github.com/spf13/cobra"
)

var CPUInfoCmd = &cobra.Command{
  Use:   "cpu",
  Short: "Prints cpu utlization",
  Long:  `Prints cpu utlization`,
  Run: func(cmd *cobra.Command, args []string) {
    cpuInfo()
  },
}


func cpuInfo() {
	cmd := exec.Command("/bin/bash", "-c", "mpstat -P ALL")
	out, err := cmd.Output()

	if err != nil {
		panic(err)
	}

	fmt.Println(string(out))
}