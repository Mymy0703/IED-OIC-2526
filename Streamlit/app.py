# *******************************************************
# Nom .......... : app.py
# Rôle ......... : Édition de métadonnées EXIF et 
#                  géolocalisation d'une image sur carte via Streamlit
# Auteur ....... : Maryam Joyez
# Version ...... : V0.1
# Compilation .. : Aucune compilation nécessaire
# Usage .........: streamlit run app.py
# *******************************************************

# -------------------------------------------------------
# Fonction d'édition de métadonnées EXIF d'une image et 
# géolocalisation de cette image via Streamlit
# -------------------------------------------------------
# Import des bibliothèques
from PIL import Image, ExifTags
import streamlit as st
import piexif
from geopy.geocoders import Nominatim

# Configuration du titre de l'application
st.title("Streamlit : Édition de métadonnées EXIF")

# Chemin d'accès de l'image
image_path = "Streamlit/mnemosyne.jpeg"

try:
    # Ouverture de l'image avec Pillow
    image = Image.open(image_path)
    st.subheader("Photo ajoutée")
    # Affichage de l'image originale dans Streamlit
    st.image(image, caption="Photo de Mnémosyne")
except FileNotFoundError:
    # Gestion d'erreur
    st.error(f"L'image '{image_path}' est introuvable.")
    st.stop()

# Création du formulaire Streamlit
st.subheader("Formulaire d'édition des métadonnées EXIF")

with st.form("exif_form"):
    # Champs de texte permettant à l'utilisateur de saisir de nouvelles valeurs EXIF
    auteur = st.text_input("Auteur")
    description = st.text_input("Description de l'image")
    logiciel = st.text_input("Logiciel utilisé")
    date_heure = st.text_input("Date et heure")
    
    # Bouton pour valider et soumettre le formulaire
    valider = st.form_submit_button("Mise à jour des métadonnées")

    # Action lors de la validation du formulaire
    if valider:
        try:
            # Récupération des métadonnées EXIF de l'image grâce à getexif()
            exif_data = image.getexif()
            
            # Si l'objet EXIF est vide, on en récupère un nouveau
            if exif_data is None:
                exif_data = image.getexif()

            # Association des balises EXIF standards à l'aide de leurs identifiants
            if auteur:
                exif_data[315] = auteur
            if description:
                exif_data[270] = description
            if logiciel:
                exif_data[305] = logiciel
            if date_heure:
                exif_data[306] = date_heure

            # Chemin de sauvegarde pour la nouvelle image modifiée
            output_path = "mnemosyne_1.jpg"
            # Enregistrement de l'image en incluant les nouveaux EXIF modifiés
            image.save(output_path, exif=exif_data)

            # Affichage d'un message de l'image mise à jour
            st.success("Métadonnées EXIF modifiées et enregistrées avec succès !")
            st.image(output_path, caption="Image avec EXIF mis à jour")

        except Exception as e:
            # Gestion des erreurs
            st.error(f"Une erreur est survenue : {e}")
            
# Extraction de coordonnées GPS
st.title("Localisation de la photo")

