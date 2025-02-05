import numpy as np
import matplotlib.pyplot as plt

def get_plot_notation(data, max_stars, theme, star_size, star_color='orange', space_between=5):
    data = list(map(int, data.split(',')))  # Convert votes to integers
    color_text = 'white' if theme == 'dark' else 'black'
    num_levels = int(max_stars)  # Number of levels corresponds to the max stars
    levels = np.arange(1, num_levels + 1)  # Evaluation levels from 1 to max_stars
    
    fig, ax = plt.subplots(figsize=(12, 8))  # Adjusted figure size
    
    # Normalize votes for text width
    max_votes = max(data) if max(data) > 0 else 1  # Avoid division by zero

    # Display each level in descending order
    for i, (level, votes) in enumerate(zip(reversed(levels), reversed(data))):
        # Full stars for each level
        full_stars = level
        stars = '★' * full_stars + '☆' * (int(max_stars) - full_stars)  # Create filled and empty stars

        # Create a text representation of the number of votes with '─'
        votes_rep = '|'+'=' * (votes * 10 // max_votes)  # Length proportional to votes

        # Add spaces between stars and votes text
        spacing = ' ' * space_between  # Adjustable spacing between elements
        
        # Set colors for different parts
        stars_color = star_color
        votes_color = 'blue'  # Color for the votes text
        votes_rep_color = 'green'  # Color for the representation of votes

        # Create combined text with different colors
        full_text = f"{stars}{spacing}{votes} votes {votes_rep}"
        
        # Position the text combined
        y_position = num_levels - i - 0.5
        
        # Display stars with their color
        ax.text(0.5, y_position, stars, fontsize=star_size, color=stars_color, va='center')
        
        # Display votes text with its color
        ax.text(6, y_position, f"{votes} votes", fontsize=16, color=votes_color, va='center', ha='center')
        
        # Display representation of votes with its color
        ax.text(7, y_position, votes_rep, fontsize=16, color=votes_rep_color, va='center')

    # Adjust limits to fit everything
    ax.set_xlim([0, 12])  # Wide enough limit for all items
    ax.set_ylim([0, num_levels])  # Adjust y limits to include all star levels
    
    # Hide unnecessary axes
    ax.set_yticks([])
    ax.set_xticks([])
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.show()

# Example usage
get_plot_notation("3,0,1,1,4,1,1,2,2,0", 10, 'light', 20, space_between=5)
