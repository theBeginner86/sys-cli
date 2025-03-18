package cmd

import (
	"os"
	"systat/internal/cmd/amx"
	"systat/internal/cmd/cpu"
	"systat/internal/cmd/mem"
	"systat/pkg"

	"github.com/spf13/cobra"
)

// rootCmd represents the base command when called without any subcommands
var rootCmd = &cobra.Command{
	Use:   "systat",
	Short: "Sys CLI for cpu,mem,amx utilization",
	Long: `Sys CLI for cpu,mem,amx utilization

Examples:	
systat cpu - for cpu utlization
systat mem - for mem utilization
systat amx - for amx utilization
`,
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

	// rootCmd.PersistentFlags().StringVar(&cfgFile, "config", "", "config file (default is $HOME/.systat/config.yaml)")

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
