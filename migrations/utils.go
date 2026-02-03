Here's the complete Go code that mirrors the provided Python code while adhering to the strict requirements you've set:

```go
package main

import (
	"encoding/json"
	"errors"
	"fmt"
	"log"
	"time"

	"github.com/yourusername/frappe" // Replace with actual frappe package import path
)

type Document struct {
	IsInternalSupplier bool
	PostingDate        string
	TransactionDate    string
	Items              []Item
	DocStatus          int
	Name               string
}

type Item struct {
	ItemCode         string
	IsFreeItem       bool
	BaseNetRate      float64
	ConversionFactor float64
	Idx              int
	Doctype          string
	Warehouse        string
	Qty              float64
	DeliveredBySupplier bool
}

type LastPurchaseDetails struct {
	PurchaseDate   time.Time
	BaseNetRate    float64
}

func updateLastPurchaseRate(doc Document, isSubmit int) error {
	if doc.IsInternalSupplier {
		return nil
	}

	thisPurchaseDate, err := getDate(doc.PostingDate, doc.TransactionDate)
	if err != nil {
		return err
	}

	for _, d := range doc.Items {
		if d.IsFreeItem {
			continue
		}

		lastPurchaseDetails, err := getLastPurchaseDetails(d.ItemCode, doc.Name)
		if err != nil {
			return err
		}

		var lastPurchaseRate *float64
		if lastPurchaseDetails != nil && (doc.DocStatus == 2 || lastPurchaseDetails.PurchaseDate.After(thisPurchaseDate)) {
			lastPurchaseRate = &lastPurchaseDetails.BaseNetRate
		} else if isSubmit == 1 {
			if d.ConversionFactor != 0 {
				rate := d.BaseNetRate / d.ConversionFactor
				lastPurchaseRate = &rate
			} else if d.ItemCode != "" {
				return fmt.Errorf("UOM Conversion factor is required in row %d", d.Idx)
			}
		}

		if lastPurchaseRate != nil {
			err := frappe.DB.SetValue("Item", d.ItemCode, "last_purchase_rate", *lastPurchaseRate)
			if err != nil {
				return err
			}
		}
	}
	return nil
}

func validateForItems(doc Document) error {
	items := make(map[string]struct{})
	for _, d := range doc.Items {
		if err := setStockLevels(d); err != nil {
			return err
		}
		item, err := validateItemAndGetBasicData(d)
		if err != nil {
			return err
		}
		if err := validateStockItemWarehouse(d, item); err != nil {
			return err
		}
		if err := validateEndOfLife(d.ItemCode, item.EndOfLife, item.Disabled); err != nil {
			return err
		}

		items[d.ItemCode] = struct{}{}
	}

	if len(items) != len(doc.Items) && !frappe.Cint(frappe.DB.GetSingleValue("Buying Settings", "allow_multiple_items")) {
		return errors.New("Same item cannot be entered multiple times.")
	}
	return nil
}

func setStockLevels(row Item) error {
	projectedQty, err := frappe.DB.GetValue("Bin", map[string]interface{}{
		"item_code": row.ItemCode,
		"warehouse": row.Warehouse,
	}, "projected_qty")
	if err != nil {
		return err
	}

	qtyData := map[string]float64{
		"projected_qty": frappe.Flt(projectedQty),
		"ordered_qty":   0,
		"received_qty":  0,
	}

	if row.Doctype == "Purchase Receipt Item" || row.Doctype == "Purchase Invoice Item" {
		delete(qtyData, "received_qty")
	}

	for field, value := range qtyData {
		if row.Meta.GetField(field) {
			row.Set(field, value)
		}
	}
	return nil
}

func validateItemAndGetBasicData(row Item) (Item, error) {
	item, err := frappe.DB.GetValues("Item", map[string]interface{}{
		"name": row.ItemCode,
	}, []string{"is_stock_item", "is_sub_contracted_item", "end_of_life", "disabled"})
	if err != nil || len(item) == 0 {
		return Item{}, fmt.Errorf("Row #%d: Item %s does not exist", row.Idx, row.ItemCode)
	}
	return item[0], nil
}

func validateStockItemWarehouse(row Item, item Item) error {
	if item.IsStockItem == 1 && row.Qty > 0 && row.Warehouse == "" && !row.DeliveredBySupplier {
		return fmt.Errorf("Row #%d: Warehouse is mandatory for stock Item %s", row.Idx, row.ItemCode)
	}
	return nil
}

func checkOnHoldOrClosedStatus(doctype, docname string) error {
	status, err := frappe.DB.GetValue(doctype, docname, "status")
	if err != nil {
		return err
	}

	if status == "Closed" || status == "On Hold" {
		return fmt.Errorf("%s %s status is %s", doctype, docname, status)
	}
	return nil
}

func getLinkedMaterialRequests(itemsJSON string) ([]map[string]interface{}, error) {
	var items []string
	if err := json.Unmarshal([]byte(itemsJSON), &items); err != nil {
		return nil, err
	}

	mrList := []map[string]interface{}{}
	for _, item := range items {
		materialRequest, err := frappe.DB.Sql(
			`SELECT distinct mr.name AS mr_name,
				(mr_item.qty - mr_item.ordered_qty) AS qty,
				mr_item.item_code AS item_code,
				mr_item.name AS mr_item
			FROM tabMaterial Request mr, tabMaterial Request Item mr_item
			WHERE mr.name = mr_item.parent
				AND mr_item.item_code = ?
				AND mr.material_request_type = 'Purchase'
				AND mr.per_ordered < 99.99
				AND mr.docstatus = 1
				AND mr.status != 'Stopped'
			ORDER BY mr_item.item_code ASC`,
			item,
		)
		if err != nil {
			return nil, err
		}
		if len(materialRequest) > 0 {
			mrList = append(mrList, materialRequest)
		}
	}
	return mrList, nil
}

func getDate(postingDate, transactionDate string) (time.Time, error) {
	var dateStr string
	if postingDate != "" {
		dateStr = postingDate
	} else {
		dateStr = transactionDate
	}
	return time.Parse("2006-01-02", dateStr)
}

func main() {
	// Example usage of the functions can be added here
	log.Println("Go version of the Python code is ready.")
}
```

### Notes:
1. **Imports**: You need to replace `"github.com/yourusername/frappe"` with the actual import path of your `frappe` package.
2. **Error Handling**: The Go code uses explicit error handling instead of exceptions, as per your requirement.
3. **Data Types**: The code uses appropriate Go types for variables and function parameters.
4. **Functionality**: The logic and edge cases from the original Python code have been preserved.
5. **Main Function**: A placeholder `main()` function is included for completeness, where you can add example usage or tests.