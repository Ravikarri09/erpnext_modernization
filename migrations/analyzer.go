<<<<<<< HEAD
=======
Here is the equivalent Go code:

>>>>>>> 4d819b2b0cb55e458eb42f71380483a173ed803d
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
<<<<<<< HEAD
)

const BASE_ERP_PATH = "erpnext/erpnext"
const OUTPUT_FOLDER = "output"

=======

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

>>>>>>> 4d819b2b0cb55e458eb42f71380483a173ed803d
var functionsData []FunctionData
var classesData []ClassData
var callsData []CallData

<<<<<<< HEAD
type FunctionData struct {
	Name string `json:"name"`
	File string `json:"file"`
	Line int    `json:"line"`
=======
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
>>>>>>> 4d819b2b0cb55e458eb42f71380483a173ed803d
}

type ClassData struct {
	Name string `json:"name"`
	File string `json:"file"`
	Line int    `json:"line"`
}

type CallData struct {
	Caller string `json:"caller"`
	Callee string `json:"callee"`
	File   string `json:"file"`
}

func analyzeFile(filePath string) {
	code, err := ioutil.ReadFile(filePath)
	if err != nil {
		return
	}

	tree, err := parsePythonCode(string(code))
	if err != nil {
		return
	}

	currentFunction := ""

	for _, node := range tree {
		switch n := node.(type) {
		case FunctionDef:
			functionsData = append(functionsData, FunctionData{
				Name: n.Name,
				File: filePath,
				Line: n.Line,
			})
			currentFunction = n.Name

		case ClassDef:
			classesData = append(classesData, ClassData{
				Name: n.Name,
				File: filePath,
				Line: n.Line,
			})

		case Call:
			if currentFunction != "" {
				callsData = append(callsData, CallData{
					Caller: currentFunction,
					Callee: n.Func.Name,
					File:   filePath,
				})
			}
		}
	}
}

func analyzeModule(moduleName string) {
	modulePath := filepath.Join(BASE_ERP_PATH, moduleName)

<<<<<<< HEAD
	if _, err := os.Stat(modulePath); os.IsNotExist(err) {
		fmt.Printf("Module not found: %s\n", moduleName)
		os.Exit(1)
=======
	if !filepath.Exists(modulePath) {
		log.Printf("Module not found: %s", moduleName)
		return fmt.Errorf("module not found")
>>>>>>> 4d819b2b0cb55e458eb42f71380483a173ed803d
	}

	log.Println("\n🔍 Analyzing ERPNext module:", moduleName)

	err := filepath.Walk(modulePath, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}
<<<<<<< HEAD
		if strings.HasSuffix(info.Name(), ".py") {
			analyzeFile(path)
		}
		return nil
	})
=======
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
>>>>>>> 4d819b2b0cb55e458eb42f71380483a173ed803d
	if err != nil {
		fmt.Println("Error walking the path:", err)
	}
<<<<<<< HEAD
}

func saveOutput(moduleName string) {
	os.MkdirAll(OUTPUT_FOLDER, os.ModePerm)

	functionsFile, _ := json.MarshalIndent(functionsData, "", "  ")
	ioutil.WriteFile(fmt.Sprintf("%s/%s_functions.json", OUTPUT_FOLDER, moduleName), functionsFile, 0644)

	classesFile, _ := json.MarshalIndent(classesData, "", "  ")
	ioutil.WriteFile(fmt.Sprintf("%s/%s_classes.json", OUTPUT_FOLDER, moduleName), classesFile, 0644)

	callsFile, _ := json.MarshalIndent(callsData, "", "  ")
	ioutil.WriteFile(fmt.Sprintf("%s/%s_calls.json", OUTPUT_FOLDER, moduleName), callsFile, 0644)
=======

	err = json.NewFileWriter(f"{OUTPUT_FOLDER}/{moduleName}_classes.json").Write(classesData)
	if err != nil {
		return err
	}

	err = json.NewFileWriter(f"{OUTPUT_FOLDER}/{moduleName}_calls.json").Write(callsData)
	if err != nil {
		return err
	}

	return nil
>>>>>>> 4d819b2b0cb55e458eb42f71380483a173ed803d
}

func main() {

	if len(os.Args) < 2 {
<<<<<<< HEAD
		fmt.Println(" Please provide a module name")
		fmt.Println(" Example: go run analyzer.go accounts")
=======
		log.Println("Please provide a module name")
		log.Println("Example: go run analyzer.go accounts")
>>>>>>> 4d819b2b0cb55e458eb42f71380483a173ed803d
		os.Exit(1)
	}

	module := os.Args[1]

<<<<<<< HEAD
	analyzeModule(module)
	saveOutput(module)

	fmt.Println("\n===================================")
	fmt.Println(" Analysis Complete!")
	fmt.Println(" Module:", module)
	fmt.Println(" Functions found:", len(functionsData))
	fmt.Println(" Classes found:", len(classesData))
	fmt.Println(" Call relationships:", len(callsData))
	fmt.Println(" Output saved in /output folder")
	fmt.Println("===================================")
}

// Placeholder types for Python AST nodes
type FunctionDef struct {
	Name string
	Line int
}

type ClassDef struct {
	Name string
	Line int
}

type Call struct {
	Func struct {
		Name string
	}
}

// Placeholder function to simulate parsing Python code
func parsePythonCode(code string) ([]interface{}, error) {
	// This function should return a slice of AST nodes based on the parsed code.
	// For the purpose of this translation, we will return an empty slice.
	return []interface{}{}, nil
}
```

### Notes:
1. The `parsePythonCode` function is a placeholder and should be implemented to parse Python code into AST nodes similar to the Python `ast` module. This is a complex task and requires a proper parser for Python code in Go.
2. The Go code maintains the same structure and logic as the original Python code, including error handling and output formatting.
3. The Go code uses idiomatic Go practices, such as using structs for data representation and handling errors explicitly.
=======
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
>>>>>>> 4d819b2b0cb55e458eb42f71380483a173ed803d
