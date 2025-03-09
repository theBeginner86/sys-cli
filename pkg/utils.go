package pkg

import (
	"fmt"
	"os"
	"os/user"
	"path"
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

func WriteOutput(data []byte, op string) error {
	filename := op + ".log"
	fpath := path.Join(OutputDir, filename)
	
	f, err := os.Create(fpath)
	if err != nil {
		return err
	}
	defer f.Close()

	_, err = f.Write(data)
	if err != nil {
		return err
	}

	return nil
}
