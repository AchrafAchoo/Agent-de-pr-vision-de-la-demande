# Agent de prévision de la demande

Agent IA qui analyse l'historique des ventes, prévoit la demande par produit et par site, mesure sa propre erreur, s'ajuste, et explique les variations en langage naturel.

## Objectifs

- Analyser l'historique des ventes
- Intégrer la saisonnalité, les promotions et les facteurs externes
- Produire des prévisions par produit et par site
- Mesurer l'erreur et s'ajuster (backtesting + détection de drift)
- Expliquer les variations (SHAP / décomposition + LLM)
- Exposer le tout via une API et une interface utilisateur

## Datasets

| Dataset | Rôle | Source |
|---|---|---|
| **M5 Forecasting (Walmart)** | Dataset principal : entraînement, évaluation, démo | [Kaggle - M5 Forecasting Accuracy](https://www.kaggle.com/competitions/m5-forecasting-accuracy) |
| **Favorita Grocery Sales** | Validation croisée : vérifier que le pipeline généralise | [Kaggle - Favorita Grocery Sales Forecasting](https://www.kaggle.com/c/favorita-grocery-sales-forecasting) |

> M5 est une *competition* Kaggle : il faut cliquer sur **Join Competition** et accepter les règles pour accéder aux données.

Le chargement complet M5 peut demander plusieurs Go de RAM. Le script charge
par défaut un échantillon de 500 séries, en filtrant avant la conversion en
format long :

```bash
python scripts/load_m5.py
python scripts/load_m5.py --max-series 1000
```

Pour charger tout le dataset (utiliser une machine avec suffisamment de mémoire) :

```bash
python scripts/load_m5.py --all
```

### Couverture des besoins

| Besoin | M5 | Favorita |
|---|---|---|
| Historique des ventes | `sales_train_evaluation.csv` | `train.csv` |
| Saisonnalité | `calendar.csv` (jour, semaine, mois, année) | dates + `holidays_events.csv` |
| Promotions | pas de flag, dérivé de `sell_prices.csv` | `onpromotion` |
| Facteurs externes | événements, SNAP | prix du pétrole, jours fériés, `transactions.csv` |
| Produit × site | `item_id` × `store_id` | `family` × `store_nbr` |

### Remarques

- Les deux datasets ont des schémas différents : on **ne les fusionne pas**. Une couche d'abstraction les ramène au même format (`unique_id`, `ds`, `y` + colonnes exogènes), et l'agent tourne sur l'un ou l'autre sans changer de code.
- Promotion M5 (proxy) : `prix_actuel / prix_moyen_item < 0.95`.

## Architecture

```
Loader (M5 / Favorita)
        │
        ▼
Format commun (unique_id, ds, y, exogènes)
        │
        ▼
Feature engineering (saisonnalité, promo, exogènes, lags)
        │
        ▼
Modèle (LightGBM / Nixtla)  ──►  models/ (artefacts sauvegardés)
        │
        ▼
Évaluation (backtesting en fenêtre glissante)
        │
        ▼
Boucle d'ajustement (réentraînement / changement de modèle si drift)
        │
        ▼
Module d'explication (SHAP / Prophet + LLM)
        │
        ▼
API (api/)  ──►  Interface utilisateur (ui/)
```

## Structure du projet

```
.
├── api/            # API REST : endpoints de prévision, d'évaluation et d'explication
├── data/           # Données brutes et transformées (non versionnées, voir .gitignore)
├── src/            # Code métier du pipeline
│   ├── loaders/        # Chargement M5 / Favorita -> format commun
│   ├── features/       # Feature engineering
│   ├── models/         # Entraînement et inférence
│   ├── evaluation/     # Backtesting, métriques, détection de drift
│   ├── explain/        # SHAP / décomposition + génération d'explications LLM
│   └── agent/          # Orchestration de l'agent (outils, boucle d'ajustement)
├── docs/           # Documentation, schémas d'architecture, rapport
├── models/         # Modèles entraînés et artefacts (non versionnés)
├── notebooks/      # Exploration et prototypage
├── scripts/        # Scripts utilitaires (chargement des données, entraînement, backtest)
├── tests/          # Tests unitaires et d'intégration
├── ui/             # Interface utilisateur
├── requirements.txt
├── .gitignore
└── README.md
```

## Modules

### 1. Loaders (`src/loaders/`)
Chargement de M5 et Favorita, conversion vers le format commun `unique_id, ds, y` + exogènes.

### 2. Features (`src/features/`)
- **Saisonnalité** : jour de la semaine, semaine, mois, année, jours fériés
- **Promotions** : `onpromotion` (Favorita), proxy prix (M5)
- **Facteurs externes** : événements, SNAP, prix du pétrole, transactions
- **Lags et moyennes glissantes** sur les ventes

### 3. Modèle (`src/models/`)
Prévisions par produit et par site avec LightGBM (ou modèles statistiques/ML via Nixtla). Les modèles entraînés sont sauvegardés dans `models/`.

### 4. Évaluation et ajustement (`src/evaluation/`)
- Backtesting en fenêtre glissante
- Métriques : MAE, RMSE, sMAPE, WRMSSE (M5)
- Si l'erreur dépasse un seuil (drift) : réentraînement ou changement de modèle

### 5. Explicabilité (`src/explain/`)
- SHAP sur LightGBM ou décomposition tendance/saisonnalité (Prophet)
- Un LLM transforme les résultats en explications lisibles, par exemple : *« les ventes montent de 18 % à cause de la promo et du week-end »*

### 6. API (`api/`)
Expose le pipeline : demande de prévision par produit/site, métriques d'erreur, explications.

### 7. Interface (`ui/`)
Interface permettant de visualiser les prévisions, l'erreur et les explications.

## Installation

```bash
git clone <url-du-repo>
cd Agent-de-prevision-de-la-demande
pip install -r requirements.txt
```

Dépendances principales : `pandas`, `lightgbm`, `shap`, `datasetsforecast`, `statsforecast`, `prophet`.

## Utilisation

Charger les données M5 (première exécution : téléchargement, puis cache dans `data/`) :

```bash
python scripts/load_m5.py
```

## Tests

```bash
pytest tests/
```

## Licences et sources

M5 et Favorita sont distribués via Kaggle pour un usage compétition/recherche. Projet académique : citer les sources dans le rapport.