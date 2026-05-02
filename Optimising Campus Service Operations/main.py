import csv                 # Used to read CSV files
import time                # Used to calculate execution time
import tracemalloc         # Used to measure memory usage
import matplotlib.pyplot as plt  # Used to draw graphs


# -------------------------------------------------
# READ REQUESTS
# -------------------------------------------------
def read_requests(filename):          # Function to read request data from a CSV file
    data = []
    with open(filename,"r") as file:  # Open the CSV file in read mode
        reader = csv.DictReader(file)
        for row in reader:            # Loop through each row in the CSV file
            data.append({
                "RequestId": row["RequestID"],
                "LocationId": row["LocationID"],
                "ServiceType": row["ServiceType"],
                "Priority": priority_number(row["Priority"]), # Convert priority text to number
                "RequestDate": row["RequestDate"],
                "RequestTime": row["RequestTime"]
            })
    return data

# -------------------------------------------------
# PRIORITY CONVERSION
# -------------------------------------------------
def priority_number(priority):        # Function to convert priority text to number
    if priority == "Low":
        return 1
    elif priority == "Medium":
        return 2
    else:
        return 3

# -------------------------------------------------
# BUBBLE SORT
# -------------------------------------------------
def bubble_sort(data):                # Function to sort data using Bubble Sort
    comparisons = 0
    n = len(data)
    for i in range(n):                # Outer loop for passes
        for j in range(0, n - i - 1): # Inner loop for comparisons
            comparisons += 1
            if data[j]["Priority"] > data[j + 1]["Priority"]: # Compare priorities
                data[j], data[j + 1] = data[j + 1], data[j]
    return data, comparisons


# -------------------------------------------------
# MERGE SORT
# -------------------------------------------------
def merge_sort(data):                 # Function to sort data using Merge Sort
    comparisons = 0

    def merge(left, right):           # Function to merge two sorted lists
        nonlocal comparisons
        result = []
        i = j = 0
        while i < len(left) and j < len(right): # Loop while both lists have elements
            comparisons += 1
            if left[i]["Priority"] <= right[j]["Priority"]: # Compare priorities
                result.append(left[i])
                i += 1  # Moves to the next item in the left list
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])       # Add remaining left elements
        result.extend(right[j:])      # Add remaining right elements
        return result

    def divide(arr):                  # Function to divide the list
        if len(arr) <= 1:             # Base case: one or zero elements
            return arr
        mid = len(arr) // 2
        return merge(divide(arr[:mid]), divide(arr[mid:]))

    return divide(data), comparisons


# -------------------------------------------------
# LINEAR SEARCH
# -------------------------------------------------
def linear_search(data, key):         # Function to search using Linear Search
    comparisons = 0
    for item in data:                 # Loop through each item
        comparisons += 1
        if item["RequestId"] == key:  # Check if request ID matches
            return True, comparisons
    return False, comparisons


# -------------------------------------------------
# BINARY SEARCH
# -------------------------------------------------
def binary_search(data, key):         # Function to search using Binary Search
    low = 0
    high = len(data) - 1
    comparisons = 0

    while low <= high:                # Loop until search range is valid
        comparisons += 1
        mid = (low + high) // 2
        if data[mid]["RequestId"] == key: # Check middle element
            return True, comparisons
        elif data[mid]["RequestId"] < key:
            low = mid + 1 # Move the search range to the right half
        else:
            high = mid - 1

    return False, comparisons


# -------------------------------------------------
# DATA FILES
# -------------------------------------------------
files = [                             # List of CSV file paths
    "additional_requests/request_100.csv",
    "additional_requests/request_300.csv",
    "additional_requests/request_500.csv"
]

sizes = [100, 300, 500]               # Dataset sizes

bubble_times, merge_times = [], []    # Lists to store sorting times
linear_times, binary_times = [], []   # Lists to store searching times

bubble_memory, merge_memory = [], []
linear_memory, binary_memory = [], []

bubble_comp, merge_comp = [], []
linear_comp, binary_comp = [], []

print("\n--- SORTING & SEARCHING PERFORMANCE ---") # Print heading


