def linear_search(data, key):         # Function to search using Linear Search
    comparisons = 0
    for item in data:                 # Loop through each item
        comparisons += 1
        if item["RequestId"] == key:  # Check if request ID matches
            return True, comparisons
    return False, comparisons
