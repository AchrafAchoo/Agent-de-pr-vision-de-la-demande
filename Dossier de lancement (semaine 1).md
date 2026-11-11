# Dossier de lancement (semaine 1)

Nov 9, 2026 · @Larhlimi

## Mode d'emploi

La semaine 1 est décisive : sur un projet de 4 semaines, un cadrage flou ou des données indisponibles ne se rattrapent pas. Ce dossier permet à l'enseignant de valider, faire reprendre ou refuser le projet sous 48 heures.

Le dossier comporte quatre livrables. **L'équipe se les répartit : chaque membre rédige seul le ou les livrables dont il est responsable, puis un autre membre le relit.** Le nom du rédacteur et du relecteur figure en tête de chaque livrable ; c'est une preuve de contribution pour la note individuelle.

**Répartition selon la taille de l'équipe**

| Taille       | Membre A                                    | Membre B                 | Membre C    | Membre D                    |
| ------------ | ------------------------------------------- | ------------------------ | ----------- | --------------------------- |
| 2 étudiants | 1. Descriptif + 3. Maquette                 | 2. Dataset + 4. Pipeline |             |                             |
| 3 étudiants | 1. Descriptif + 4. Pipeline (consolidation) | 2. Dataset               | 3. Maquette |                             |
| 4 étudiants | 1. Descriptif                               | 2. Dataset               | 3. Maquette | 4. Pipeline (consolidation) |

Le pipeline des tâches (livrable 4) est consolidé par un seul membre, mais **chaque membre y ajoute lui-même ses propres tâches**.

**Notre répartition**

| Livrable                | Rédacteur       | Relecteur        | Fichier dans le dépôt                           |
| ----------------------- | ---------------- | ---------------- | ------------------------------------------------- |
| 1. Descriptif du projet | Amine El Alouani | Achraf Alla      | `docs/semaine1/1-descriptif.md`                 |
| 2. Dataset              | Achraf Alla      | Amine El Alouani | `docs/semaine1/2-dataset.md` + `data/sample/` |
| 3. Maquette globale     | Amine El Alouani | Achraf Alla      | `maquette.md` + `docs/semaine1/img/`          |
| 4. Pipeline des tâches | Achraf Alla      | Amine El Alouani | `docs/semaine1/4-pipeline.md`                   |

**Circuit GitHub**

1. Le coordinateur crée le dossier `docs/semaine1/` avec un `README.md` qui reprend le tableau « Notre répartition ».
2. Chaque rédacteur copie la section de son livrable dans le fichier indiqué, travaille sur sa propre branche (`semaine1/dataset`, par exemple) et ouvre une pull request.
3. Le relecteur vérifie les critères d'acceptation du livrable, commente dans la pull request, puis l'approuve.
4. Une pull request n'est fusionnée qu'après approbation. Les quatre livrables sont fusionnés sur la branche principale avant la date limite.
5. Le coordinateur pose l'étiquette `semaine1-remis` sur le dernier commit et en informe l'enseignant.

Remplacez chaque `[à compléter]` par vos réponses. Les exemples en italique viennent du projet n° 1 du catalogue (agent de recherche documentaire) ; supprimez-les dans votre version. Le dossier rempli tient sur 4 à 6 pages, maquettes comprises.

## Livrable 1 : descriptif du projet mis à jour

Rédacteur : \[à compléter\]   Relecteur : \[à compléter\]   Fichier : `docs/semaine1/1-descriptif.md`

Le descriptif adapte la fiche du catalogue à votre version du projet. Il doit pouvoir être lu seul par quelqu'un qui ne connaît pas le catalogue.

**1.1 Contexte et problème** (5 lignes au plus) : quel problème métier, pour qui, comment on fait aujourd'hui sans l'agent. \[à compléter\]

**1.2 Objectif** en une phrase : \[à compléter\]

**1.3 Utilisateurs cibles et scénario d'usage principal** : qui utilise l'agent et ce qu'il fait, étape par étape. \[à compléter\]

**1.4 Fonctionnalités du MVP** (2 à 3 pour un binôme, 3 à 4 pour un trinôme, 4 à 5 pour une équipe de 4)

| N° | Fonctionnalité   | Ce que l'utilisateur voit ou obtient | Priorité (indispensable, souhaitable) |
| --- | ----------------- | ------------------------------------ | -------------------------------------- |
| F1  | \[à compléter\] | \[à compléter\]                    |                                        |
| F2  | \[à compléter\] | \[à compléter\]                    |                                        |
| F3  |                   |                                      |                                        |
| F4  |                   |                                      |                                        |
| F5  |                   |                                      |                                        |