try:
    # Extraction des coordonnées GPS de l'image grâce à piexif
    exif_dict = piexif.load(image_path)
    gps = exif_dict["GPS"]
    
    # On récupère les degrés, minutes et secondes pour la latitude et la longitude
    lat_d = gps[piexif.GPSIFD.GPSLatitude][0][0] / gps[piexif.GPSIFD.GPSLatitude][0][1]
    lat_m = gps[piexif.GPSIFD.GPSLatitude][1][0] / gps[piexif.GPSIFD.GPSLatitude][1][1]
    lat_s = gps[piexif.GPSIFD.GPSLatitude][2][0] / gps[piexif.GPSIFD.GPSLatitude][2][1]
    
    lon_d = gps[piexif.GPSIFD.GPSLongitude][0][0] / gps[piexif.GPSIFD.GPSLongitude][0][1]
    lon_m = gps[piexif.GPSIFD.GPSLongitude][1][0] / gps[piexif.GPSIFD.GPSLongitude][1][1]
    lon_s = gps[piexif.GPSIFD.GPSLongitude][2][0] / gps[piexif.GPSIFD.GPSLongitude][2][1]

    # Conversion en degrés décimaux précis
    lat = lat_d + (lat_m / 60.0) + (lat_s / 3600.0)
    lon = lon_d + (lon_m / 60.0) + (lon_s / 3600.0)

    if gps[piexif.GPSIFD.GPSLatitudeRef] == b'S': lat = -lat
    if gps[piexif.GPSIFD.GPSLongitudeRef] == b'W': lon = -lon

    # Trouver le pays via les coordonnées de l'image
    geolocator = Nominatim(user_agent="geo_app")
    location = geolocator.reverse(f"{lat}, {lon}", language="fr")
    # Extraction du nom du pays, "Inconnu" par défaut si non trouvé
    pays = location.raw['address'].get('country', 'Inconnu') if location else "Inconnu"

    # Affichage dans Streamlit
    st.success(f"Pays identifié : **{pays}**")
    st.info(f"Coordonnées : Latitude {lat}, Longitude {lon}")
    
    # Affichage de la carte
    st.map({"lat": [lat], "lon": [lon]})

except Exception as e:
    # Gestion d'erreurs
    st.error(f"Erreur ou données GPS introuvables : {e}")



import pandas as pd
import pydeck as pdk

st.title("Mes voyages et destinations de rêve")

# Définition des points (POIs) avec leurs coordonnées et couleurs (Vert pour visité, Orange pour rêve)
data_points = [
    {"lieu": "Pays-Bas", "lat": 52.3676, "lon": 4.9041, "couleur": [0, 200, 0]},      # Vert
    {"lieu": "Maroc (Marrakech)", "lat": 31.6295, "lon": -7.9811, "couleur": [0, 200, 0]}, # Vert
    {"lieu": "Tunisie (Djerba)", "lat": 33.8076, "lon": 10.8451, "couleur": [0, 200, 0]}, # Vert
    {"lieu": "Malaisie", "lat": 3.1390, "lon": 101.6869, "couleur": [255, 165, 0]},      # Orange
    {"lieu": "Chine", "lat": 39.9042, "lon": 116.4074, "couleur": [255, 165, 0]},         # Orange
    {"lieu": "Corée du Sud", "lat": 37.5665, "lon": 126.9780, "couleur": [255, 165, 0]}   # Orange
]
df_points = pd.DataFrame(data_points)

# Définition des liaisons d'un point vers le suivant
data_lines = [
    {"from_lon": 4.9041, "from_lat": 52.3676, "to_lon": -7.9811, "to_lat": 31.6295},
    {"from_lon": -7.9811, "from_lat": 31.6295, "to_lon": 10.8451, "to_lat": 33.8076},
    {"from_lon": 10.8451, "from_lat": 33.8076, "to_lon": 101.6869, "to_lat": 3.1390},
    {"from_lon": 101.6869, "from_lat": 3.1390, "to_lon": 116.4074, "to_lat": 39.9042},
    {"from_lon": 116.4074, "from_lat": 39.9042, "to_lon": 126.9780, "to_lat": 37.5665}
]
df_lines = pd.DataFrame(data_lines)

# Configuration de la vue globale de la carte
view_state = pdk.ViewState(latitude=30.0, longitude=30.0, zoom=1, pitch=0)

# Couche pour tracer les lignes entre les points
layer_lines = pdk.Layer(
    "LineLayer",
    df_lines,
    get_source_position="[from_lon, from_lat]",
    get_target_position="[to_lon, to_lat]",
    get_color=[150, 150, 150, 180], # Lignes grises semi-transparentes
    get_width=3,
)

# Couche pour afficher les POIs colorés
layer_points = pdk.Layer(
    "ScatterplotLayer",
    df_points,
    get_position="[lon, lat]",
    get_color="couleur",
    get_radius=300000,
    pickable=True,
)

# Affichage de la carte interactive finale
st.pydeck_chart(pdk.Deck(
    layers=[layer_lines, layer_points], 
    initial_view_state=view_state, 
    tooltip={"text": "{lieu}"}
))
