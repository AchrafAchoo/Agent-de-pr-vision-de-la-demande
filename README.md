# Agent de prévision de la demande

Agent IA qui analyse l'historique des ventes, prévoit la demande par produit et par site, mesure sa propre erreur, s'ajuste, et explique les variations en langage naturel.

## Objectifs

- Analyser l'historique des ventes
- Intégrer la saisonnalité, les promotions et les facteurs externes
- Produire des prévisions par produit et par site
- Mesurer l'erreur et s'ajuster (backtesting + détection de drift)
- Expliquer les variations (SHAP / décomposition + LLM)

## Datasets

| Dataset | Rôle | Source |
|---|---|---|
| **M5 Forecasting (Walmart)** | Dataset principal : entraînement, évaluation, démo | [Kaggle - M5 Forecasting Accuracy](https://www.kaggle.com/competitions/m5-forecasting-accuracy) |
| **Favorita Grocery Sales** | Validation croisée : vérifier que le pipeline généralise | [Kaggle - Favorita Grocery Sales Forecasting](https://www.kaggle.com/c/favorita-grocery-sales-forecasting) |

> M5 est une *competition* Kaggle : il faut cliquer sur **Join Competition** et accepter les règles pour accéder aux données.

Alternative sans Kaggle pour M5 :

```python
from datasetsforecast.m5 import M5
Y_df, X_df, S_df = M5.load('data')
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
Modèle (LightGBM / Nixtla)
        │
        ▼
Évaluation (backtesting en fenêtre glissante)
        │
        ▼
Boucle d'ajustement (réentraînement / changement de modèle si drift)
        │
        ▼
Module d'explication (SHAP / Prophet + LLM)
```

## Modules

### 1. Loaders
Chargement de M5 et Favorita, conversion vers le format commun `unique_id, ds, y` + exogènes.

### 2. Features
- **Saisonnalité** : jour de la semaine, semaine, mois, année, jours fériés
- **Promotions** : `onpromotion` (Favorita), proxy prix (M5)
- **Facteurs externes** : événements, SNAP, prix du pétrole, transactions
- **Lags et moyennes glissantes** sur les ventes

### 3. Modèle
Prévisions par produit et par site avec LightGBM (ou modèles statistiques/ML via Nixtla).

### 4. Évaluation et ajustement
- Backtesting en fenêtre glissante
- Métriques : MAE, RMSE, sMAPE, WRMSSE (M5)
- Si l'erreur dépasse un seuil (drift) : réentraînement ou changement de modèle

### 5. Explicabilité
- SHAP sur LightGBM ou décomposition tendance/saisonnalité (Prophet)
- Un LLM transforme les résultats en explications lisibles, par exemple : *« les ventes montent de 18 % à cause de la promo et du week-end »*

## Installation

```bash
git clone <url-du-repo>
cd Agent-de-prevision-de-la-demande
pip install -r requirements.txt
```

Dépendances principales : `pandas`, `lightgbm`, `shap`, `datasetsforecast`, `statsforecast`, `prophet`.

## Structure du projet (proposée)

```
.
├── data/
├── src/
│   ├── loaders/
│   ├── features/
│   ├── models/
│   ├── evaluation/
│   └── explain/
├── notebooks/
├── requirements.txt
└── README.md
```

## Licences et sources

M5 et Favorita sont distribués via Kaggle pour un usage compétition/recherche. Projet académique : citer les sources dans le rapport.
