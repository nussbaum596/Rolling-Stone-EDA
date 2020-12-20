import pandas as pd
import numpy as np

#Importing scraped data to clean
list_top500_2003 = pd.read_csv('list_top500_2003.csv')

#Splitting Album Title and Artist
list_top500_2003[['Artist', 'Album_Title']] = list_top500_2003['Album'].str.split(", '", expand=True)

#Removing Old Album Variable and Renaming Album_Title to Album
list_top500_2003 = list_top500_2003.drop('Album', axis=1)
list_top500_2003 = list_top500_2003.rename(columns = {'Album_Title':'Album'})

#Removing the leftover quote on the end for the album titles
list_top500_2003['Album'] = list_top500_2003['Album'].map(lambda x: str(x)[:-1])

##There were a few instances where the ", '" wasn't spaced appropriately so the album title appeared null. I will just fix those manually
#Rank 487 ('She's So Unusal' by Cyndi Lauper)
list_top500_2003 = list_top500_2003.set_index('Rank')
list_top500_2003.loc['487','Artist'] = 'Cyndi Lauper'
list_top500_2003.loc['487','Album'] = '''She's So Unusual'''

#Rank 169 ('Exodus' by Bob Marley and the Wailers)
list_top500_2003.loc['169','Artist'] = 'Bob Marley and the Wailers'
list_top500_2003.loc['169','Album'] = 'Exodus'

list_top500_2003 = list_top500_2003.reset_index()

#Splitting Label, Year, and Description
list_top500_2003['Label'] = list_top500_2003['Description'].str.split(",", expand=True)[0]
list_top500_2003['Year'] = list_top500_2003['Description'].str.extract(", (.*?)\n", expand=True)[0]
list_top500_2003['Description_2'] = list_top500_2003['Description'].str.split("\n", expand=True)[1]

list_top500_2003 = list_top500_2003.drop('Description', axis=1)
list_top500_2003 = list_top500_2003.rename(columns = {'Description_2':'Description'})


#Changing Order of variables (Just to make it easier to work with)
list_top500_2003 = list_top500_2003[['Rank', 'Album', 'Artist', 'Year', 'Label', 'Description']]

#Converting Year and Rank to  numeric variables
list_top500_2003['Year'] = pd.to_numeric(list_top500_2003['Year'])
list_top500_2003['Rank'] = pd.to_numeric(list_top500_2003['Rank'])


##Adding a decades column
conditions = [
    list_top500_2003['Year'] < 1960,
    (list_top500_2003['Year']  >= 1960) & (list_top500_2003['Year'] < 1970),
    (list_top500_2003['Year']  >= 1970) & (list_top500_2003['Year'] < 1980),
    (list_top500_2003['Year']  >= 1980) & (list_top500_2003['Year'] < 1990),
    (list_top500_2003['Year']  >= 1990) & (list_top500_2003['Year'] < 2000),
    (list_top500_2003['Year']  >= 2000) & (list_top500_2003['Year'] < 2010),
    list_top500_2003['Year'] >= 2010
    ]

decade = ['1950s', '1960s', '1970s', '1980s', '1990s', '2000s', '2010s']

list_top500_2003['Decade'] = np.select(conditions, decade)

#Creating CSV file of cleaned data
list_top500_2003.to_csv('list_top500_2003_clean.csv')