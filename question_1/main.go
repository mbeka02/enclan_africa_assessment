package main

import (
	"fmt"
	"sort"
)

func main() {
	values := []int{12, 7, 12, 3, 5, 7, 8, 3, 9}
	// 1. Remove duplicates using a map
	valuesMap := make(map[int]struct{})
	// iterate through the values and add them to the map
	for _, value := range values {
		valuesMap[value] = struct{}{}
	}
	// 2. convert the map back to a slice
	filteredValues := make([]int, 0, len(valuesMap))
	for key := range valuesMap {
		filteredValues = append(filteredValues, key)
	}
	// 3. sort in ascending order
	sort.Ints(filteredValues)

	fmt.Println(filteredValues)
}
