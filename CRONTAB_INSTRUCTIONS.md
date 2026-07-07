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

Ajoutez la ligne suivante à la fin du fichier pour exécuter le réentraînement chaque dimanche à 3h00 du matin :

```cron
0 3 * * 0 /bin/bash /chemin/vers/Sentiscope/retrain_cron.sh >> /chemin/vers/Sentiscope/retrain.log 2>&1
```

*Note : N'oubliez pas de remplacer `/chemin/vers/Sentiscope` par le chemin absolu vers la racine de votre dépôt sur le serveur.*