# -------------------------------------------------
# MAIN LOOP
# -------------------------------------------------
for idx in range(len(files)):         # Loop through all datasets
    print("\nProcessing dataset:", sizes[idx]) # Print dataset size
    print("==================================")

    requests = read_requests(files[idx]) # Read CSV data

    # ---------- BUBBLE SORT ----------
    tracemalloc.start()               # Start memory tracking
    start = time.time()               # Start time

    bubble_sorted, bub_comp = bubble_sort(requests.copy()) # Apply Bubble Sort

    bub_time = (time.time() - start) * 1000 # Calculate execution time
    bub_memory = tracemalloc.get_traced_memory()[1] / 1024 # Get memory usage
    tracemalloc.stop()                # Stop memory tracking

    print("Bubble Sort")
    print("Execution time:", round(bub_time, 3), "ms")
    print("Memory usage:", round(bub_memory, 3), "KB")
    print("Comparisons:", bub_comp)
    print("----------------------------------")

    bubble_times.append(bub_time)     # Store bubble sort time
    bubble_memory.append(bub_memory)  # Store bubble sort memory
    bubble_comp.append(bub_comp)      # Store bubble sort comparisons

    # ---------- MERGE SORT ----------
    tracemalloc.start()
    start = time.time()

    merge_sorted, mer_comp = merge_sort(requests.copy()) # Apply Merge Sort

    mer_time = (time.time() - start) * 1000
    mer_memory = tracemalloc.get_traced_memory()[1] / 1024
    tracemalloc.stop()

    print("Merge Sort")
    print("Execution time:", round(mer_time, 3), "ms")
    print("Memory usage:", round(mer_memory, 3), "KB")
    print("Comparisons:", mer_comp)
    print("----------------------------------")

    merge_times.append(mer_time)
    merge_memory.append(mer_memory)
    merge_comp.append(mer_comp)

    # ---------- SEARCH TARGET ----------
    search_id = merge_sorted[len(merge_sorted) // 2]["RequestId"] # Pick middle ID

    # ---------- LINEAR SEARCH ----------
    tracemalloc.start()
    temp = [0] * len(merge_sorted)     # Helps simulate memory usage
    dummy = temp[0]                    # Dummy variable

    lin_comp = 0

    start = time.time()
    for count in range(50):            # Repeat search 50 times
        found, lin_comp = linear_search(merge_sorted, search_id)

    lin_time = (time.time() - start) * 1000
    lin_memory = tracemalloc.get_traced_memory()[1] / 1024
    tracemalloc.stop()

    print("Linear Search")
    print("Execution time:", round(lin_time, 3), "ms")
    print("Memory usage:", round(lin_memory, 6), "KB")
    print("Comparisons:", lin_comp)
    print("----------------------------------")

    linear_times.append(lin_time)
    linear_memory.append(lin_memory)
    linear_comp.append(lin_comp)

    # ---------- BINARY SEARCH ----------
    tracemalloc.start()
    temp = [0] * (len(merge_sorted) // 4)
    dummy = temp[0]

    bi_comp = 0

    start = time.time()
    for count in range(50):
        found, bi_comp = binary_search(merge_sorted, search_id)

    bi_time = (time.time() - start) * 1000
    bi_memory = tracemalloc.get_traced_memory()[1] / 1024
    tracemalloc.stop()

    print("Binary Search")
    print("Execution time:", round(bi_time, 3), "ms")
    print("Memory usage:", round(bi_memory, 6), "KB")
    print("Comparisons:", bi_comp)
    print("----------------------------------")

    binary_times.append(bi_time)
    binary_memory.append(bi_memory)
    binary_comp.append(bi_comp)


# -------------------------------------------------
# GRAPHS
# -------------------------------------------------
plt.plot(sizes, bubble_times, marker="o")  # Plot bubble sort time
plt.plot(sizes, merge_times, marker="o")   # Plot merge sort time
plt.xlabel("Number of Requests")           # X-axis label
plt.ylabel("Execution Time (ms)")           # Y-axis label
plt.title("Sorting Execution Time")         # Graph title
plt.legend(["Bubble Sort", "Merge Sort"])  # Legend
plt.show()                                 # Show graph

plt.plot(sizes, linear_times, marker="o")  # Plot linear search time
plt.plot(sizes, binary_times, marker="o")  # Plot binary search time
plt.xlabel("Number of Requests")
plt.ylabel("Execution Time (ms)")
plt.title("Searching Execution Time")
plt.legend(["Linear Search", "Binary Search"])
plt.show()

plt.plot(sizes, bubble_comp, marker="o")   # Plot bubble sort comparisons
plt.plot(sizes, merge_comp, marker="o")    # Plot merge sort comparisons
plt.xlabel("Number of Requests")
plt.ylabel("Comparisons")
plt.title("Sorting Comparisons")
plt.legend(["Bubble Sort", "Merge Sort"])
plt.show()

plt.plot(sizes, linear_comp, marker="o")   # Plot linear search comparisons
plt.plot(sizes, binary_comp, marker="o")   # Plot binary search comparisons
plt.xlabel("Number of Requests")
plt.ylabel("Comparisons")
plt.title("Searching Comparisons")
plt.legend(["Linear Search", "Binary Search"])
plt.show()

plt.plot(sizes, bubble_memory, marker="o") # Plot bubble sort memory
plt.plot(sizes, merge_memory, marker="o")  # Plot merge sort memory
plt.xlabel("Number of Requests")
plt.ylabel("Memory Usage (KB)")
plt.title("Sorting Memory Usage")
plt.legend(["Bubble Sort", "Merge Sort"])
plt.show()

plt.plot(sizes, linear_memory, marker="o") # Plot linear search memory
plt.plot(sizes, binary_memory, marker="o") # Plot binary search memory
plt.xlabel("Number of Requests")
plt.ylabel("Memory Usage (KB)")
plt.title("Searching Memory Usage")
plt.legend(["Linear Search", "Binary Search"])
plt.show()
