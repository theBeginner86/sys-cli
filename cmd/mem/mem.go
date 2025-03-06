package mem

import (
	"fmt"
	"os/exec"

	"github.com/spf13/cobra"
)

var MemInfoCmd = &cobra.Command{
  Use:   "mem",
  Short: "Prints memory utlization",
  Long:  `Prints memory utlization`,
  Run: func(cmd *cobra.Command, args []string) {
    memInfo()
  },
}


func memInfo() {
	cmd := exec.Command("/bin/bash", "-c", "free -h")
	out, err := cmd.Output()

	if err != nil {
		panic(err)
	}

	fmt.Println(string(out))
}