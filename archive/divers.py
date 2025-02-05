import random

# Générer un tableau de 20 entrées avec des nombres aléatoires
tableau_aleatoire = [random.randint(1, 100) for _ in range(20)]

# # Afficher le tableau
# print(tableau_aleatoire)

n = [["2","3"],["2","3"]]
print(type(n))


def get_unique_values(arr):
    # Utiliser set() pour obtenir les valeurs uniques
    unique_values = list(set(arr))
    return unique_values

# Your array
arr = [3, 0, 1, 1, 4, 1, 1, 2, 2, 0]

# Calculate the sum of the array
total = sum(arr)

# Convert each value to percentage with 2 decimal places
percentage_array = [round((x / total) * 100, 2) for x in arr]

# Print the percentage array
print(percentage_array)