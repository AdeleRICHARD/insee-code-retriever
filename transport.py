import os
import requests
import pandas as pd
from requests.auth import HTTPBasicAuth

# Dictionnaire des correspondances manuelles pour les stations manquantes
manual_corrections = {
    "Orly 4": ("Orly", "94310"),
    "Orly 1-2-3": ("Orly", "94310"),
    "Gare du Nord": ("Paris", "75010"),
    "Arts et Métiers": ("Paris", "75003"),
    "Dugommier": ("Paris", "75012"),
    "Buttes-Chaumont": ("Paris", "75019"),
    "Cambronne": ("Paris", "75015"),
    "Carrefour Pleyel": ("Saint-Denis", "93066"),
    "Champs-Élysées – Clemenceau": ("Paris", "75008"),
    "Concorde": ("Paris", "75008"),
    "Gabriel Péri": ("Gennevilliers", "92036"),
    "Faidherbe Chaligny": ("Paris", "75011"),
    "Falguière": ("Paris", "75015"),
    "Michel Ange-Auteuil": ("Paris", "75016"),
    "Les Gobelins": ("Paris", "75013"),
    "Pasteur": ("Paris", "75015"),
    "Notre-Dame-de-Lorette": ("Paris", "75009"),
    "Opéra": ("Paris", "75009"),
    "Porte de Montreuil": ("Paris", "75020"),
    "Strasbourg-Saint-Denis": ("Paris", "75010"),
    "Sully-Morland": ("Paris", "75004"),
    "Télégraphe": ("Paris", "75020"),
    "Porte d'Ivry": ("Paris", "75013"),
    "Quai de la Gare": ("Paris", "75013"),
    "Quatre Septembre": ("Paris", "75002"),
    "Montparnasse-Bienvenüe": ("Paris", "75015"),
    "Funiculaire Montmartre Station Basse": ("Paris", "75018"),
    "Ménilmontant": ("Paris", "75020"),
    "Montgallet": ("Paris", "75012"),
    "Mairie de Montreuil": ("Montreuil", "93048"),
    "Porte de Bagnolet": ("Paris", "75020"),
    "Villejuif - Léo Lagrange": ("Villejuif", "94076"),
    "Corentin Celton": ("Issy-les-Moulineaux", "92040"),
    "Quai de la Rapée": ("Paris", "75012"),
    "Cosmonautes": ("Saint-Denis", "93066"),
    "Meudon-sur-Seine": ("Meudon", "92048"),
    "Brancion": ("Paris", "75015"),
    "Poterne des Peupliers": ("Paris", "75013"),
    "Les Mobiles": ("Paris", "75020"),
    "Mairie de Villeneuve-la-Garenne": ("Villeneuve-la-Garenne", "92078"),
    "Le Luth": ("Gennevilliers", "92036"),
    "Pont de Bezons": ("Bezons", "95063"),
    "Jacques Prévert": ("Aubervilliers", "93001"),
    "Watteau - Rondenay": ("Nanterre", "92050"),
    "Verdun Hoche": ("Colombes", "92025"),
    "Carle-Darthe": ("Suresnes", "92073"),
    "Pavé Blanc": ("Clamart", "92023"),
    "Drancy-Avenir": ("Drancy", "93029"),
    "Parc André Malraux": ("Nanterre", "92050"),
    "Cimetière Parisien d'Ivry": ("Ivry-sur-Seine", "94041"),
    "Crimée": ("Paris", "75019"),
    "Charenton-Écoles": ("Charenton-le-Pont", "94018"),
    "Créteil - Pointe du Lac": ("Créteil", "94028"),
    "Bonne Nouvelle": ("Paris", "75010"),
    "Petit-Châtenay": ("Châtenay-Malabry", "92019"),
    "Théâtre La Piscine": ("Châtenay-Malabry", "92019"),
    "Anny Flore": ("Bobigny", "93008"),
    "Serge Gainsbourg": ("Saint-Denis", "93066"),
    "Coteaux Beauclair": ("Montreuil", "93048"),
    "Luxembourg": ("Paris", "75005"),
    "Havre-Caumartin": ("Paris", "75009"),
    "Pablo Neruda": ("Stains", "93072"),
    "Créteil–L’Échat": ("Créteil", "94028"),
    "Campo Formio": ("Paris", "75013"),
    "Guy Môquet": ("Paris", "75017"),
    "La Motte Picquet-Grenelle": ("Paris", "75015"),
    "Place de Clichy": ("Paris", "75017"),
    "Stalingrad": ("Paris", "75019"),
    "Grands Boulevards": ("Paris", "75009"),
    "Richelieu-Drouot": ("Paris", "75009"),
    "Basilique de Saint-Denis": ("Saint-Denis", "93066"),
    "Square Sainte-Odile": ("Paris", "75017"),
    "Hôpital Bicêtre": ("Le Kremlin-Bicêtre", "94043"),
    "Botzaris": ("Paris", "75019"),
    "Rue des Boulets": ("Paris", "75011"),
    "Avenue Émile Zola": ("Paris", "75015"),
    "Danube": ("Paris", "75019"),
    "Dupleix": ("Paris", "75015"),
    "Charles Michels": ("Paris", "75015"),
    "Jasmin": ("Paris", "75016"),
    "Malakoff - Rue Étienne Dolet": ("Malakoff", "92046"),
    "Michel Ange-Molitor": ("Paris", "75016"),
    "Mirabeau": ("Paris", "75016"),
    "Miromesnil": ("Paris", "75008"),
    "Liège": ("Paris", "75009"),
    "Mouton-Duvernet": ("Paris", "75014"),
    "Porte de Vanves": ("Paris", "75014"),
    "Rambuteau": ("Paris", "75004"),
    "Rue de la Pompe": ("Paris", "75016"),
    "Saint-Georges": ("Paris", "75009"),
    "Villejuif - Louis Aragon": ("Villejuif", "94076"),
    "Front Populaire": ("Aubervilliers", "93001"),
    "Porte de la Chapelle": ("Paris", "75018"),
    "Assemblée Nationale": ("Paris", "75007"),
    "La Courneuve 8 Mai 1945": ("La Courneuve", "93027"),
    "Malakoff - Plateau de Vanves": ("Malakoff", "92046"),
    "Porte de Champerret": ("Paris", "75017"),
    "Tolbiac": ("Paris", "75013"),
    "Gaston Roulaud": ("Montreuil", "93048"),
    "Hôpital Delafontaine": ("Saint-Denis", "93066"),
    "Jean Rostand": ("Vitry-sur-Seine", "94081"),
    "Stade Charléty": ("Paris", "75013"),
    "Stade Géo André": ("Issy-les-Moulineaux", "92040"),
    "Lacépède": ("Paris", "75013"),
    "Chemin des Reniers": ("Clichy", "92024"),
    "Charlebourg": ("La Garenne-Colombes", "92035"),
    "Victor Basch": ("Issy-les-Moulineaux", "92040"),
    "Montempoivre": ("Paris", "75012"),
    "Maryse Bastié": ("Paris", "75013"),
    "Hôpital Robert Debré": ("Paris", "75019"),
    "Butte du Chapeau Rouge": ("Paris", "75019"),
    "Ella Fitzgerald": ("Paris", "75019"),
    "Suzanne Valadon": ("Paris", "75018"),
    "Guynemer": ("Paris", "75006"),
    "Division Leclerc": ("Villejuif", "94076"),
    "Meudon-la-Forêt": ("Meudon", "92048"),
    "Jean Vilar": ("Vitry-sur-Seine", "94081"),
    "Diane Arbus": ("Paris", "75013"),
    "Porte d'Asnières": ("Paris", "75017"),
    "Beethoven - Concorde": ("Paris", "75008"),
    "Petit Noisy": ("Noisy-le-Grand", "93051"),
    "Dewoitine": ("Colombes", "92025"),
    "Boucicaut": ("Paris", "75015"),
    "Bréguet-Sabin": ("Paris", "75011"),
    "Bir-Hakeim": ("Paris", "75015"),
    "Aubervilliers Pantin - Quatre Chemins": ("Aubervilliers", "93001"),
    "Daumesnil": ("Paris", "75012"),
    "École Vétérinaire de Maisons-Alfort": ("Maisons-Alfort", "94046"),
    "Église d'Auteuil": ("Paris", "75016"),
    "Franklin D. Roosevelt": ("Paris", "75008"),
    "Jacques Bonsergent": ("Paris", "75010"),
    "Maubert-Mutualité": ("Paris", "75005"),
    "Lamarck-Caulaincourt": ("Paris", "75018"),
    "Louise Michel": ("Levallois-Perret", "92044"),
    "Louvre-Rivoli": ("Paris", "75001"),
    "Pyramides": ("Paris", "75001"),
    "Robespierre": ("Montreuil", "93048"),
    "Vavin": ("Paris", "75006"),
    "Villejuif Paul Vaillant-Couturier": ("Villejuif", "94076"),
    "Porte de Clignancourt": ("Paris", "75018"),
    "Maisons-Alfort-Stade": ("Maisons-Alfort", "94046"),
    "Pont de Levallois": ("Levallois-Perret", "92044"),
    "Porte de Vincennes": ("Paris", "75012"),
    "Edgar Quinet": ("Paris", "75014"),
    "Maisons-Alfort-Les Juilliottes": ("Maisons-Alfort", "94046"),
    "Parc de Saint-Cloud": ("Saint-Cloud", "92064"),
    "Blumenthal": ("Levallois-Perret", "92044"),
    "Gilbert Bonnemaison": ("Gennevilliers", "92036"),
    "Jacqueline Auriol": ("Paris", "75015"),
    "Butte Pinson": ("Pierrefitte-sur-Seine", "93059"),
    "Baudelaire": ("Clichy-sous-Bois", "93014"),
    "Hélène Boucher": ("Le Bourget", "93013"),
    "Camille Groult": ("Vitry-sur-Seine", "94081"),
    "Constant Coquelin": ("Bagnolet", "93006"),
    "Orly - Gaston Viens": ("Orly", "94310"),
    "Hôpital Avicenne": ("Bobigny", "93008"),
    "Six Routes": ("La Courneuve", "93027"),
    "Cluny-La Sorbonne": ("Paris", "75005"),
    "Terminal 2 - Gare TGV": ("Roissy-en-France", "95527"),
    "Havre-Caumartin": ("Paris", "75009"),
    "Auguste Perret": ("Issy-les-Moulineaux", "92040"),
    "Javel - André Citroën": ("Paris", "75015"),
    "Chaussée d'Antin - La Fayette": ("Paris", "75009"),
    "École Militaire": ("Paris", "75007"),
    "Alcide d'Orbigny": ("Meudon", "92048"),
    "Germaine Tailleferre": ("Paris", "75019"),
    "Hôpital Béclère": ("Clamart", "92023"),
    "Parc des Sports": ("Choisy-le-Roi", "94022"),
    "Anna de Noailles": ("Clichy-sous-Bois", "93014"),
    "La Dhuys": ("Montfermeil", "93048"),
    "Olympiades": ("Paris", "75013"),
    "Boulogne - Jean Jaurès": ("Boulogne-Billancourt", "92012"),
    "Bolivar": ("Paris", "75019"),
    "Anatole France": ("Levallois-Perret", "92044"),
    "Barbès-Rochechouart": ("Paris", "75018"),
    "Créteil–Préfecture": ("Créteil", "94028"),
    "Cardinal Lemoine": ("Paris", "75005"),
    "Glacière": ("Paris", "75013"),
    "Jules Joffrin": ("Paris", "75018"),
    "Marcadet-Poissonniers": ("Paris", "75018"),
    "Michel Bizot": ("Paris", "75012"),
    "Le Kremlin-Bicêtre": ("Le Kremlin-Bicêtre", "94043"),
    "Ledru Rollin": ("Paris", "75011"),
    "Palais Royal - Musée du Louvre": ("Paris", "75001"),
    "Pernety": ("Paris", "75014"),
    "Picpus": ("Paris", "75012"),
    "Oberkampf": ("Paris", "75011"),
    "Saint-Philippe du Roule": ("Paris", "75008"),
    "Richard Lenoir": ("Paris", "75011"),
    "Ranelagh": ("Paris", "75016"),
    "Raspail": ("Paris", "75014"),
    "Réaumur Sébastopol": ("Paris", "75002"),
    "Reuilly-Diderot": ("Paris", "75012"),
    "Montparnasse-Bienvenüe": ("Paris", "75015"),
    "Funiculaire Montmartre Station Haute": ("Paris", "75018"),
    "Trinité d'Estienne d'Orves": ("Paris", "75009"),
    "Tuileries": ("Paris", "75001"),
    "Porte de Bagnolet": ("Paris", "75020"),
    "Villejuif-Louis Aragon": ("Villejuif", "94076"),
    "Châtillon-Montrouge": ("Châtillon", "92020"),
    "Georges Brassens": ("Paris", "75015"),
    "Suresnes-Longchamp": ("Suresnes", "92073"),
    "Faubourg de l'Arche": ("Courbevoie", "92026"),
    "Parc Pierre Lagravère": ("Colombes", "92025"),
    "Domaine Chérioux": ("Vitry-sur-Seine", "94081"),
    "Robert Wagner": ("Aubervilliers", "93001"),
    "Inovel Parc Nord": ("Vélizy-Villacoublay", "78650"),
    "Paul Éluard": ("Saint-Denis", "93066"),
    "Rouget de Lisle": ("Poissy", "78498"),
    "Cimetière de Saint-Denis": ("Saint-Denis", "93066"),
    "Escadrille Normandie-Niémen": ("Le Bourget", "93013"),
    "Suzanne Lenglen": ("Issy-les-Moulineaux", "92040"),
    "Maurice Lachâtre": ("La Courneuve", "93027"),
    "La Croix-de-Berny-Fresnes": ("Antony", "92002"),
    "Terminal 3 - Roissypole": ("Roissy-en-France", "95527"),
    "Haussmann-Saint-Lazare": ("Paris", "75008"),
    "Caroline Aigle": ("Paris", "75013"),
    "Alexandre Dumas": ("Paris", "75011"),
    "Buzenval": ("Paris", "75020"),
    "Censier-Daubenton": ("Paris", "75005"),
    "Corentin Cariou": ("Paris", "75019"),
    "Esplanade de la Défense": ("Courbevoie", "92026"),
    "Adrienne Bolland": ("Bobigny", "93008"),
    "Angélique Compoint": ("Paris", "75017"),
    "Coeur d'Orly": ("Orly", "94310"),
    "Épinettes - Pouchet": ("Paris", "75017"),
    "Bagneux - Lucie Aubrac": ("Bagneux", "92007"),
    "Malabry": ("Châtenay-Malabry", "92019"),
    "Cité-Jardin": ("Suresnes", "92073"),
    "LaVallée": ("Chaville", "92022"),
    "Nanterre-Ville": ("Nanterre", "92050"),
    "Alma-Marceau": ("Paris", "75008"),
    "Colonel Fabien": ("Paris", "75010"),
    "Étienne Marcel": ("Paris", "75002"),
    "Félix Faure": ("Paris", "75015"),
    "Filles du Calvaire": ("Paris", "75011"),
    "Marcel Sembat": ("Boulogne-Billancourt", "92012"),
    "Saint-Placide": ("Paris", "75006"),
    "Simplon": ("Paris", "75018"),
    "Solférino": ("Paris", "75007"),
    "Mairie de Montrouge": ("Montrouge", "92049"),
    "Bobigny-Pantin - Raymond Queneau": ("Bobigny", "93008"),
    "Garibaldi": ("Saint-Ouen", "93070"),
    "Chardon Lagache": ("Paris", "75016"),
    "Mabillon": ("Paris", "75006"),
    "Philippe Auguste": ("Paris", "75011"),
    "Porte d'Italie": ("Paris", "75013"),
    "Auguste Delaune": ("Nanterre", "92050"),
    "Desnouettes": ("Paris", "75015"),
    "Brimborion": ("Sèvres", "92072"),
    "Jacques-Henri Lartigue": ("Boulogne-Billancourt", "92012"),
    "Henri Farman": ("Paris", "75015"),
    "Épinay-Orgemont": ("Épinay-sur-Seine", "93031"),
    "Delphine Seyrig": ("Aubervilliers", "93001"),
    "Colette Besson": ("Saint-Denis", "93066"),
    "Joncherolles": ("Villetaneuse", "93078"),
    "Roger Sémat": ("Saint-Denis", "93066"),
    "Porte de l'Essonne": ("Athis-Mons", "91027"),
    "Place de la Logistique": ("Gennevilliers", "92036"),
    "Pierre De Geyter": ("Saint-Denis", "93066"),
    "Christophe Colomb": ("Saint-Ouen", "93070"),
    "Hôpital Béclère": ("Clamart", "92023"),
    "Musée de Sèvres": ("Sèvres", "92072"),
    "Théâtre Gérard Philipe": ("Saint-Denis", "93066"),
    "Châteaudun - Barbès": ("Paris", "75009"),
    "Barbès-Rochechouart": ("Paris", "75018"),
    "Chaussée d'Antin - La Fayette": ("Paris", "75009"),
    "Convention": ("Paris", "75015"),
    "Laumière": ("Paris", "75019"),
    "Grands Boulevards": ("Paris", "75009"),
    "Basilique de Saint-Denis": ("Saint-Denis", "93066"),
    "Exelmans": ("Paris", "75016"),
    "Franklin D. Roosevelt": ("Paris", "75008"),
    "Alexandra David-Néel": ("Levallois-Perret", "92044"),
    "Honoré de Balzac": ("Colombes", "92025"),
    "Four-Peary": ("Asnières-sur-Seine", "92004"),
    "Vallée aux Loups": ("Châtenay-Malabry", "92019"),
    "Porte de Champerret": ("Paris", "75017"),
    "Chevilly - Larue": ("Chevilly-Larue", "94021"),
    "Saint-Denis – Pleyel": ("Saint-Denis", "93066"),
    "Saint-Paul": ("Paris", "75004"),
    "Auber": ("Paris", "75009"),
    "Gare du Nord": ("Paris", "75010"),
    "Antony": ("Antony", "92002"),
    "Malesherbes": ("Paris", "75008"),
    "Boulogne - Pont de Saint-Cloud": ("Boulogne-Billancourt", "92012"),
    "Alésia": ("Paris", "75014"),
    "Brochant": ("Paris", "75017"),
    "Commerce": ("Paris", "75015"),
    "La Fourche": ("Paris", "75017"),
    "Le Peletier": ("Paris", "75009"),
    "Madeleine": ("Paris", "75008"),
    "Mairie d'Ivry": ("Ivry-sur-Seine", "94041"),
    "Passy": ("Paris", "75016"),
    "Père Lachaise": ("Paris", "75020"),
    "Place des Fêtes": ("Paris", "75019"),
    "Place d'Italie": ("Paris", "75013"),
    "Pyrénées": ("Paris", "75020"),
    "Saint-Denis - Porte de Paris": ("Saint-Denis", "93066"),
    "Wagram": ("Paris", "75017"),
    "Les Courtilles": ("Asnières-sur-Seine", "92004"),
    "Porte d'Orléans": ("Paris", "75014"),
    "Kléber": ("Paris", "75016"),
    "Pré Saint-Gervais": ("Le Pré-Saint-Gervais", "93061"),
    "Rue du Bac": ("Paris", "75007"),
    "Lourmel": ("Paris", "75015"),
    "Les Flanades": ("Sarcelles", "95585"),
    "Saarinen": ("Rungis", "94065"),
    "Robert Schuman": ("Noisy-le-Grand", "93051"),
    "Louvois": ("Vélizy-Villacoublay", "78650"),
    "Porte de Charenton": ("Paris", "75012"),
    "Lochères": ("Sartrouville", "78586"),
    "Delaunay-Belleville": ("Saint-Denis", "93066"),
    "Parc PX": ("Roissy-en-France", "95527"),
    "Aimé Césaire": ("Saint-Ouen", "93070"),
    "Noveos": ("Clamart", "92023"),
    "Porte Dauphine": ("Paris", "75016"),
    "Maison Blanche": ("Paris", "75013"),
    "Orry-la-Ville-Coye-la-Forêt": ("Orry-la-Ville", "60483"),
    "Parc PR": ("Roissy-en-France", "95527"),
    "Terminal 1": ("Roissy-en-France", "95527"),
    "Avron": ("Paris", "75020"),
    "Château d'Eau": ("Paris", "75010"),
    "Balard": ("Paris", "75015"),
    "Jardin Parisien": ("Clamart", "92023"),
    "Bastille": ("Paris", "75004"),
    "Belleville": ("Paris", "75020"),
    "Château de Vincennes": ("Vincennes", "94080"),
    "Hôtel de Ville": ("Paris", "75004"),
    "Iéna": ("Paris", "75016"),
    "Jussieu": ("Paris", "75005"),
    "Odéon": ("Paris", "75006"),
    "Pont de Sèvres": ("Boulogne-Billancourt", "92012"),
    "Ségur": ("Paris", "75007"),
    "Saint-Marcel": ("Paris", "75005"),
    "Saint-Sébastien-Froissart": ("Paris", "75011"),
    "Gallieni": ("Bagnolet", "93006"),
    "Hoche": ("Pantin", "93055"),
    "Trocadéro": ("Paris", "75016"),
    "Victor Hugo": ("Paris", "75016"),
    "Poissonnière": ("Paris", "75009"),
    "Porte de la Villette": ("Paris", "75019"),
    "Jean Moulin": ("Le Kremlin-Bicêtre", "94043"),
    "Parc des Chanteraines": ("Gennevilliers", "92036"),
    "Timbaud": ("Saint-Denis", "93066"),
    "Marie de Miribel": ("Gennevilliers", "92036"),
    "Les Cholettes": ("Nanterre", "92050"),
    "Lamartine": ("Paris", "75016"),
    "L’Onde": ("Vélizy-Villacoublay", "78650"),
    "Vauban": ("Sèvres", "92072"),
    "Soleil Levant": ("Aubervilliers", "93001"),
    "Porte de Pantin": ("Paris", "75019"),
    "Georges Millandy": ("Suresnes", "92073"),
    "Bourse": ("Paris", "75002"),
    "Argentine": ("Paris", "75016"),
    "Liberté": ("Charenton-le-Pont", "94018"),
    "Nationale": ("Paris", "75013"),
    "Sentier": ("Paris", "75002"),
    "Rennes": ("Paris", "75006"),
    "Volontaires": ("Paris", "75015"),
    "Les Agnettes": ("Asnières-sur-Seine", "92004"),
    "Louis Blanc": ("Paris", "75010"),
    "Pont Neuf": ("Paris", "75001"),
    "Riquet": ("Paris", "75019"),
    "Saint-Ambroise": ("Paris", "75011"),
    "Belvédère": ("Colombes", "92025"),
    "Marché de Saint-Denis": ("Saint-Denis", "93066"),
    "Centre de Châtillon": ("Châtillon", "92020"),
    "Mail de la Plaine": ("Gennevilliers", "92036"),
    "Musée MAC VAL": ("Vitry-sur-Seine", "94081"),
    "Mairie de Vitry": ("Vitry-sur-Seine", "94081"),
    "Rose Bertin": ("Saint-Denis", "93066"),
    "La Muette": ("Paris", "75016"),
    "Chantilly-Gouvieux": ("Chantilly", "60141"),
    "Barbara": ("Montrouge", "92049"),
    "Montreuil - Hôpital": ("Montreuil", "93048"),
    "Jourdain": ("Paris", "75019"),
    "Pierre et Marie Curie": ("Ivry-sur-Seine", "94041"),
    "Notre-Dame-des-Champs": ("Paris", "75006"),
    "Pont Marie": ("Paris", "75004"),
    "Saint-Germain-des-Prés": ("Paris", "75006"),
    "Rue Saint-Maur": ("Paris", "75011"),
    "Duroc": ("Paris", "75007"),
    "Château Rouge": ("Paris", "75018"),
    "Saint-Augustin": ("Paris", "75008"),
    "Charonne": ("Paris", "75011"),
    "Le Vésinet-Centre": ("Le Vésinet", "78650"),
    "Corvisart": ("Paris", "75013"),
    "Cour Saint-Émilion": ("Paris", "75012"),
    "Gambetta": ("Paris", "75020"),
    "La Tour Maubourg": ("Paris", "75007"),
    "Pelleport": ("Paris", "75020"),
    "Abbesses": ("Paris", "75018"),
    "Saint-Sulpice": ("Paris", "75006"),
    "Saint-Mandé": ("Saint-Mandé", "94067"),
    "Voltaire": ("Paris", "75011"),
    "Paul Valéry": ("Paris", "75012"),
    "Asnières Quatre Routes": ("Asnières-sur-Seine", "92004"),
    "La Borne Blanche": ("Orry-la-Ville", "60483"),
    "Croix de Chavaux": ("Montreuil", "93048"),
    "Cadet": ("Paris", "75009"),
    "Chemin Vert": ("Paris", "75011"),
    "Les Peintres": ("Clichy", "92024"),
    "Romainville - Carnot": ("Romainville", "93063"),
}

