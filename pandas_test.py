import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

region = ['Azerbaijan','Bahamas', 'Bangladesh', 'Belize', 'Bhutan',
          'Cambodia', 'Cameroon', 'Cape Verde', 'Chile', 'China']   #10个

kind = ['Afforestation & reforestation', 'Biofuels', 'Biogas', 'Biomass', 'Cement']   #5个

np.random.seed(20180316)
arr_region = np.random.choice(region, size=(200,))
list_region = list(arr_region)

arr_kind = np.random.choice(kind, size=(200,))
list_kind = list(arr_kind)

values = np.random.randint(100, 200, 200)
list_values = list(values)

df = pd.DataFrame({'region':list_region,'kind': list_kind,'values':list_values})

print(df.head(10))


