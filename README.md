# insee-code-retriever

Ce projet contient un script en Python qui permet de récupérer pour chaque station de métro, bus et autres, le code INSEE associé et sa commune.

## Description du projet

Ce projet vise à faciliter l'obtention des codes INSEE pour les différentes stations de transport public en France. Le script récupère les informations nécessaires à partir de sources de données publiques et les associe à chaque station de métro, bus, etc.

## Installation

Pour installer ce projet, vous pouvez cloner le dépôt GitHub :

```sh
git clone https://github.com/AdeleRICHARD/insee-code-retriever.git
cd insee-code-retriever
```

## Utilisation

Pour utiliser le script, exécutez la commande suivante dans votre terminal :

```sh
python transport.py
```

Assurez-vous de personnaliser les paramètres dans le fichier `main_script.py` selon vos besoins spécifiques.

## Contribuer

Les contributions sont les bienvenues ! Pour contribuer :
1. Forkez le projet
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/NouvelleFonctionnalité`)
3. Commitez vos modifications (`git commit -m 'Ajouter nouvelle fonctionnalité'`)
4. Poussez votre branche (`git push origin feature/NouvelleFonctionnalité`)
5. Ouvrez une Pull Request

## Description du fichier 

transport.py

 contient un script Python qui permet de récupérer les informations de commune et de code INSEE pour chaque station de transport en Île-de-France. Le script utilise une combinaison de corrections manuelles et d'appels à une API pour obtenir ces informations.

### Fonctionnalités principales

1. **Chargement des données** :
   - Chargement d'un fichier CSV contenant les stations de transport (

Transports_IDF.csv

).
   - Ajout de colonnes pour la commune et le code INSEE.

2. **Nettoyage des noms de stations** :
   - Fonction [`clean_station_name`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fadele%2FfigaroStack%2Fscripts%2Ftransport.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A461%2C%22character%22%3A4%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fadele%2FfigaroStack%2Fscripts%2Ftransport.ipynb%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A539%2C%22character%22%3A13%7D%7D%5D%2C%22c5164c3f-f934-4215-9445-81fc219c1e32%22%5D "Go to definition") pour nettoyer les noms de stations en supprimant les caractères invisibles.

3. **Corrections manuelles** :
   - Dictionnaire [`manual_corrections`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fadele%2FfigaroStack%2Fscripts%2Ftransport.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A6%2C%22character%22%3A0%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fadele%2FfigaroStack%2Fscripts%2Ftransport.ipynb%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A542%2C%22character%22%3A68%7D%7D%5D%2C%22c5164c3f-f934-4215-9445-81fc219c1e32%22%5D "Go to definition") contenant les correspondances manuelles pour les stations manquantes.

4. **Appels à l'API** :
   - Utilisation d'une clé API pour appeler l'API SNCF et récupérer les informations de commune et de code INSEE.
   - Si l'API ne retourne pas de résultat, utilisation des corrections manuelles si disponibles.

5. **Mise à jour des données** :
   - Mise à jour des colonnes du DataFrame avec les informations récupérées.
   - Sauvegarde du fichier mis à jour sous le nom [`Transports_IDF_commune_insee.csv`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fadele%2FfigaroStack%2Fscripts%2Ftransport.ipynb%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A571%2C%22character%22%3A20%7D%7D%5D%2C%22c5164c3f-f934-4215-9445-81fc219c1e32%22%5D "Go to definition").

### Exemple d'utilisation

```python
# Charger le fichier CSV
df = pd.read_csv('Transports_IDF.csv')

# Nettoyer les noms de stations
df['nom_iv'] = df['nom_iv'].apply(clean_station_name)

# Récupérer les informations via l'API et les corrections manuelles
for index, row in df.iterrows():
    station_name = row['nom_iv']
    transport_mode = row['mode']
    commune, insee = get_commune_from_station_sncg(station_name, api_key, transport_mode)
    if not commune or not insee:
        if station_name in manual_corrections:
            commune, insee = manual_corrections[station_name]
    df.at[index, 'Commune'] = commune
    df.at[index, 'INSEE'] = insee

# Sauvegarder le fichier mis à jour
df.to_csv('Transports_IDF_commune_insee.csv', index=False)
```

Pour plus de détails, consultez le fichier 

transport.py