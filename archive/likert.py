# import matplotlib.pyplot as plt
# import numpy as np

# def plot_bubble_chart(data, items, evaluation_levels, bubble_scale=100, x_margin=0.2, y_margin=0.2):
#     """
#     Plots a bubble chart where the color represents the evaluation level (green to red),
#     and the opacity of each bubble is inversely related to the bubble size (larger bubbles are more transparent).

#     Parameters:
#     data (2D array): The number of people for each item at each evaluation level.
#                      Rows represent items, columns represent evaluation levels.
#     items (list): Labels for the items (y-axis).
#     evaluation_levels (list): Labels for the evaluation levels (x-axis).
#     bubble_scale (int): Scaling factor for bubble sizes (default 100).
#     x_margin (float): Additional space between bubbles horizontally.
#     y_margin (float): Additional space between bubbles vertically.
#     """
    
#     # Create a grid of X and Y positions
#     x, y = np.meshgrid(np.arange(data.shape[1]), np.arange(data.shape[0]))

#     # Flatten the data to use it for both size and color mapping
#     bubble_sizes = data.flatten() * bubble_scale  # Scale bubble sizes for visibility

#     # Normalize bubble sizes to [0, 1] for opacity control (larger bubbles = lower opacity)
#     max_size = bubble_sizes.max()
#     min_size = bubble_sizes.min()
#     opacities = (max_size - bubble_sizes) / (max_size - min_size)  # Larger bubbles have lower opacity

#     # Create a fixed color for each evaluation level (column)
#     num_levels = len(evaluation_levels)
#     color_map = plt.cm.RdYlGn(np.linspace(0, 1, num_levels))  # Green to red colormap
#     colors = np.array([color_map[i % num_levels] for i in np.arange(data.shape[1])])  # Apply colors based on column index

#     # Create the bubble chart
#     plt.figure(figsize=(10, 6))

#     # Plot bubbles with same color per evaluation level and varying opacity based on size
#     for i in range(data.shape[1]):  # Loop through each evaluation level (column)
#         color = colors[i]  # Get the color for the current evaluation level
#         for j in range(data.shape[0]):  # Loop through each item (row)
#             alpha = opacities[i * data.shape[0] + j]  # Get the opacity for the current bubble size
#             plt.scatter(x[j, i], y[j, i], s=data[j, i] * bubble_scale, color=color, edgecolor='black', alpha=alpha)

#     # Add labels and grid lines
#     plt.xticks(np.arange(data.shape[1]), evaluation_levels, rotation=45, ha="right")
#     plt.yticks(np.arange(data.shape[0]), items)
#     plt.grid(True)

#     # Adjust margins by setting axis limits
#     plt.xlim(-x_margin, data.shape[1] - 1 + x_margin)  # Add margin on x-axis
#     plt.ylim(-y_margin, data.shape[0] - 1 + y_margin)  # Add margin on y-axis
    
#     # Adjust layout spacing
#     plt.subplots_adjust(left=0.15, right=0.9, top=0.9, bottom=0.2)

#     # Add a title
#     plt.title('Bubble Chart: Number of People by Evaluation Level (Opacity by Size)')

#     # Show the plot
#     plt.tight_layout()
#     plt.show()

# # Example usage:
# data = np.array([
#     [50, 20, 15, 10, 5],   # Item 1
#     [30, 40, 25, 10, 5],   # Item 2
#     [20, 10, 30, 40, 50],  # Item 3
#     [25, 35, 20, 15, 5]    # Item 4
# ])

# items = ['Item 1', 'Item 2', 'Item 3', 'Item 4']
# evaluation_levels = ['Very Favorable', 'Favorable', 'Neutral', 'Unfavorable', 'Not at All Favorable']

# # Call the function with custom bubble size scaling and margins
# plot_bubble_chart(data, items, evaluation_levels, bubble_scale=200, x_margin=0.5, y_margin=0.5)


import matplotlib.pyplot as plt
import numpy as np

import matplotlib
import matplotlib as mpl


# vegetables = ["cucumber", "tomato", "lettuce", "asparagus",
#               "potato", "wheat", "barley"]
# farmers = ["Farmer Joe", "Upland Bros.", "Smith Gardening",
#            "Agrifun", "Organiculture", "BioGoods Ltd.", "Cornylee Corp."]

items = ['Item 1', 'Item 2', 'Item 3', 'Item 4']
levels = ['Very Favorable', 'Favorable', 'Neutral', 'Unfavorable', 'Not at All Favorable']

data = np.array([
    [50, 20, 15, 10, 5],   # Item 1
    [30, 40, 15, 10, 5],   # Item 2
    [20, 10, 30, 35, 5],  # Item 3
    [25, 35, 20, 15, 5]    # Item 4
])

fig, ax = plt.subplots()
im = ax.imshow(data)

# Show all ticks and label them with the respective list entries
ax.set_xticks(np.arange(len(levels)), labels=levels)
ax.set_yticks(np.arange(len(items)), labels=items)

# Rotate the tick labels and set their alignment.
plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")

# Loop over data dimensions and create text annotations.
for i in range(len(items)):
    for j in range(len(levels)):
        text = ax.text(j, i, data[i, j],
                       ha="center", va="center", color="w")

# ax.set_title("Harvest of local farmers (in tons/year)")
fig.tight_layout()
plt.show()