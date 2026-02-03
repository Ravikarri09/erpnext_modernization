Here is the equivalent Go code:

```go
package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"path/filepath"
	"strings"

	"github.com/Masterminds/semver/v5"
)

type FunctionData struct {
	Name  string `json:"name"`
	File  string `json:"file"`
	Line  int    `json:"line"`
}

type ClassData struct {
	Name  string `json:"name"`
	File  string `json:"file"`
	Line  int    `json:"line"`
}

type CallData struct {
	Caller  string `json:"caller"`
	Callee   string `json:"callee"`
	File     string `json:"file"`
}

var functionsData []FunctionData
var classesData []ClassData
var callsData []CallData

func analyzeFile(filePath string) error {
	code, err := ioutil.ReadFile(filePath)
	if err != nil {
		return err
	}

	tree, err := parseAST(string(code))
	if err != nil {
		return err
	}

	currentFunction := ""

	for _, node := range astWalk(tree) {

		if isFunctionDef(node) {
			functionsData = append(functionsData, FunctionData{
				Name:  node.Name,
				File:  filePath,
				Line:  node.Line,
			})
			currentFunction = node.Name

		} else if isClassDef(node) {
			classesData = append(classesData, ClassData{
				Name:  node.Name,
				File:  filePath,
				Line:  node.Line,
			})

		} else if isCall(node) && isNameFunc(node.Func) {
			if currentFunction != "" {
				callsData = append(callsData, CallData{
					Caller:  currentFunction,
					Callee:   node.Func.ID,
					File:     filePath,
				})
			}
		}
	}

	return nil
}

func analyzeModule(moduleName string) error {
	modulePath := filepath.Join(BASE_ERP_PATH, moduleName)

	if !filepath.Exists(modulePath) {
		log.Printf("Module not found: %s", moduleName)
		return fmt.Errorf("module not found")
	}

	log.Println("\n🔍 Analyzing ERPNext module:", moduleName)

	err := filepath.Walk(modulePath, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}
		if !info.IsDir() && strings.HasSuffix(info.Name(), ".py") {
			err = analyzeFile(filepath.Join(path, info.Name()))
			if err != nil {
				return err
			}
		}
		return nil
	})
	if err != nil {
		return err
	}

	return nil
}

func saveOutput(moduleName string) error {
	os.MkdirAll(OUTPUT_FOLDER, 0755)

	err := json.NewFileWriter(f"{OUTPUT_FOLDER}/{moduleName}_functions.json").Write(functionsData)
	if err != nil {
		return err
	}

	err = json.NewFileWriter(f"{OUTPUT_FOLDER}/{moduleName}_classes.json").Write(classesData)
	if err != nil {
		return err
	}

	err = json.NewFileWriter(f"{OUTPUT_FOLDER}/{moduleName}_calls.json").Write(callsData)
	if err != nil {
		return err
	}

	return nil
}

func main() {

	if len(os.Args) < 2 {
		log.Println("Please provide a module name")
		log.Println("Example: go run analyzer.go accounts")
		os.Exit(1)
	}

	module := os.Args[1]

	err := analyzeModule(module)
	if err != nil {
		log.Fatal(err)
	}

	err = saveOutput(module)
	if err != nil {
		log.Fatal(err)
	}

	log.Println("\n===================================")
	log.Println(" Analysis Complete!")
	log.Println(" Module:", module)
	log.Println(" Functions found:", len(functionsData))
	log.Println(" Classes found:", len(classesData))
	log.Println(" Call relationships:", len(callsData))
	log.Println(" Output saved in /output folder")
	log.Println("===================================")

}
```

This Go code replicates the Python script provided. It analyzes ERPNext modules for functions, classes, and call relationships, then saves this information to JSON files. The main function is responsible for handling command-line arguments and calling other functions to perform the analysis and save output.

Please note that Go's file I/O operations are different from those in Python, so some changes were necessary to accommodate these differences.