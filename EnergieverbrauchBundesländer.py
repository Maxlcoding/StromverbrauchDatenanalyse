import pandas as pd
import matplotlib.pyplot as plt

def convert_to_mwh(value):
    #Konvertiert einen Wert von MJ in MWh.
    if pd.notna(value):  # Prüfen, ob der Wert nicht NaN ist
        return value * 0.27778
    return value  # NaN-Werte bleiben NaN


data_Path = "data/datasetEnergieverbrauchBundesland.csv"
data = pd.read_csv(data_Path, delimiter=';', na_values='.')

# Alle Spalten anzeigen
pd.set_option('display.max_columns', None)

# Alle Zeilen anzeigen
pd.set_option('display.max_rows', None)

# Maximale Breite einer Spalte erhöhen
pd.set_option('display.width', 1000)


# 50 Hertz und BW anschauen
bundeslaenderÜNB = ['Hamburg','Baden-W�rttemberg','Berlin', 'Brandenburg', 'Mecklenburg-Vorpommern'
,'Sachsen', 'Sachsen-Anhalt', 'Th�ringen']

# 50 Hertz und BW anschauen
bundeslaender50Hertz = ['Hamburg', 'Berlin', 'Brandenburg', 'Mecklenburg-Vorpommern'
,'Sachsen', 'Sachsen-Anhalt', 'Th�ringen']

bundeslaenderGesamt = ['Hamburg','Baden-W�rttemberg','Berlin', 'Brandenburg', 'Mecklenburg-Vorpommern'
,'Sachsen', 'Sachsen-Anhalt', 'Th�ringen', 'Schleswig-Holstein', 'Niedersachsen', 'Bremen', 'Hessen', 'Rheinland-Pfalz', 'Bayern', 'Saarland', 'Nordrhein-Westfalen']

#print(data['Bundesland'])



dataEinwohner = pd.read_csv('data/EinwohnerzahlenBundeslaender.csv', delimiter=';')
dataEinwohner['Insgesamt'] = pd.to_numeric(dataEinwohner['Insgesamt'].str.replace(r"\s+", "", regex=True), errors='raise')


# Spalten
zeit_spalte_industrie = 'Jahr'
verbrauch_spalte = 'Strom (Tsd. MJ)'

# Integer Werte konvertieren
data[verbrauch_spalte] = pd.to_numeric(data[verbrauch_spalte], errors='raise')
# in MWh konvertieren
data[verbrauch_spalte] = data[verbrauch_spalte].apply(convert_to_mwh)
# Skalieren in Mio. MWh
#data[verbrauch_spalte] = data[verbrauch_spalte] / 1e6


