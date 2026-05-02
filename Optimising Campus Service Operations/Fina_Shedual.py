import csv
import time
import math


# ---------- LOAD REQUESTS ----------
def load_requests(filename):          # Function to load requests from CSV file
    data = []
    with open(filename, "r") as file: # Open requests file in read mode
        reader = csv.DictReader(file)
        for row in reader:            # Loop through each row
            if row["RequestID"] != "" and row["LocationID"] != "": # Check valid data
                data.append(row)
    return data

# ---------- LOAD STAFF ----------
def load_staff(filename):             # Function to load staff IDs
    staffs = []
    with open(filename, "r") as file: # Open staff file in read mode
        reader = csv.DictReader(file)
        for row in reader:            # Loop through each row
            staffs.append(row["StaffID"])
    return staffs

# ---------- LOAD LOCATIONS ----------
def load_locations(filename):         # Function to load locations and coordinates
    location = {}
    with open(filename, "r") as file: # Open locations file
        reader = csv.DictReader(file)
        for row in reader:            # Loop through rows
            location[row["LocationID"]] = ( # Use location ID as key
                float(row["X"]),      # Store X coordinate
                float(row["Y"])
            )
    return location


# ---------- DISTANCE ----------
def distance(p1, p2):                 # Function to calculate distance between two points
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
    # Uses Euclidean distance formula


# ---------- GREEDY TO TARGET ----------
def greedy_to_target(start, target, location): # Greedy algorithm to find route
    current = start
    visited = [start]
    total = 0

    remaining = list(location.keys()) # List of all locations
    if start in remaining:
        remaining.remove(start)

    while current != target:          # Loop until target location is reached
        nearest = None
        shortest = None

        for loc in remaining:         # Check all remaining locations
            d = distance(locations[current], locations[loc]) # Calculate distance
            if shortest is None or d < shortest:
                shortest = d
                nearest = loc


        visited.append(nearest)       # Add nearest location to route
        total += shortest             # Add distance to total
        current = nearest             # Move to nearest location
        remaining.remove(nearest)     # Remove visited location

    return visited, round(total, 2)


# =================== MAIN ===================

start_time = time.time()              # Record program start time

requests = load_requests("campus_dataset/requests.csv")
staff = load_staff("campus_dataset/staff.csv")
locations = load_locations("campus_dataset/locations.csv")

print("\nFINAL SERVICE SCHEDULE")
print("=" * 60)

staff_index = 0  # Keeps track of current staff member
count = 0  # Counts assigned staff requests

for req in requests:                  # Loop through each request
    route, dist = greedy_to_target("L001", req["LocationID"], locations)

    print("Request:", req["RequestID"])
    print("Staff:", staff[staff_index])
    print("Location:", req["LocationID"])
    print("Route:", " -> ".join(route))
    print("Distance:", dist)
    print("-" * 38)

    count += 1
    if count == 5 and staff_index < len(staff) - 1: # After 5 requests
        staff_index += 1 # Moves next staff member
        count = 0  # Resets request
