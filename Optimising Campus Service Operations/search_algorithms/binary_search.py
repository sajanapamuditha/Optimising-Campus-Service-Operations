def binary_search(data, key):         # Function to search using Binary Search
    low = 0
    high = len(data) - 1
    comparisons = 0

    while low <= high:                # Loop until search range is valid
        comparisons += 1
        mid = (low + high) // 2
        if data[mid]["RequestId"] == key: # Check middle element
            return True, comparisons
        elif data[mid]["RequestId"] < key: # If key is greater
            low = mid + 1
        else:
            high = mid - 1

    return False, comparisons
