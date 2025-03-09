package cmd

import (
	"os"
	"sys-cli/cmd/amx"
	"sys-cli/cmd/cpu"
	"sys-cli/cmd/mem"
	"sys-cli/pkg"

	"github.com/spf13/cobra"
)

// rootCmd represents the base command when called without any subcommands
var rootCmd = &cobra.Command{
	Use:   "sys-cli",
	Short: "Sys CLI for cpu,mem,amx utilization",
	Long: `Sys CLI for cpu,mem,amx utilization`,
}

// Execute adds all child commands to the root command and sets flags appropriately.
// This is called by main.main(). It only needs to happen once to the rootCmd.
func Execute() {
	err := rootCmd.Execute()
	if err != nil {
		os.Exit(1)
	}
}

func init() {
	cobra.OnInitialize(initConfig)

	// rootCmd.PersistentFlags().StringVar(&cfgFile, "config", "", "config file (default is $HOME/.sys-cli.yaml)")

	// Cobra also supports local flags, which will only run
	// when this action is called directly.
	// rootCmd.Flags().BoolP("toggle", "t", false, "Help message for toggle")
	rootCmd.AddCommand(VersionCmd)
	rootCmd.AddCommand(mem.MemInfoCmd)
	rootCmd.AddCommand(cpu.CPUInfoCmd)
	rootCmd.AddCommand(amx.AMXInfoCmd)
}

func initConfig() {
	pkg.SetOutputDirectory()
	pkg.CreateOutputDirIfNotExists()
}
