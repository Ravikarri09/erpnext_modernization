Here is the equivalent Go code that produces the same output as the provided Python code:

```go
package main

import (
	"fmt"
)

func main() {
	result := add(2, 3)
	fmt.Println(result)
}

func add(a int, b int) int {
	return a + b
}
```

This Go program defines a `main` function that calls an `add` function to sum the numbers 2 and 3, and then prints the result, which matches the output of the original Python code.