**1.5 Services et composants techniques**

| Service ou composant                                | Rôle dans le projet | Technologie choisie    | Pourquoi ce choix |
| --------------------------------------------------- | -------------------- | ---------------------- | ----------------- |
| Modèle (LLM ou ML)                                 |                      |                        |                   |
| Recherche ou mémoire (RAG, base vectorielle, SGBD) |                      |                        |                   |
| Outils appelés par l'agent                         |                      |                        |                   |
| API                                                 |                      | FastAPI                |                   |
| Interface                                           |                      |                        |                   |
| Conteneur et intégration continue                  |                      | Docker, GitHub Actions |                   |

**1.6 Hors périmètre** (ce que vous ne ferez pas) : \[à compléter\]

**1.7 Écart avec la fiche du catalogue** : ce que vous ajoutez, retirez ou modifiez, et pourquoi. \[à compléter ou « aucun »\]

*Exemple : les ingénieurs d'un bureau d'études cherchent à la main dans 40 normes internes en PDF. Objectif : obtenir en moins de 10 secondes une réponse citée. F1 ingestion et recherche, F2 réponse avec citations, F3 interface Streamlit. Hors périmètre : documents scannés, gestion des droits.*

**Critères d'acceptation (vérifiés par le relecteur)**

- [ ] Le problème et l'utilisateur sont compréhensibles sans le catalogue.
- [ ] Le nombre de fonctionnalités correspond à la taille de l'équipe.
- [ ] Chaque fonctionnalité est démontrable (pas de formulation vague comme « améliorer »).
- [ ] Chaque composant technique a une justification d'une ligne.
- [ ] Le hors périmètre est rempli.

## Livrable 2 : dataset

Rédacteur : \[à compléter\]   Relecteur : \[à compléter\]   Fichiers : `docs/semaine1/2-dataset.md` + `data/sample/`

Sans données utilisables dès la semaine 1, le projet ne peut pas tenir en 4 semaines. **Un échantillon réel doit déjà être dans le dépôt** (quelques fichiers ou une centaine de lignes, moins de 10 Mo). Les données complètes volumineuses ne vont pas dans Git : indiquez où elles se trouvent.

**2.1 Description**

| Rubrique                                                                  | Réponse                          |
| ------------------------------------------------------------------------- | --------------------------------- |
| Nom et source (lien)                                                      | \[à compléter\]                 |
| Producteur ou propriétaire                                               | \[à compléter\]                 |
| Volume (nombre de fichiers, lignes, pages, taille)                        | \[à compléter\]                 |
| Format et structure (PDF, CSV, JSON, logs, images ; colonnes principales) | \[à compléter\]                 |
| Langue et période couverte                                               | \[à compléter\]                 |
| Licence et droits d'usage                                                 | \[à compléter\]                 |
| Données personnelles ou sensibles, et traitement prévu                  | \[à compléter ou « aucune »\] |
| Emplacement des données complètes                                       | \[à compléter\]                 |

**2.2 Qualité constatée sur l'échantillon** : valeurs manquantes, doublons, bruit, documents illisibles, déséquilibre. \[à compléter\]

**2.3 Justification** : pour chaque fonctionnalité du livrable 1, expliquez en une ligne en quoi ces données permettent de la réaliser.

| Fonctionnalité | Données utilisées | En quoi elles suffisent |
| --------------- | ------------------- | ----------------------- |
| F1              |                     |                         |
| F2              |                     |                         |
| F3              |                     |                         |

**2.4 Alternative de repli** : si la source principale devient inaccessible ou se révèle inutilisable, quelle autre source (jeu public, données simulées ou générées) et ce que vous perdez en l'utilisant. \[à compléter\]

**2.5 Jeu de test** : comment vous mesurerez la qualité de l'agent. Taille (au moins 20 cas), origine, réponses attendues rédigées par qui. \[à compléter\]

*Exemple : 40 articles scientifiques en accès libre (licence CC BY), environ 600 pages PDF, en français et en anglais, aucune donnée personnelle ; 5 PDF dans `data/sample/`. Repli : résumés arXiv en anglais seulement. Jeu de test : 20 questions avec réponses et passages attendus, rédigées par l'équipe.*

**Critères d'acceptation (vérifiés par le relecteur)**

