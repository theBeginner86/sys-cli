package cmd

import (
  "fmt"

  "github.com/spf13/cobra"
)

var VersionCmd = &cobra.Command{
  Use:   "version",
  Short: "Print the version number of Sys CLI",
  Long:  `All software has versions. This is Sys CLI`,
  Run: func(cmd *cobra.Command, args []string) {
    fmt.Println("Sys CLI Version - v0.0.1")
  },
}