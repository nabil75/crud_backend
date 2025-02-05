
# Import other requirements
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt

# Import pandas profiling library
import ydata_profiling as pp

import pkg_resources

# Import Iris Dataset
df_iris = pd.read_csv('./Iris.csv')

# To check if the dataset is imported successfully
df_iris.info()

# Geneate  Report and save for later use
pp.ProfileReport(df_iris, title="Pandas Profiling Report").to_file("report.html")