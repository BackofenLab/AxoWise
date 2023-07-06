import matplotlib.pyplot as plt

# Input sizes
sizes = [500, 1000, 2000, 5000, 10000]

# Measured times for function 1
times_old = [7.67753911, 13.925365686, 20.008758783, 26.585243702, 31.92001462]

# Measured times for function 2
times_new = [3.594931985, 4.127116085, 4.404329399, 4.394800243, 4.935018612]

# Measured times for function 3
times_multiprocessing = [0.879, 0.928, 1.006, 1.130, 1.415]

# Plot the data
plt.plot(sizes, times_old, label="Old Enrichment")
plt.plot(sizes, times_new, label="Optimized Enrichment")
plt.plot(sizes, times_multiprocessing, label="Optimized Enrichment with multiprocessing")

# Set labels and title
plt.xlabel("Input Size (Proteins)")
plt.ylabel("Time (s)")
plt.title("Execution Time Comparison")

# Add a legend
plt.legend()

# Show the plot
plt.show()
