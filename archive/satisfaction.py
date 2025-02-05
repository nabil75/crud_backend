import matplotlib.pyplot as plt

# Example data for satisfaction levels and response counts
satisfaction_levels = ['Pas du tout satisfait', 'Peu satsisfait', 'Moyennement satisfait', 'Plutôt satisfait', 'Très satsifait']  # Satisfaction levels
data = [5, 8, 12, 6, 9]  # Number of responses per level

# Create a bar chart
fig, ax = plt.subplots()

# Plot the bars
ax.bar(satisfaction_levels, data, color='skyblue')

# Customize the chart
ax.set_xlabel('Satisfaction Level')
ax.set_ylabel('Number of Responses')
ax.set_title('Responses per Satisfaction Level')

# Show the chart
plt.show()