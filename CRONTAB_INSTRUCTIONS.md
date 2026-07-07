# Instructions pour la mise en place du cronjob de réentraînement

Ce document explique comment automatiser le réentraînement hebdomadaire du modèle d'analyse de sentiments.

## 1. Rendre le script exécutable

Avant de planifier la tâche, assurez-vous que le script shell a les droits d'exécution :

```bash
chmod +x retrain_cron.sh
```

## 2. Configurer la tâche planifiée (crontab)

Éditez la table de tâches planifiées de l'utilisateur courant :

```bash
crontab -e
```

Ajoutez la ligne suivante à la fin du fichier pour exécuter le réentraînement chaque dimanche à 3h00 du matin.
**Important :** Cron s'exécute dans un environnement minimal. Vous devez fournir la variable `DATABASE_URL` pour que le script puisse se connecter à la base de données en production.

```cron
# Définissez vos accès à la base de données avant l'exécution du script
0 3 * * 0 DATABASE_URL="mysql+pymysql://utilisateur:motdepasse@hote:3306/sentiscope" /bin/bash /chemin/vers/Sentiscope/retrain_cron.sh >> /chemin/vers/Sentiscope/retrain.log 2>&1
```

*Note : N'oubliez pas d'adapter la chaîne de connexion `DATABASE_URL` ainsi que le chemin `/chemin/vers/Sentiscope` selon la configuration de votre serveur de production.*
