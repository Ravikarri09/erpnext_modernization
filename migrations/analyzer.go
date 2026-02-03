

package main
import (
	"encoding/json"
	"fmt"
	"go/parser"
	"go/token"
	"io/ioutil"
	"os"
	"path/filepath"
	"strings"
	"go/ast"
)

const (
	BASE_ERP_PATH = "erpnext/erpnext"
	OUTPUT_FOLDER  = "output"
)

var (
	functionsData []map[string]interface{}
	classesData   []map[string]interface{}
	callsData     []map[string]interface{}
)

func analyzeFile(filePath string) error {
	data, err := ioutil.ReadFile(filePath)
	if err != nil {
		return err
	}

	fset := token.NewFileSet()
	node, err := parser.ParseFile(fset, "", data, parser.ParseComments)
	if err != nil {
		return err
	}

	var currentFunction string

	for _, decl := range node.Decls {
		if funcDecl, ok := decl.(*parser.FuncDecl); ok {
			functionsData = append(functionsData, map[string]interface{}{
				"name": funcDecl.Name.Name,
				"file": filePath,
				"line": fset.Position(funcDecl.Pos()).Line,
			})
			currentFunction = funcDecl.Name.Name
		}

		if genDecl, ok := decl.(*parser.GenDecl); ok {
			for _, spec := range genDecl.Specs {
				if typeSpec, ok := spec.(*parser.TypeSpec); ok {
					classesData = append(classesData, map[string]interface{}{
						"name": typeSpec.Name.Name,
						"file": filePath,
						"line": fset.Position(typeSpec.Pos()).Line,
					})
				}
			}
		}
	}

	for _, stmt := range node.Body.List {
		if callExpr, ok := stmt.(*parser.ExprStmt); ok {
			if fun, ok := callExpr.X.(*parser.CallExpr); ok {
				if ident, ok := fun.Fun.(*parser.Ident); ok {
					if currentFunction != "" {
						callsData = append(callsData, map[string]interface{}{
							"caller":  currentFunction,
							"callee":  ident.Name,
							"file":    filePath,
						})
					}
				}
			}
		}
	}

	return nil
}

func analyzeModule(moduleName string) error {
	modulePath := filepath.Join(BASE_ERP_PATH, moduleName)

	if _, err := os.Stat(modulePath); os.IsNotExist(err) {
		return fmt.Errorf("module not found: %s", moduleName)
	}

	fmt.Printf("\n🔍 Analyzing ERPNext module: %s\n", moduleName)

	return filepath.Walk(modulePath, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}
		if strings.HasSuffix(info.Name(), ".py") {
			if err := analyzeFile(path); err != nil {
				return err
			}
		}
		return nil
	})
}

func saveOutput(moduleName string) error {
	if err := os.MkdirAll(OUTPUT_FOLDER, os.ModePerm); err != nil {
		return err
	}

	if err := writeJSONFile(fmt.Sprintf("%s/%s_functions.json", OUTPUT_FOLDER, moduleName), functionsData); err != nil {
		return err
	}
	if err := writeJSONFile(fmt.Sprintf("%s/%s_classes.json", OUTPUT_FOLDER, moduleName), classesData); err != nil {
		return err
	}
	if err := writeJSONFile(fmt.Sprintf("%s/%s_calls.json", OUTPUT_FOLDER, moduleName), callsData); err != nil {
		return err
	}

	return nil
}

func writeJSONFile(filePath string, data interface{}) error {
	file, err := json.MarshalIndent(data, "", "  ")
	if err != nil {
		return err
	}
	return ioutil.WriteFile(filePath, file, 0644)
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Please provide a module name")
		fmt.Println("Example: go run analyzer.go accounts")
		os.Exit(1)
	}

	module := os.Args[1]

	if err := analyzeModule(module); err != nil {
		fmt.Println(err)
		os.Exit(1)
	}

	if err := saveOutput(module); err != nil {
		fmt.Println(err)
		os.Exit(1)
	}

	fmt.Println("\n===================================")
	fmt.Println(" Analysis Complete!")
	fmt.Printf(" Module: %s\n", module)
	fmt.Printf(" Functions found: %d\n", len(functionsData))
	fmt.Printf(" Classes found: %d\n", len(classesData))
	fmt.Printf(" Call relationships: %d\n", len(callsData))
	fmt.Println(" Output saved in /output folder")
	fmt.Println("===================================")
}
