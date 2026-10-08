# Plateforme de risque de crédit IA

Une solution globale d’intelligence du risque de crédit qui combine ingestion de données, ingénierie des fonctionnalités, apprentissage automatique, explicabilité et surveillance pour soutenir des décisions de prêt plus sûres.

## Vue d’ensemble

Cette plateforme est conçue pour aider les institutions financières à évaluer le risque des emprunteurs à l’aide de modèles pilotés par l’IA et d’un support décisionnel transparent. Elle peut être utilisée pour :

- noter les candidats à partir du comportement de crédit historique et des signaux financiers
- détecter la fraude et les schémas d’application anormaux
- expliquer les décisions du modèle pour des raisons de conformité et d’examen
- surveiller la performance du modèle au fil du temps
- soutenir les décisions de souscription et de gestion du risque de portefeuille

## Fonctionnalités clés

- Pipeline de données pour les demandes de crédit et les données de performance historiques
- Ingénierie des fonctionnalités pour le comportement des emprunteurs, les obligations de dette et les indicateurs de remboursement
- Entraînement de modèles pour la classification binaire et le classement du risque
- Explicabilité avec SHAP, importance des variables et analyses détaillées des décisions
- Tableau de bord et rapports pour les parties prenantes métier
- Surveillance des modèles pour la dérive, la dégradation des performances et les changements de seuils
- Déploiement prêt pour l’API et architecture évolutive

## Stack technologique

- Java et Spring Boot pour l’API métier
- React, TypeScript et Vite pour l’interface web
- Python pour le service de prédiction et l’analyse des données
- scikit-learn
- XGBoost / LightGBM
- pandas / NumPy
- Jupyter Notebook
- FastAPI pour le service ML
- Docker Compose pour lancer les services
- MLflow pour le suivi des expériences

## Structure du projet

```text
AI-Credit-Risk-Platform/
├── backend/       # API Spring Boot
├── front/         # Interface React/Vite
├── ml-service/    # API Python/FastAPI et modèle ML
├── data/          # Données préparées
├── models/        # Métadonnées et seuils du modèle
├── notebooks/
├── docker-compose.yml
├── requirements.txt
├── README.md
└── .gitignore
```

## Flux de travail typique

1. Importer les données de demande de prêt et du profil client.
2. Nettoyer et normaliser les données pour la modélisation.
3. Créer des fonctionnalités pertinentes pour le risque.
4. Entraîner et valider un modèle de risque de crédit.
5. Noter les candidats entrants.
6. Expliquer les résultats du modèle pour une revue humaine.
7. Surveiller les prédictions et réentraîner si nécessaire.

## Objectifs du modèle

La plateforme peut être configurée pour prédire :

- la probabilité de défaut (PD)
- la perte attendue (EL)
- le risque d’insolvabilité
- la segmentation client par catégorie de crédit
- la recommandation d’approbation de la demande

## Démarrage

### Prérequis

- Docker et Docker Compose
- Node.js et npm pour lancer l’interface React

### Lancer l’application

```bash
docker compose up --build
```

Dans un autre terminal, lancer l’interface web :

```bash
cd front
npm install
npm run dev
```

Vite affiche l’adresse locale à ouvrir dans le navigateur. Les requêtes `/api` sont relayées vers le backend Spring Boot sur le port `8080`.

### Comptes de démonstration

Les comptes locaux sont définis dans la configuration Spring Security :

- Agent : `agent` / `agent123`
- Responsable : `responsable` / `resp123`

Ces mots de passe sont réservés aux essais locaux. Ils doivent être remplacés avant tout déploiement accessible à d’autres personnes.

## Exemple de cas d’usage

Un prêteur peut utiliser la plateforme pour examiner le profil d’un candidat, estimer la probabilité de défaut et expliquer les facteurs de risque à l’origine de la recommandation du modèle. Le résultat peut soutenir les décisions de souscription tout en préservant la transparence et l’auditabilité.

## Considérations sur les données

- garantir la confidentialité des données et la conformité aux réglementations locales
- valider l’absence de valeurs manquantes et le déséquilibre des classes
- utiliser des découpes temporelles pour une évaluation plus réaliste
- examiner l’équité et l’explicabilité entre les segments clients

## Surveillance et gouvernance

- suivre la dérive du modèle au fil du temps
- surveiller les taux de faux positifs et de faux négatifs
- documenter les décisions de réentraînement
- maintenir le versionnage des modèles et l’historique de validation
- aligner la solution sur la gouvernance interne du risque et les normes réglementaires

## Licence

Ce projet est sous licence MIT.

## Contribution

Les contributions sont les bienvenues. Veuillez créer une branche de fonctionnalité, ajouter des tests lorsque cela est pertinent et ouvrir une demande de fusion avec un résumé clair des changements.

## Contact

Pour toute question ou opportunité de collaboration, veuillez contacter le responsable du projet.