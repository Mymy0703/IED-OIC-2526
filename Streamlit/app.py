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
    
    lat = gps[piexif.GPSIFD.GPSLatitude][0][0] / gps[piexif.GPSIFD.GPSLatitude][0][1]
    lon = gps[piexif.GPSIFD.GPSLongitude][0][0] / gps[piexif.GPSIFD.GPSLongitude][0][1]
    
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
