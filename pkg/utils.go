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

func CreateOutputFile(op string) error {
	filename := op + ".log"
	fpath := path.Join(OutputDir, filename)

		_, err := os.Create(fpath)
		if err != nil {
			return err
		}	
		return nil
}

// TODO: use mutex for thread safe
func WriteBytesToFile(data []byte, op string) error {
	filename := op + ".log"
	fpath := path.Join(OutputDir, filename)

		f, err := os.OpenFile(fpath, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
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

// TODO: use mutex for thread safe
func WriteStringToFile(data string, op string) error {
	filename := op + ".log"
	fpath := path.Join(OutputDir, filename)

		f, err := os.OpenFile(fpath, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
		if err != nil {
			return err
		}
		defer f.Close()

	_, err = f.WriteString(data)
	if err != nil {
		return err
	}

	return nil
}
