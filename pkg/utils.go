package pkg

import (
	"fmt"
	"os"
	"os/user"
	"path/filepath"
)

var (
	OutputDir string
)

func SetOutputDirectory() {
	usr, err := user.Current()
	if err != nil {
		OutputDir = filepath.Join(".sys-cli", "out")
	} else {
		OutputDir = filepath.Join(usr.HomeDir, ".sys-cli", "out")
	}
}

func CreateOutputDirIfNotExists() {
	_, err := os.Stat(OutputDir)
	if os.IsNotExist(err) {
		err := os.MkdirAll(OutputDir, 0775)
		if err != nil {
			fmt.Println(err)
		}
	}
}
