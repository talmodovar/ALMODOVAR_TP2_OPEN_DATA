# Pipeline Open Data - Fruits (OpenFoodFacts)

## 📋 Description

Ce projet implémente un pipeline d'ingénierie des données automatisé pour collecter, nettoyer et stocker des informations nutritionnelles sur les **fruits** depuis l'API publique OpenFoodFacts. Il est conçu pour être robuste, reproductible et facile à étendre.

## 🎯 Objectifs

- **Acquisition** : Récupérer ~1000 produits de la catégorie "fruits" via l'API v2.
- **Transformation** : Nettoyer les données (suppression doublons, gestion NULLs, typage strict).
- **Stockage** : Sauvegarder les données brutes (JSON) et raffinées (Parquet) pour analyse.
- **Qualité** : Assurer l'intégrité des données pour des analyses nutritionnelles.

## 🛠️ Technologies utilisées

- 🐍 **Python 3.11+**
- 🐼 **pandas** : Manipulation et nettoyage des données
- 🌐 **httpx** : Requêtes HTTP asynchrones/synchrones performantes
- 🔄 **tenacity** : Gestion robuste des retries API
- 📊 **DuckDB** : Analyse SQL performante sur fichiers Parquet
- 📦 **uv** : Gestionnaire de dépendances ultra-rapide

## 📦 Installation

### Prérequis

- Python 3.11 ou supérieur
- `uv` (recommandé) ou `pip`

### Configuration

1. Cloner le dépôt :
   ```bash
   git clone <url-du-repo>
   cd tp2-pipeline
   ```

2. Installer les dépendances :
   ```bash
   uv sync
   # ou
   pip install -r requirements.txt
   ```

### Variables d'environnement

Créer un fichier `.env` à la racine (optionnel si pas d'auth) :

```env
# Exemple de configuration (si nécessaire)
API_KEY=votre_cle_api
```

## 🚀 Utilisation

### Exécution du pipeline

Pour lancer le pipeline complet (collecte -> nettoyage -> stockage) :

```bash
uv run python -m pipeline.main --name fruits
```

Cela va :
1. Télécharger les données dans `data/raw/fruits_YYYYMMDD_HHMMSS.json`
2. Nettoyer les données
3. Sauvegarder le résultat dans `data/processed/fruits_YYYYMMDD_HHMMSS.parquet`

### Vérification des données

Pour analyser la qualité des fichiers générés :

```bash
uv run python verify_data.py
```

## 📊 Structure du projet

```
tp2-pipeline/
├── data/                   # Stockage des données (ignoré par git)
│   ├── raw/                # Fichiers JSON bruts
│   └── processed/          # Fichiers Parquet nettoyés
├── pipeline/               # Code source du pipeline
│   ├── config.py           # Configuration globale
│   ├── fetcher.py          # Module d'acquisition (API)
│   ├── transformer.py      # Module de transformation (pandas)
│   ├── storage.py          # Module de stockage (I/O)
│   └── main.py             # Script d'orchestration
├── verify_data.py          # Script d'analyse qualité
├── test_api.py             # Tests exploratoires API
├── pyproject.toml          # Dépendances (uv)
└── README.md               # Documentation
```

## 🔍 Données collectées

### Champs extraits

| Champ | Type | Description | Exemple |
|-------|------|-------------|---------|
| `code` | String | Code-barres unique (EAN) | "3274080005003" |
| `product_name` | String | Nom du produit | "Compote de Pomme" |
| `brands` | String | Marque | "Materne" |
| `categories` | String | Catégories (tags) | "Plant-based foods..." |
| `nutriscore_grade` | String | Note Nutri-Score (a-e) | "a" |
| `nova_group` | Int | Groupe NOVA (1-4) | 1 |
| `energy_100g` | Float | Énergie (kJ/100g) | 250.0 |
| `sugars_100g` | Float | Sucres (g/100g) | 12.5 |

### Statistiques Cibles

- **Volume** : ~1000 produits (~10 pages de 100)
- **Format** : Parquet (compression Snappy), optimisé pour l'analytique.

## 🧹 Nettoyage effectué

Le module `transformer.py` applique les règles suivantes :
1. **Dédoublonnage** : Suppression des doublons basés sur le `code`.
2. **Filtrage** : Suppression des produits sans nom ou sans code.
3. **Imputation** :
   - Textes manquants → "Unknown"
   - Valeurs nutritionnelles manquantes → 0.0
   - Nutriscore manquant → "unknown"
4. **Typage** : Conversion stricte vers les types cibles (int, float, string).
5. **Nettoyage texte** : Suppression des espaces superflus (strip).

## 📈 Exemples d'analyses possibles

Avec DuckDB, vous pouvez requêter directement le fichier Parquet :

```sql
-- Top 5 des fruits les plus sucrés
SELECT product_name, sugars_100g 
FROM 'data/processed/*.parquet' 
ORDER BY sugars_100g DESC 
LIMIT 5;

-- Distribution des Nutri-Scores
SELECT nutriscore_grade, count(*) as count 
FROM 'data/processed/*.parquet' 
GROUP BY nutriscore_grade;
```

## 🐛 Résolution de problèmes

**Erreur : "Rate limit exceeded"**
> Augmentez `API_RATE_LIMIT` dans `pipeline/config.py`.

**Erreur : "No products found"**
> Vérifiez que l'API est accessible et que la catégorie "fruits" existe toujours.

## 📝 Licence

TP académique - Usage éducatif uniquement dans le cadre du module Open Data & Data Engineering.

## 👤 Auteur

**TP2 Data Engineering**
