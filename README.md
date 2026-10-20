# Boucle Son — serveur + app

Colle un lien TikTok/Instagram → le serveur récupère le son, la miniature et le nom → l'app le met en playlist, avec effets et boucle.

## Lancer en local (test)
    pip install -r requirements.txt     # + ffmpeg installé sur ta machine
    APP_KEY=monmotdepasse python server.py
Ouvre http://localhost:8080

## Mettre en ligne (pour l'utiliser sur ton téléphone)
1. Mets ce dossier sur un dépôt GitHub (privé).
2. Sur Render, Railway ou Fly.io : « New Web Service » depuis ce dépôt (il détecte le Dockerfile).
3. Ajoute la variable d'environnement APP_KEY (ton mot de passe). Sans elle, n'importe qui peut utiliser ton serveur.
4. Ouvre l'adresse https obtenue sur ton téléphone, puis « Ajouter à l'écran d'accueil ».
   La première fois, l'app te demande la clé d'accès.

## À savoir
- TikTok et Instagram changent souvent : si les liens cessent de marcher, redéploie pour mettre yt-dlp à jour.
- Instagram bloque souvent les serveurs : si besoin, exporte tes cookies dans un fichier cookies.txt à la racine du projet.
- Limite : sons de moins de 15 minutes. Usage personnel uniquement, respecte les droits des créateurs.

## Fonctions de l'app
Interface meikilab : disque vinyle, visualiseur, couleurs adaptées à la miniature, flèches précédent/suivant. Import par lien (un ou plusieurs liens collés d'un coup, bouton 📋), miniatures, noms et artistes, playlists, favoris ♥, recherche, aléatoire, boucle (un son / la liste), minuterie de sommeil, effets (vitesse, reverb, basses, 8D, préréglages slowed/speed up/nightcore), renommer, changer de playlist, lecteur plein écran avec barre de progression, lecture écran verrouillé.
APP_KEY est facultative : sans elle, l'app ne demande aucune clé.
