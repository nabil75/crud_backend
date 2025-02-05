import matplotlib.pyplot as plt
import numpy as np
from third_party_functions import *

items = ['Item 1', 'Item 2', 'Item 3', 'Item 4']
levels = ['Very Favorable', 'Favorable', 'Neutral', 'Unfavorable', 'Not at All Favorable']

data = np.array([
    [50, 20, 15, 10, 5],   # Item 1
    [30, 40, 15, 10, 5],   # Item 2
    [20, 10, 30, 35, 5],  # Item 3
    [25, 35, 20, 15, 5]    # Item 4
])

fig, ax = plt.subplots()

im, cbar = heatmap(data, items, levels, ax=ax,
                   cmap="YlGn", cbarlabel="harvest [t/year]")
texts = annotate_heatmap(im, valfmt="{x:.0f}")

fig.tight_layout()
plt.show()