package pkg

import (
	"fmt"
	"os"
	"os/user"
	"path"
	"path/filepath"
	"strings"
	"strconv"
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

func MaxFloat(a, b float64) float64 {
	if a > b {
		return a
	}
	return b
}

// parseSize converts human-readable sizes (e.g., "7.6Gi", "903Mi", "0B") to GiB
func ParseSize(sizeStr string) (float64, error) {
	if sizeStr == "" {
		return 0, fmt.Errorf("empty size string")
	}

	// Extract number and unit
	numStr := ""
	unit := ""
	for _, r := range sizeStr {
		if r >= '0' && r <= '9' || r == '.' {
			numStr += string(r)
		} else {
			unit += string(r)
		}
	}

	num, err := strconv.ParseFloat(numStr, 64)
	if err != nil {
		return 0, fmt.Errorf("invalid number in size: %v", err)
	}

	// Convert to GiB based on unit
	switch strings.ToLower(unit) {
	case "gi", "gib":
		return num, nil
	case "mi", "mib":
		return num / 1024, nil // MiB to GiB
	case "ki", "kib":
		return num / (1024 * 1024), nil // KiB to GiB
	case "b":
		return num / (1024 * 1024 * 1024), nil // Bytes to GiB
	case "":
		return num, nil // Assume GiB if no unit (unlikely)
	default:
		return 0, fmt.Errorf("unknown unit: %s", unit)
	}
}