def is_in_idf(insee_code):
    """
    Check if an INSEE code belongs to Île-de-France.
    """
    return insee_code.startswith(('75', '77', '78', '91', '92', '93', '94', '95'))

def get_commune_from_station_sncg(station_name, api_key, transport_mode):
    """
    Search for the commune of a station via the SNCF API using the API key as the username.
    
    station_name: Name of the station
    api_key: SNCF API key (used as the username)
    transport_mode: Type of transport (e.g., GL, METRO, TRAMWAY, etc.)
    """
    url = f"https://api.sncf.com/v1/coverage/sncf/places?q={station_name}"
    response = requests.get(url, auth=HTTPBasicAuth(api_key, ''))  # The password field is empty
    
    if response.status_code == 200:
        data = response.json()
        if 'places' in data and len(data['places']) > 0:
            for place in data['places']:
                if 'stop_area' in place:
                    stop_area = place['stop_area']
                    if 'administrative_regions' in stop_area:
                        admin_region = stop_area['administrative_regions'][0]
                        insee_code = admin_region['insee']
                        
                        # If it's an IDF transport, filter by INSEE code
                        if transport_mode in ['METRO', 'TRAMWAY', 'RER', 'VAL']:
                            if is_in_idf(insee_code):
                                return admin_region['name'], insee_code
                        # If it's a GL train or another type, do not filter
                        elif transport_mode == 'TRAIN':
                            return admin_region['name'], insee_code
        return None, None
    else:
        print(f"Error {response.status_code} when calling the API for {station_name}")
        return None, None
    
