# Import des bibliothèques
from PIL import Image, ExifTags
import streamlit as st

# Titre de l'application
st.title("Streamlit : Édition de métadonnées EXIF")

# Chargement de l'image
image_path = "mnemosyne.png"

try:
    # Ouverture de l'image avec Pillow
    image = Image.open(image_path)
    st.subheader("Photo ajoutée")
    # Affichage de l'image dans Streamlit
    st.image(image, caption="Photo de Mnémosyne")
except FileNotFoundError:
    # Gestion de l'erreur
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

    if valider:
        try:
            # Récupération des métadonnées EXIF actuelles de l'image via getexif()
            exif_data = image.getexif()
            
            # Si l'objet EXIF est vide, on en récupère un nouveau
            if exif_data is None:
                exif_data = image.getexif()

            # Modification des tags EXIF à l'aide de leurs identifiants numériques :
            # 315 correspond au tag de l'artiste (Artist)
            # 270 correspond au tag de la description (ImageDescription)
            # 305 correspond au tag du logiciel (Software)
            # 306 correspond au tag de la date et l'heure (DateTime)
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
            # Gestion des erreurs survenant pendant la manipulation ou l'enregistrement des EXIF
            st.error(f"Une erreur est survenue : {e}")
