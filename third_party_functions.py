import matplotlib.pyplot as plt
import numpy as np
import matplotlib



# Fonction pour splitter les labels sur plusieurs lignes
def split_label(label, threshold):
    words = label.split()  # Diviser la chaîne en mots
    lines = []
    current_line = []

    # Construire les lignes sans dépasser le seuil par ligne
    for word in words:
        word = word.replace("''", "'")  # Remplacer les doubles apostrophes par un seul
        # Si ajouter le mot dépasse le seuil, on commence une nouvelle ligne
        if sum(len(w) for w in current_line) + len(current_line) + len(word) > threshold:
            lines.append(" ".join(current_line))
            current_line = [word]
        else:
            current_line.append(word)
    
    # Ajouter la dernière ligne
    if current_line:
        lines.append(" ".join(current_line))
    
    # Retourner le label splitté avec des sauts de ligne
    return "\n".join(lines)

def sumReponseTrue(val_tot):
    val_result_tot =[0]*len(val_tot[0])
    for val in val_tot:
        for i in range(len(val)):
            val_result_tot[i] += val[i]
    return val_result_tot

def count_occurrences(arr, levels):
    # Initialize a dictionary with keys from 1 to 10 and default value 0
    counts = {i: 0 for i in range(1, levels+1)}
    # Iterate over the array and update the count for each value
    for num in arr:
        if num in counts:
            counts[num] += 1
    return counts

def get_unique_values(arr):
    # Utiliser set() pour obtenir les valeurs uniques
    unique_values = list(set(arr))
    return unique_values

def heatmap(data, row_labels, col_labels, ax=None,
            cbar_kw=None, cbarlabel="", theme_color="", **kwargs):
    """
    Create a heatmap from a numpy array and two lists of labels.

    Parameters
    ----------
    data
        A 2D numpy array of shape (M, N).
    row_labels
        A list or array of length M with the labels for the rows.
    col_labels
        A list or array of length N with the labels for the columns.
    ax
        A `matplotlib.axes.Axes` instance to which the heatmap is plotted.  If
        not provided, use current Axes or create a new one.  Optional.
    cbar_kw
        A dictionary with arguments to `matplotlib.Figure.colorbar`.  Optional.
    cbarlabel
        The label for the colorbar.  Optional.
    **kwargs
        All other arguments are forwarded to `imshow`.
    """

    if ax is None:
        ax = plt.gca()

    if cbar_kw is None:
        cbar_kw = {}

    # Plot the heatmap
    im = ax.imshow(data, **kwargs)

    # Create colorbar
    cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
    cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom", color=theme_color)

    # Set colorbar tick color
    cbar.ax.yaxis.set_tick_params(color=theme_color)
    plt.setp(cbar.ax.get_yticklabels(), color=theme_color)


    # Show all ticks and label them with the respective list entries.
    ax.set_xticks(np.arange(data.shape[1]), labels=col_labels)
    ax.set_yticks(np.arange(data.shape[0]), labels=row_labels, color=theme_color)

    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=True, bottom=False,
                   labeltop=True, labelbottom=False)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=-30, ha="right", rotation_mode="anchor", color=theme_color)

    # Turn spines off and create white grid.
    ax.spines[:].set_visible(False)

    ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im, cbar


def annotate_heatmap(im, data=None, valfmt="{x:.0f}",
                     textcolors=("black", "white"),
                     threshold=None, **textkw):
    """
    A function to annotate a heatmap.

    Parameters
    ----------
    im
        The AxesImage to be labeled.
    data
        Data used to annotate.  If None, the image's data is used.  Optional.
    valfmt
        The format of the annotations inside the heatmap.  This should either
        use the string format method, e.g. "$ {x:.2f}", or be a
        `matplotlib.ticker.Formatter`.  Optional.
    textcolors
        A pair of colors.  The first is used for values below a threshold,
        the second for those above.  Optional.
    threshold
        Value in data units according to which the colors from textcolors are
        applied.  If None (the default) uses the middle of the colormap as
        separation.  Optional.
    **kwargs
        All other arguments are forwarded to each call to `text` used to create
        the text labels.
    """

    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()

    # Normalize the threshold to the images color range.
    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(data.max())/2.

    # Set default alignment to center, but allow it to be
    # overwritten by textkw.
    kw = dict(horizontalalignment="center",
              verticalalignment="center")
    kw.update(textkw)

    # Get the formatter in case a string is supplied
    if isinstance(valfmt, str):
        valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)

    # Loop over the data and create a `Text` for each "pixel".
    # Change the text's color depending on the data.
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
            text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
            texts.append(text)

    return texts

def lire_ligne(fichier, i):
    """
    Ouvre un fichier texte et retourne la ligne i (indexée à partir de 1).
    
    Args:
        fichier (str): Le chemin vers le fichier texte.
        i (int): Le numéro de la ligne à extraire (commence à 1).
        
    Returns:
        str: Le contenu de la ligne i, ou un message d'erreur si la ligne n'existe pas.
    """
    
    try:
        with open(fichier, mode="r", encoding="utf-8") as f:
            lignes = f.readlines()  # Lire toutes les lignes
            if 1 <= i <= len(lignes):  # Vérifier que i est dans les limites
                return lignes[i - 1].strip()  # Retourner la ligne sans les espaces inutiles
            else:
                return f"La ligne {i} n'existe pas dans le fichier."
    except FileNotFoundError:
        return f"Le fichier {fichier} est introuvable."
    except Exception as e:
        return f"Une erreur est survenue : {e}"