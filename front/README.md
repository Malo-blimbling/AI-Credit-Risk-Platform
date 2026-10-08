# Frontend React

Le client React/Vite consomme le backend Spring Boot via `/api`. En développement, Vite relaie ces requêtes vers `http://localhost:8080`.

## Démarrage

Lancer le backend et le service ML depuis la racine du projet :

```sh
docker compose up --build
```

Dans un autre terminal :

```sh
cd front
npm install
npm run dev
```

Ouvrir l’URL Vite affichée dans le terminal, puis se connecter avec un compte backend. Les métriques sont réservées au rôle Responsable ; l’historique est disponible aux utilisateurs authentifiés.

L’historique backend est actuellement conservé en mémoire et est donc réinitialisé au redémarrage du service.
