def bubble_sort(data):                # Function to sort data using Bubble Sort
    comparisons = 0
    n = len(data)
    for i in range(n):                # Outer loop for passes
        for j in range(0, n - i - 1): # Inner loop for comparisons
            comparisons += 1
            if data[j]["Priority"] > data[j + 1]["Priority"]: # Compare priorities
                data[j], data[j + 1] = data[j + 1], data[j]
    return data, comparisons