- [ ] L'échantillon est dans `data/sample/` et s'ouvre sans erreur.
- [ ] La licence autorise l'usage dans un projet de cours.
- [ ] Les données personnelles éventuelles sont anonymisées ou remplacées par des données fictives.
- [ ] Chaque fonctionnalité du MVP est couverte par la justification.
- [ ] L'alternative de repli est réellement accessible (lien vérifié).
- [ ] Le jeu de test est défini, même partiellement rédigé.

## Livrable 3 : maquette globale

Rédacteur : \[à compléter\]   Relecteur : \[à compléter\]   Fichiers : `docs/semaine1/3-maquette.md` + `docs/semaine1/img/`

La maquette comporte deux vues : l'architecture (comment le système fonctionne) et les écrans (ce que voit l'utilisateur).

**3.1 Schéma d'architecture.** Montrez les composants du livrable 1, les flux de données et le parcours d'une requête de l'utilisateur jusqu'à la réponse. Pour une équipe de 4, montrez aussi les agents ou sous-systèmes et leurs échanges. Écrivez-le en Mermaid dans le fichier Markdown (GitHub l'affiche directement) ou déposez une image dans `img/`.

Modèle à adapter (exemple du projet n° 1) :

```mermaid
flowchart LR
Rédacteur : Amine El Alouani   Relecteur : Achraf Alla   Fichier : `docs/semaine1/1-descriptif.md`
    UI -->|question| API[API FastAPI /ask]
    API --> R[Recherche vectorielle]
**1.1 Contexte et problème** (5 lignes au plus) : un responsable approvisionnement doit anticiper les ventes de chaque article dans chaque magasin pour éviter les ruptures et le surstock. Sans l'agent, il consulte l'historique et applique des estimations manuelles, difficiles à comparer et à justifier. Les effets du calendrier, des prix et des événements sont donc pris en compte de manière inégale.
    R --> DB[(Base vectorielle)]
    ING[Ingestion des PDF] --> DB
**1.2 Objectif** en une phrase : produire une prévision de demande à 28 jours par article et magasin, accompagnée d'une mesure d'erreur et d'une explication lisible des principales variations.
    R -->|passages| LLM[LLM]
    LLM -->|réponse + citations| API
**1.3 Utilisateurs cibles et scénario d'usage principal** : le responsable approvisionnement sélectionne un magasin, un article et un horizon de 7 ou 28 jours. Il lance la prévision, consulte la courbe de demande attendue et les indicateurs d'erreur issus du backtesting, puis ouvre l'explication pour identifier les facteurs associés à la variation. Il peut enfin télécharger le résultat au format CSV.
    API --> UI
```

| F1  | Prévoir la demande | Prévision à 7 ou 28 jours pour un article et un magasin sélectionnés | indispensable |
| F2  | Évaluer la fiabilité | MAE, RMSE et sMAPE sur une fenêtre de backtesting | indispensable |
| F3  | Expliquer la variation | Facteurs principaux affichés en langage naturel à partir des variables du modèle | indispensable |
| F4  | Exporter le résultat | Tableau CSV de la prévision et des indicateurs associés | souhaitable |
| F5  |                   |                                      |                                        |
| ----------------- | ------------------- | --------------------------- | ---------------------------------- |
| \[à compléter\] |                     |                             |                                    |
**1.6 Hors périmètre** (ce que vous ne ferez pas) : optimisation automatique des commandes, connexion à un ERP ou à des données temps réel, prévision probabiliste avec intervalle de confiance, gestion des droits utilisateurs, entraînement sur plusieurs pays et génération d'explications libres sans variables mesurées.
| \[à compléter\] |                     |                             |                                    |
|                   |                     |                             |                                    |
**1.7 Écart avec la fiche du catalogue** : le projet est recentré sur le dataset M5 et un horizon de 28 jours. La boucle de changement automatique de modèle et la validation complète sur Favorita sont des objectifs secondaires ; elles pourront être ajoutées après le MVP si les prévisions et l'API sont stabilisées.

**3.4 Parcours utilisateur** : enchaînement des écrans pour le scénario principal du livrable 1 (écran A, action, écran B...). \[à compléter\]
Rédacteur : Achraf Alla   Relecteur : Amine El Alouani   Fichiers : `docs/semaine1/2-dataset.md` + `data/m5/datasets/`
**Critères d'acceptation (vérifiés par le relecteur)**

| Nom et source (lien)                                                      | M5 Forecasting Accuracy, [Kaggle](https://www.kaggle.com/competitions/m5-forecasting-accuracy) |
- [ ] Chaque composant du livrable 1 apparaît dans le schéma, et inversement.
- [ ] Le parcours d'une requête se suit de bout en bout sur le schéma.
- [ ] Chaque fonctionnalité du MVP est visible sur au moins un écran.
- [ ] Le schéma s'affiche correctement sur GitHub (Mermaid valide ou image présente).
- [ ] Pour une équipe de 4 : les agents ou sous-systèmes et leurs échanges sont représentés.

## Livrable 4 : pipeline des tâches prévues

Consolidateur : \[à compléter\]   Relecteur : \[à compléter\]   Fichier : `docs/semaine1/4-pipeline.md`
**2.2 Qualité constatée sur l'échantillon** : les valeurs de ventes sont majoritairement des comptes entiers, avec beaucoup de zéros pour les séries peu vendues. Le calendrier contient des valeurs manquantes pour les jours sans événement, et les prix ne sont pas disponibles pour toutes les combinaisons article-semaine. Aucun doublon évident n'est attendu dans les clés article-magasin-jour ; ces contrôles seront automatisés à l'ingestion. Le jeu est déséquilibré entre articles et magasins.

Le pipeline découpe le projet en tâches de 1 à 2 jours. **Chaque membre saisit lui-même ses tâches** ; le consolidateur vérifie les dépendances et l'équilibre de la charge. Les tâches sont aussi créées comme issues GitHub (ou dans un tableau GitHub Projects) pour être suivies dans le rapport hebdomadaire.
**2.4 Alternative de repli** : le jeu public Favorita Grocery Sales Forecasting ([Kaggle](https://www.kaggle.com/competitions/favorita-grocery-sales-forecasting)) reprend les ventes par magasin et produit, avec une variable de promotion explicite. À défaut d'accès à Kaggle, nous générerons un petit jeu synthétique avec saisonnalité hebdomadaire et promotions. Dans les deux cas, nous perdrons la comparaison WRMSSE officielle M5 et une partie de la structure hiérarchique.

**4.1 Liste des tâches**
Rédacteur : Amine El Alouani   Relecteur : Achraf Alla   Fichiers : `docs/semaine1/3-maquette.md` + `docs/semaine1/img/`
| ID | Tâche            | Fonctionnalité | Responsable | Dépend de | Semaine | Terminée quand ? (critère vérifiable) |
| -- | ----------------- | --------------- | ----------- | ---------- | ------- | ---------------------------------------- |
| T1 | \[à compléter\] |                 |             |            | 1       |                                          |
    U[Responsable approvisionnement] --> UI[Interface Streamlit]
    UI -->|article, magasin, horizon| API[API FastAPI]
    API --> PREV[Service de prévision]
    ING[Ingestion M5] --> DATA[(CSV / Parquet)]
    DATA --> FE[Features : lags, calendrier, prix]
    FE --> MOD[LightGBM / Nixtla]
    MOD --> PREV
    PREV --> EVAL[Backtesting et métriques]
    PREV --> SHAP[Contributions SHAP]
    EVAL --> API
    SHAP --> EXPL[Explication en langage naturel]
    EXPL --> API
    API -->|prévision, métriques, explication| UI
*Exemple : T3, « Indexer les 40 PDF dans la base vectorielle », F1, membre B, dépend de T1, semaine 2, terminée quand une requête de test renvoie les 5 passages les plus proches en moins de 2 s.*

**4.2 Jalons hebdomadaires** (repris de la fiche de cadrage)
**3.2 Légende du schéma** : l'interface et l'API servent F1 et F4 ; l'ingestion et le stockage préparent les données de F1 à F3 ; le module de features et le modèle produisent F1 ; le backtesting sert F2 ; SHAP et l'explication servent F3.

| Semaine | Jalon démontrable                                  | Tâches qui y mènent |
**3.4 Parcours utilisateur** : écran Sélection → choix de l'article, du magasin et de l'horizon → clic sur « Calculer » → écran Résultat de prévision → clic sur « Voir la qualité et l'explication » → écran Qualité et explication → export CSV facultatif.
| ------- | --------------------------------------------------- | --------------------- |
| 1       | Dossier de lancement fusionné, prototype en script |                       |
Consolidateur : Achraf Alla   Relecteur : Amine El Alouani   Fichier : `docs/semaine1/4-pipeline.md`
| 3       | MVP complet, Docker et CI au vert                   |                       |
| 4       | Résultats mesurés, code gelé, soutenance         |                       |

**4.3 Vue chronologique.** Ajoutez un diagramme de Gantt en Mermaid (modèle ci-dessous, à adapter à vos dates et tâches) :

```mermaid
gantt
    dateFormat YYYY-MM-DD
    title Pipeline du projet
    section Semaine 1
    T1 Dépôt et environnement   :t1, 2026-11-16, 1d
| T1 | Valider le chargement M5 et le format commun | F1 | Achraf Alla | - | 1 | Le script charge un sous-ensemble et produit `unique_id`, `ds`, `y` sans erreur |
| T2 | Construire les variables calendrier, prix et lags | F1, F3 | Amine El Alouani | T1 | 1 | Les features sont générées sur un jeu de validation sans fuite temporelle |
| T3 | Implémenter le modèle de référence saisonnier | F1, F2 | Achraf Alla | T1 | 1 | Une prévision à 28 jours est produite pour 20 séries |
| T4 | Entraîner le premier modèle ML/statistique | F1 | Amine El Alouani | T2 | 2 | Le modèle sauvegardé prédit les 28 jours de l'échantillon |
| T5 | Ajouter le backtesting et les métriques | F2 | Achraf Alla | T3, T4 | 2 | MAE, RMSE et sMAPE sont calculés automatiquement |
| T6 | Ajouter l'explication des contributions | F3 | Amine El Alouani | T4 | 2 | Les trois facteurs principaux sont disponibles pour une série |
| T7 | Exposer les fonctions par FastAPI | F1, F2, F3 | Achraf Alla | T5, T6 | 3 | Les endpoints répondent avec un schéma JSON documenté |
| T8 | Construire l'interface Streamlit et l'export | F1, F2, F3, F4 | Amine El Alouani | T7 | 3 | Le scénario complet est démontrable de la sélection à l'export |
    T2 Récupération des données :t2, after t1, 2d
| T1, T2, T3, T4, T5, T6, T7, T8 |
    T3 Indexation               :t3, after t2, 2d
    T4 API /ask                 :t4, after t3, 2d
```

**4.4 Chemin critique et charge**

    T1 Chargement et format     :t1, 2026-11-16, 1d
    T2 Features                 :t2, after t1, 1d
    T3 Modèle de référence      :t3, after t1, 1d

    T4 Modèle principal         :t4, after t2, 2d
    T5 Backtesting              :t5, after t4, 2d
    T6 Explications             :t6, after t4, 1d
- [ ] Aucune tâche ne dépasse 2 jours.
    T7 API                      :t7, after t5, 2d
    T8 Interface et export      :t8, after t7, 2d
- [ ] Chaque fonctionnalité du MVP a au moins une tâche, et chaque tâche a un critère de fin vérifiable.
 Chaîne de tâches dont le moindre retard décale la soutenance : T1, T2, T4, T5, T7, T8. T3 et T6 peuvent avancer en parallèle après T1/T4.
 Charge par membre (nombre de jours de tâches) : Amine El Alouani, 8 jours ; Achraf Alla, 8 jours.
- [ ] Les tâches existent comme issues GitHub.

## Remise et décision de l'enseignant
- [ ] Échantillon de données dans `data/sample/`
- [ ] Schéma et écrans visibles sur GitHub
- [ ] Issues GitHub créées pour les tâches du pipeline
- [ ] Étiquette `semaine1-remis` posée et enseignant prévenu

| Données accessibles et échantillon présent (L2)                       | Bloquant      | ☐        |             |
| MVP réaliste en 4 semaines pour cette taille d'équipe (L1, L4)         | Bloquant      | ☐        |             |
| Livrables répartis, chacun avec un rédacteur et un relecteur distincts | Bloquant      | ☐        |             |
| Licence et données personnelles traitées (L2)                          | Bloquant      | ☐        |             |
| Architecture cohérente avec les fonctionnalités (L1, L3)               | À améliorer | ☐        |             |
| Écrans couvrant tout le MVP (L3)                                        | À améliorer | ☐        |             |
| Tâches courtes, critères de fin vérifiables, charge équilibrée (L4) | À améliorer | ☐        |             |
| Alternative de repli et jeu de test définis (L2)                        | À améliorer | ☐        |             |

**Décision** : ☐ Validé   ☐ À reprendre   ☐ Refusé (changement de sujet)

Date et visa : \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Lien avec l'évaluation.** Ce dossier sert de référence pour le critère P1 (respect du cadrage) et alimente P3 (jeu de test et indicateurs) et P7 (pipeline et suivi). La répartition et les pull requests de chaque membre comptent comme preuves pour le coefficient individuel.