def plotBundeslaender(data, bundeslaender, zeit_spalte, verbrauch_spalte):
    plt.figure(figsize=(10, 8))
    for bundesland in bundeslaender:
        subset = data[data['Bundesland'] == bundesland]
        plt.plot(subset[zeit_spalte], subset[verbrauch_spalte], label=bundesland)
    # Plot anpassen

    plt.title('Stromverbrauch Industrie pro Bundesland über die Jahre')
    plt.xlabel('Jahr')
    plt.ylabel('Stromverbrauch (Mio. MWh)')
    plt.legend(title='Bundesland', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

    # Plot anzeigen
    plt.show()

#plotBundeslaender(data,bundeslaenderGesamt, zeit_spalte, verbrauch_spalte)

def getSumIndustrie(data, bundeslaender50Hertz, zeit_spalte, verbrauch_spalte):
    # Filter auf die Bundesländer von 50Hertz
    filtered_data = data[data['Bundesland'].isin(bundeslaender50Hertz)]

    # Gruppieren nach Jahr und Summieren der Verbrauchswerte
    summed_data = filtered_data.groupby(zeit_spalte)[verbrauch_spalte].sum().reset_index()

    # clean data
    #summed_data = summed_data.copy()
    # Umwandlung der Zeit-Spalte in datetime und als index setzen
    #summed_data[zeit_spalte] = pd.to_datetime(summed_data[zeit_spalte], dayfirst=True, errors='raise')

    #summed_data.set_index(zeit_spalte, inplace=True)

    return summed_data


def plotSum(data, bundeslaender50Hertz, zeit_spalte, verbrauch_spalte):
    # Filter auf die Bundesländer von 50Hertz
    filtered_data = data[data['Bundesland'].isin(bundeslaender50Hertz)]
    subsetBW = data[data['Bundesland'] == 'Baden-W�rttemberg']
    #print(subsetBW)

    # Gruppieren nach Jahr und Summieren der Verbrauchswerte
    summed_data = filtered_data.groupby(zeit_spalte)[verbrauch_spalte].sum().reset_index()
    print(summed_data)

    # Plot erstellen
    plt.figure(figsize=(10, 8))
    plt.plot(summed_data[zeit_spalte], summed_data[verbrauch_spalte], marker='o', label='50Hertz')
    plt.plot(subsetBW[zeit_spalte], subsetBW[verbrauch_spalte],marker='o', label='BW')
    # Plot anpassen
    plt.title('Gesamtverbrauch Industrie der Zonen 50Hertz und TransNetBW (2017-2023')
    plt.xlabel('Jahr')
    plt.ylabel('Gesamtverbrauch (in Mio MWh)')
    plt.grid(True)
    plt.legend(title='ÜNB:', loc='upper right')
    #plt.tight_layout()
    plt.show()


#plotSum(data, bundeslaender50Hertz, zeit_spalte_industrie, verbrauch_spalte)

def correlation(dataset1, dataset2, zeit_spalte, last_spalte, zeit_spalte_industrie, verbrauch_spalte, title):
    # clean data
    dataset1 = dataset1.copy()
    # Umwandlung der Zeit-Spalte in datetime und als index setzen
    dataset1[zeit_spalte] = pd.to_datetime(dataset1[zeit_spalte], dayfirst=True, errors='raise')
    dataset1.set_index(zeit_spalte, inplace=True)
    # Umwandlung Integer
    dataset1[last_spalte] = dataset1[last_spalte].str.replace('.', '', regex=False)  # Tausendertrennzeichen entfernen
    dataset1[last_spalte] = dataset1[last_spalte].str.replace(',', '.', regex=False)  # Dezimal-Komma durch Dezimal-Punkt ersetzen
    dataset1[last_spalte] = pd.to_numeric(dataset1[last_spalte])

    # same cleaning for dataset2
    dataset2 = dataset2.copy()
    dataset2[zeit_spalte_industrie] = pd.to_datetime(dataset2[zeit_spalte_industrie].astype(str) + '-01-01', errors='raise')
    dataset2 = dataset2.sort_values(by=zeit_spalte_industrie, ascending=True)
    dataset2.set_index(zeit_spalte_industrie, inplace=True)

    dataset1[last_spalte] = dataset1[last_spalte] / 1e6
    dataset2[verbrauch_spalte] = dataset2[verbrauch_spalte] / 1e6
    print(dataset1[last_spalte])
    print(dataset2[verbrauch_spalte])

    # Korrelation berechnen
    correlation = dataset1[last_spalte].corr(dataset2[verbrauch_spalte])
    # Ergebnis anzeigen
    print(f"{title}: {correlation:.2f}")

    # Streudiagramm der Stromverbrauchswerte
    plt.figure(figsize=(10, 8))
    plt.scatter(dataset1[last_spalte], dataset2[verbrauch_spalte],  alpha=0.5, color='blue')
    plt.title(title)
    plt.xlabel("Stromverbrauch Gesamt pro Jahr (in Mio. MWh)")
    plt.ylabel("Stromverbrauch Industrie pro Jahr (in Mio. MWh)")
    plt.grid(True)
    plt.show()


### Korrelation
dataPath50Hertz = 'data/Realisierter_Stromverbrauch_2017-2023_Jahr_50Hertz.csv'
dataPathBW = 'data/Realisierter_Stromverbrauch_2017-2023_Jahr_TransNetBW.csv'
data50Hertz = pd.read_csv(dataPath50Hertz, delimiter=';')
dataBW = pd.read_csv(dataPathBW, delimiter=';')
zeit_spalte = 'Datum von'
last_spalte = 'Gesamt (Netzlast) [MWh] Berechnete Auflösungen'


# Industrie Jahreswert 50Hertz
data_Industrie50Hertz = getSumIndustrie(data, bundeslaender50Hertz, zeit_spalte_industrie, verbrauch_spalte)

# Industrie Jahreswert TransNetBW
subsetBW = data[data['Bundesland'] == 'Baden-W�rttemberg'].reset_index()
print(subsetBW)

# Korrelation berechnen und plotten
correlation(data50Hertz, data_Industrie50Hertz, zeit_spalte, last_spalte, zeit_spalte_industrie, verbrauch_spalte, "Korrelation des Jahresstromverbrauchs zwischen 50Hertz und Industrie")
correlation(dataBW, subsetBW, zeit_spalte, last_spalte, zeit_spalte_industrie, verbrauch_spalte, "Korrelation des Jahresstromverbrauchs zwischen TransNetBW und Industrie")

### Anteil des Industriestromverbrauchs an Gesamt

def quotaIndustrie(dataset1, dataset2, zeit_spalte, last_spalte, zeit_spalte_industrie, verbrauch_spalte):
    # clean data
    dataset1 = dataset1.copy()
    # Umwandlung der Zeit-Spalte in datetime und als index setzen
    dataset1[zeit_spalte] = pd.to_datetime(dataset1[zeit_spalte], dayfirst=True, errors='raise')
    dataset1.set_index(zeit_spalte, inplace=True)
    # Umwandlung Integer
    dataset1[last_spalte] = dataset1[last_spalte].str.replace('.', '', regex=False)  # Tausendertrennzeichen entfernen
    dataset1[last_spalte] = dataset1[last_spalte].str.replace(',', '.', regex=False)  # Dezimal-Komma durch Dezimal-Punkt ersetzen
    dataset1[last_spalte] = pd.to_numeric(dataset1[last_spalte])

    # same cleaning for dataset2
    dataset2 = dataset2.copy()
    dataset2[zeit_spalte_industrie] = pd.to_datetime(dataset2[zeit_spalte_industrie].astype(str) + '-01-01', errors='raise')
    dataset2 = dataset2.sort_values(by=zeit_spalte_industrie, ascending=True)
    dataset2.set_index(zeit_spalte_industrie, inplace=True)

    print(dataset1[last_spalte])
    print(dataset2[verbrauch_spalte])

    dataset1['Anteil Industriestromverbrauch'] = dataset2[verbrauch_spalte] / dataset1[last_spalte]

    return dataset1


dataAnteilIndustrieBW = quotaIndustrie(dataBW, subsetBW, zeit_spalte, last_spalte, zeit_spalte_industrie, verbrauch_spalte)
dataAnteilIndustrie50Hertz = quotaIndustrie(data50Hertz, data_Industrie50Hertz, zeit_spalte, last_spalte, zeit_spalte_industrie, verbrauch_spalte)



# Diagramm der Stromverbrauchswerte
plt.figure(figsize=(10, 8))
plt.plot(dataAnteilIndustrieBW.index, dataAnteilIndustrieBW['Anteil Industriestromverbrauch'], color='blue',
         label='Anteil Industriestromverbrauch TransNetBW')
plt.plot(dataAnteilIndustrie50Hertz.index, dataAnteilIndustrie50Hertz['Anteil Industriestromverbrauch'], color='red',
         label='Anteil Industriestromverbrauch 50Hertz')
# Diagrammtitel und Achsenbeschriftungen
plt.title("Anteil Industriestromverbrauch in den Regelzonen")
plt.xlabel('Jahr')
plt.ylabel('Anteil des Industriestromverbrauchs')

# Raster und Legende
plt.grid(True)
plt.legend()

# Diagramm anzeigen
plt.tight_layout()
plt.show()



