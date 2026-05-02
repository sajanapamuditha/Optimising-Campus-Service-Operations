import csv
import time
import math             # Used for mathematical calculations


# -------------------------------------------------
# LOAD LOCATIONS FROM CSV
# -------------------------------------------------
def load_locations(file_path):        # Function to load location data from CSV
    locations = {}                    # Dictionary to store location coordinates

    with open(file_path, "r") as file: # Open CSV file in read mode
        reader = csv.DictReader(file)  # Read each row as a dictionary

        for row in reader:             # Loop through each row in CSV
            location_id = row["LocationID"]  # Get location ID
            x_value = float(row["X"])
            y_value = float(row["Y"])

            locations[location_id] = (x_value, y_value) # Store coordinates

    return locations


# -------------------------------------------------
# DISTANCE CALCULATION
# -------------------------------------------------
def find_distance(point_a, point_b):  # Function to calculate distance between two points
    x_diff = point_a[0] - point_b[0]
    y_diff = point_a[1] - point_b[1]

    dist = math.sqrt(x_diff * x_diff + y_diff * y_diff) # Euclidean distance formula
    return dist


# -------------------------------------------------
# GREEDY NEAREST NEIGHBOUR
# -------------------------------------------------
def greedy_route(start_point, locations): # Greedy algorithm for route Optimisation
    visited = [start_point]
    total_distance = 0
    current_point = start_point

    remaining_points = list(locations.keys()) # List of all locations
    remaining_points.remove(start_point)      # Remove start location

    while len(remaining_points) > 0:  # Loop until all locations are visited
        nearest_point = None
        nearest_distance = None

        for point in remaining_points: # Check each remaining location
            current_distance = find_distance(
                locations[current_point],
                locations[point]
            )

            if nearest_distance is None or current_distance < nearest_distance:
                nearest_distance = current_distance # Update shortest distance
                nearest_point = point               # Update nearest location

        visited.append(nearest_point)
        total_distance = total_distance + nearest_distance
        current_point = nearest_point
        remaining_points.remove(nearest_point) # Remove visited location

    return visited, round(total_distance, 2)


# -------------------------------------------------
# SIMPLE DIJKSTRA ALGORITHM
# -------------------------------------------------
def dijkstra_shortest(start_point, locations): # Function to find Shortest paths
    shortest_distances = {}
    visited = []

    for point in locations:           # Initialize distances
        shortest_distances[point] = None

    shortest_distances[start_point] = 0 # Distance to start point is zero

    while len(visited) < len(locations): # Loop until all locations are visited
        current_point = None
        smallest_distance = None

        for point in shortest_distances:  # Find nearest unvisited point
            if point not in visited and shortest_distances[point] is not None:
                if smallest_distance is None or shortest_distances[point] < smallest_distance:
                    smallest_distance = shortest_distances[point]
                    current_point = point

        visited.append(current_point)  # Mark current point as visited

        for next_point in locations:  # Check all neighbours
            if next_point not in visited:
                edge_distance = find_distance(
                    locations[current_point], # Current location
                    locations[next_point]     # Neighbour location
                )

                new_distance = shortest_distances[current_point] + edge_distance

                if shortest_distances[next_point] is None or new_distance < shortest_distances[next_point]:
                    shortest_distances[next_point] = new_distance # Update distance

    return shortest_distances          # Return shortest distances


# -------------------------------------------------
# MAIN PROGRAM
# -------------------------------------------------
print("*" * 40)                       # Print header line
print("ROUTE OPTIMISATION - TASK 4")  # Print title
print("*" * 40)

locations_data = load_locations("campus_dataset/locations.csv") # Load locations
start_location = "L001"               # Starting location


# -------- GREEDY ROUTE --------
start_time = time.time()              # Start time for greedy algorithm
result = greedy_route(start_location, locations_data) # Run greedy algorithm
route = result[0]                     # Extract route list from the result
distance = result[1]                  # Extract total distance
end_time = time.time()                # End time

print("\nGreedy Nearest-Neighbour Route:")
print(" -> ".join(route))             # Display route
print("Total Distance:", distance)    # Display distance
print("Execution Time:", round((end_time - start_time) * 1000, 3), "ms") # Time


# -------- DIJKSTRA --------
start_time = time.time()              # Start time for Dijkstra
shortest_result = dijkstra_shortest(start_location, locations_data) # Run Dijkstra
end_time = time.time()                # End time

print("\nDijkstra Shortest Distances from", start_location)
for location in sorted(shortest_result): # Loop through results
    print(location, ":", round(shortest_result[location], 2)) # Print distances

print("Execution Time:", round((end_time - start_time) * 1000, 3), "ms") # Time
