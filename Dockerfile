# Utiliser une image de base avec Python
FROM python:3.8

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers nécessaires dans le conteneur
COPY . /app

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port sur lequel l'application Flask s'exécute
EXPOSE 5000

# Définir l'environnement de production
ENV FLASK_ENV=production

# Commande pour démarrer l'application Flask
CMD ["python", "app.py"]
