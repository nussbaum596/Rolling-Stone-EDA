import pandas as pd
import numpy as np

#Importing scraped data to clean
list_top500_2020 = pd.read_csv('list_top500_2020.csv')

#Splitting Album Title and Artist
list_top500_2020[['Artist', 'Album_Title']] = list_top500_2020['Album'].str.split(", '", expand=True)

#Removing Old Album Variable and Renaming Album_Title to Album
list_top500_2020 = list_top500_2020.drop('Album', axis=1)
list_top500_2020 = list_top500_2020.rename(columns = {'Album_Title':'Album'})

#Removing the leftover quote on the end for the album titles
list_top500_2020['Album'] = list_top500_2020['Album'].map(lambda x: str(x)[:-1])

#Splitting Record Label and Release Year
list_top500_2020[['Label','Year']] =list_top500_2020['Subtitle'].str.split(", ", expand=True)

#Removing Subtitle Variable
list_top500_2020 = list_top500_2020.drop('Subtitle', axis=1)

#Changing Order of variables (Just to make it easier to work with)
list_top500_2020 = list_top500_2020[['Rank', 'Album', 'Artist', 'Year', 'Label', 'Description']]

#Converting Year and Rank to  numeric variables
list_top500_2020['Year'] = pd.to_numeric(list_top500_2020['Year'])
list_top500_2020['Rank'] = pd.to_numeric(list_top500_2020['Rank'])

#Fixing Year for Brian Eno's 'Another Green World'
list_top500_2020['Year'] = list_top500_2020['Year'].replace(19755, 1975)

##Adding a decades column
conditions = [
    list_top500_2020['Year'] < 1960,
    (list_top500_2020['Year']  >= 1960) & (list_top500_2020['Year'] < 1970),
    (list_top500_2020['Year']  >= 1970) & (list_top500_2020['Year'] < 1980),
    (list_top500_2020['Year']  >= 1980) & (list_top500_2020['Year'] < 1990),
    (list_top500_2020['Year']  >= 1990) & (list_top500_2020['Year'] < 2000),
    (list_top500_2020['Year']  >= 2000) & (list_top500_2020['Year'] < 2010),
    list_top500_2020['Year'] >= 2010
    ]

decade = ['1950s', '1960s', '1970s', '1980s', '1990s', '2000s', '2010s']

list_top500_2020['Decade'] = np.select(conditions, decade)

#Creating CSV file of cleaned data
list_top500_2020.to_csv('list_top500_2020_clean.csv')