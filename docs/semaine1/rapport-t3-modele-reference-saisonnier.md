# T3 — Modèle de référence saisonnier

## Objectif

Implémenter une prévision de référence pour F1 et disposer de métriques
comparables pour F2. Le critère de T3 est une prévision sur 28 jours pour
20 séries.

## Ce qui a été fait

Le modèle saisonnier hebdomadaire reprend les ventes des 7 derniers jours
observés et répète ce cycle pour produire les valeurs futures. Par exemple,
la prévision du prochain lundi reprend la dernière vente du lundi observé.
Cette méthode ne nécessite pas d'entraînement et sert de référence pour
comparer les futurs modèles.

Le module [`seasonal_naive.py`](../../src/models/seasonal_naive.py) fournit :

- `seasonal_naive_forecast` : une prévision par série, avec les colonnes
  `unique_id`, `ds` et `y_hat` ;
- `backtest_seasonal_naive` : un backtest qui garde les 28 dernières
  observations de chaque série hors de l'historique utilisé pour prévoir ;
- `evaluate_forecast` : le calcul des métriques MAE, RMSE et sMAPE.

Le script [`run_seasonal_baseline.py`](../../scripts/run_seasonal_baseline.py)
charge 20 séries M5 par défaut, calcule le backtest, puis produit une prévision
future de 28 jours. Le résultat est exporté en CSV.

## Exécution

Depuis la racine du dépôt :

```powershell
python scripts/run_seasonal_baseline.py
```

Le fichier généré par défaut est
[`m5_seasonal_naive_forecast.csv`](../../data/m5_seasonal_naive_forecast.csv).
Les options `--max-series` et `--output` permettent de choisir le nombre de
séries et le chemin de sortie.

## Résultats de vérification

À l'exécution sur les 20 séries M5 :

- 560 prévisions générées (20 séries × 28 jours) ;
- dates prédites : du 20 juin au 17 juillet 2016 ;
- MAE : **1,8143** ;
- RMSE : **4,0231** ;
- sMAPE : **94,2827 %**.

Ces métriques proviennent d'un backtest sur les 28 dernières observations
connues de chaque série. Le calcul du sMAPE traite une journée où la valeur
observée et la prévision sont toutes deux nulles comme une erreur nulle.

Les tests ciblés se trouvent dans
[`test_seasonal_naive.py`](../../tests/test_seasonal_naive.py) : les 4 tests
passent. Ils vérifient la répétition du cycle hebdomadaire, le découpage du
backtest, les métriques lorsque les ventes sont nulles et le rejet d'une série
avec moins d'une semaine d'historique.
