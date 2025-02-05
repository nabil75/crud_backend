import matplotlib.pyplot as plt
import numpy as np

# Sample data with matching dimensions
x = np.linspace(0, 10, 100)
y = np.sin(x)
data = np.random.rand(4)  # Changed from (10, 4) to (4) to match labels
labels = ['A', 'B', 'C', 'D']

# Set up the figure and a 2x2 grid of subplots
fig, axs = plt.subplots(2, 2, figsize=(10, 8))

# Line plot
axs[0, 0].plot(x, y, color="teal")
axs[0, 0].set_title("Line Chart")
axs[0, 0].set_xlabel("X-axis")
axs[0, 0].set_ylabel("Y-axis")

# Bar plot
axs[0, 1].bar(labels, data, color="orange")  # Data and labels now have matching length
axs[0, 1].set_title("Bar Chart")
axs[0, 1].set_xlabel("Category")
axs[0, 1].set_ylabel("Values")

# Scatter plot (adjust data as needed)
scatter_data_x = np.random.rand(10)
scatter_data_y = np.random.rand(10)
axs[1, 0].scatter(scatter_data_x, scatter_data_y, color="purple")
axs[1, 0].set_title("Scatter Plot")
axs[1, 0].set_xlabel("X-axis")
axs[1, 0].set_ylabel("Y-axis")

# Pie chart
axs[1, 1].pie(data, labels=labels, autopct='%1.1f%%', startangle=90, colors=["blue", "green", "red", "yellow"])
axs[1, 1].set_title("Pie Chart")

# Adjust layout to avoid overlap
plt.tight_layout()

# Display the dashboard
plt.show()
