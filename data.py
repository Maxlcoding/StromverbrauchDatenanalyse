import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

"""matplotlib.use("MacOSX")


#plt.use('TkAgg')  # Stabileres Backend für macOS
# Alle Spalten anzeigen
pd.set_option('display.max_columns', None)

# Alle Zeilen anzeigen
# pd.set_option('display.max_rows', None)

# Maximale Breite einer Spalte erhöhen
pd.set_option('display.width', 1000)
"""
dataPath = "Realisierter_Stromverbrauch_2019-2024_50Hertz.csv"

data = pd.read_csv(dataPath, delimiter=';')

target_column = 'Gesamt (Netzlast) [MWh] Originalauflösungen'
# Prüfen, ob ungültige Werte (NaN) existieren
missing_values = data[target_column].isnull().sum()
print(f"Fehlende Werte in der Spalte '{target_column}': {missing_values}")

# Ungültige Werte entfernen (optional, wenn sie vorhanden sind)
data = data.dropna(subset=[target_column])
# Sicherstellen, dass alle Strings bereinigt werden
data[target_column] = data[target_column].str.replace('.', '', regex=False)  # Tausendertrennzeichen entfernen
data[target_column] = data[target_column].str.replace(',', '.', regex=False)  # Dezimal-Komma durch Dezimal-Punkt ersetzen


#print(data.head())
print(data.columns)
data[target_column] = pd.to_numeric(data[target_column])


varianz = data[target_column].var()
print(f"Die Varianz der Netzlast beträgt: {varianz}")

std = data[target_column].std()
print(f"Die Standartabweichung der Netzlast beträgt: {std}")

# Größten Wert in der Zielspalte anzeigen
max_value = data[target_column].max()

print(f"Der größte Wert in der Spalte {target_column} ist: {max_value}")

# Sicherstellen, dass die Zeitspalte im Datumsformat ist
#print(data.dtypes)  # Zeigt den Datentyp der Spalten
#print(data.head())  # Zeigt die ersten Zeilen der DataFrame
#print(data[['Datum von', 'Gesamt (Netzlast) [MWh] Originalauflösungen']].isnull().sum())  # Zählt Fehlwerte in relevanten Spalten


#print(data.head())
#print(data.columns)

#sampled_data = data[::100]
#filtered_data = data[(data['Datum von'] >= '2019-01-01 00:00') & (data['Datum von'] <= '2019-01-31 00:00')]

"""
zeit_spalte = "Datum von"
last_spalte = "Gesamt (Netzlast) [MWh] Berechnete Auflösungen"

# Umwandlung der Zeit-Spalte in datetime, zur Sicherheit
#data[zeit_spalte] = pd.to_datetime(data[zeit_spalte])

# Plot erstellen
#plt.figure(figsize=(12, 6))  # Größe des Plots festlegen
plt.plot(data[zeit_spalte], data[last_spalte], label="Gesamtlast Strom", color='blue')

# Achsentitel und Plot-Titel
plt.xlabel("Zeit (Datum von)")
plt.ylabel("Gesamtlast Strom (in MWh)")  # Einheit anpassen, falls bekannt
plt.title("Gesamtlast Strom über die Zeit")

# Legende und Gitter
#plt.legend()
#plt.grid()
# Plot anzeigen
plt.show()
"""
# TO DO Varianz, Standartabweichung, Variationskoeffizent Zusammenhänge: Kovarianz/Korrelation