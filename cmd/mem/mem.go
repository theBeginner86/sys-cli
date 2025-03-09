package mem

import (
	"os/exec"
	"fmt"
	// "context"

	"github.com/spf13/cobra"
	// "k8s.io/kubectl/pkg/util/interrupt"
	// watchtools "k8s.io/client-go/tools/watch"

	"sys-cli/pkg"
)

var (
	MEM = "mem"
	watch bool
 	MemInfoCmd = &cobra.Command{
		Use:   MEM,
		Short: "Prints memory utlization",
		Long:  `Prints memory utlization`,
		RunE: func(cmd *cobra.Command, args []string) error {
			if watch {

			}
			err := memInfo()
			if err != nil {
				return err
			}
			return nil
		},
	}
)

// func watchMem() error {
// 	ctx, cancel := context.WithCancel(context.Background())
// 	defer cancel()
// 	// intr := interrupt.New(nil, cancel)
// 	// intr.Run(func() error {
// 	// 	_, err := watchtools.UntilWithoutRetry(ctx, w, func(e watch.Event) (bool, error) {
			
// 	// 		return false, nil
// 	// 	})
// 	// 	return err
// 	// })
// 	var err error
// 	go func(err error) {
// 		for {
// 			err = memInfo()
// 			if err != nil {

// 			}
// 		}
// 	}(err)
// 	<- sig
// 	return nil
// }


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
}