# Load the CSV file with the stations
csv_file_path = 'Transports_IDF.csv'  # Replace with the path to your file
df = pd.read_csv(csv_file_path)

# Add columns for the commune and the INSEE code
df['Commune'] = ''
df['INSEE'] = ''

# Function to clean station names
def clean_station_name(station_name):
    return station_name.strip().replace('\u200b', '').replace('\u00a0', '')

# Apply cleaning to all keys in the manual_corrections dictionary
manual_corrections_cleaned = {clean_station_name(k): v for k, v in manual_corrections.items()}

# Second pass: Call the API only for stations that are not filled
api_key = os.getenv("SNCF_API_KEY")
for index, row in df.iterrows():
    station_name = clean_station_name(row['nom_iv'])
    transport_mode = row['mode']  # e.g., 'METRO', 'TRAMWAY', 'GL'
    
    # Try to get data via the API with the transport mode
    commune, insee = get_commune_from_station_sncg(station_name, api_key, transport_mode)
    
    # If the API returns no result, use manual corrections if available
    if not commune or not insee:
        if station_name in manual_corrections:
            commune, insee = manual_corrections[station_name]
        else:
            print(f"No match found for {station_name}")
    
    # Update the DataFrame columns
    df.at[index, 'Commune'] = commune
    df.at[index, 'INSEE'] = insee

# Save the results to a new CSV file
df.to_csv('Transports_IDF_avec_communes_insee_last.csv', index=False)
print("File updated with communes and INSEE codes.")
