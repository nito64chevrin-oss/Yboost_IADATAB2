# Météo & Cinéma — Prédire la fréquentation des salles

Ce projet vise à mesurer et à prédire la fréquentation des salles de cinéma en France en fonction de la **météo** et de la **période de l'année** (mois, vacances scolaires, jours fériés).

---

## Objectifs

L'objectif principal est d'estimer l'influence de la météo et du calendrier sur le nombre d'entrées en salle. Concrètement, l'outil doit permettre de :

- **Prédire le démarrage d'un film** selon la météo et la date de sortie ;
- **Analyser l'effet de la météo par genre** : par exemple, une comédie attire-t-elle moins de spectateurs qu'un film d'animation lorsqu'il pleut ?
- **Prévoir le nombre de billets vendus** à court terme.

---

## Sources de données

| Source | Contenu | Provenance |
|---|---|---|
| **Météo-France** | Données météorologiques (températures, précipitations) | [data.gouv.fr](https://www.data.gouv.fr) |
| **CNC** (Centre national du cinéma et de l'image animée) | Entrées mensuelles au cinéma | [data.gouv.fr](https://www.data.gouv.fr) |
| **Calendrier social** | Vacances scolaires et jours fériés | [data.gouv.fr](https://www.data.gouv.fr) |

Toutes les données utilisées sont **open source**.

---

## Fonctionnalités

- **Zone de prédiction interactive** : choix de la zone géographique, des conditions météo et de la date.
- **Pages explicatives** : présentation des méthodes utilisées, accompagnée de graphiques pour chaque jeu de données, séparément puis croisés.
- **Export des résultats** : possibilité de télécharger les prédictions effectuées.

---

## Méthodologie

### Étape 1 — Créer un indice météo national pondéré

La météo n'est pas la même à Lille et à Marseille. L'idée est donc de calculer une moyenne nationale des précipitations et des températures, **pondérée par le poids cinématographique de chaque région**. L'Île-de-France, par exemple, représente une part bien plus importante des entrées nationales que les autres régions.

### Étape 2 — Modéliser la saisonnalité de base

Avant d'étudier l'effet de la météo, il faut modéliser la fréquentation « normale » en fonction :

- du mois ;
- des vacances scolaires et jours fériés ;
- de l'attractivité des films à l'affiche.

### Étape 3 — Analyser les résidus au regard de la météo

On compare ensuite l'**écart entre la fréquentation prévue et la fréquentation réelle** avec les **anomalies météorologiques**, par exemple un mois de juillet anormalement pluvieux par rapport aux normales de saison.

### Étape 4 — Développer un outil de simulation

Une interface interactive permet à un gérant de cinéma de saisir :

- les prévisions météo à 7 jours ;
- les films à l'affiche.

L'outil renvoie alors une **estimation de la fréquentation** ainsi que des **conseils d'ajustement** (nombre de séances à programmer, stock de confiserie, etc.).