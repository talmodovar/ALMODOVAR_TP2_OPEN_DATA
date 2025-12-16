import duckdb
import pandas as pd
from pathlib import Path

def analyze_parquet():
    """Analyse complète des données Parquet."""
    
    # Chemin vers les données traitées (prend le dernier fichier généré)
    processed_dir = Path("data/processed")
    # On cherche d'abord les fichiers 'fruits_*.parquet' (données réelles)
    parquet_files = list(processed_dir.glob("fruits_*.parquet"))
    
    # Si pas de fichiers fruits, on regarde s'il y a d'autres parquets (ex: test)
    if not parquet_files:
        parquet_files = list(processed_dir.glob("*.parquet"))
    
    if not parquet_files:
        print("❌ Aucun fichier Parquet trouvé dans data/processed/")
        return

    # On prend le fichier le plus récent pour l'analyse
    parquet_file = sorted(parquet_files)[-1]
    print(f"📂 Analyse du fichier : {parquet_file}")

    con = duckdb.connect()
    
    print("=" * 60)
    print("VÉRIFICATION DES DONNÉES - FRUITS")
    print("=" * 60)
    
    # Charger le fichier Parquet dans une vue DuckDB
    con.execute(f"CREATE OR REPLACE VIEW products AS SELECT * FROM '{parquet_file}'")
    
    # a) STATISTIQUES GÉNÉRALES
    print("\n📊 STATISTIQUES GÉNÉRALES")
    print("-" * 30)
    
    count = con.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    print(f"Nombre total de produits : {count}")
    
    columns = con.execute("DESCRIBE products").df()
    print(f"Nombre de colonnes : {len(columns)}")
    print("\nListe des colonnes :")
    print(columns[['column_name', 'column_type']].to_string(index=False))

    # b) QUALITÉ DES DONNÉES
    print("\n✅ QUALITÉ DES DONNÉES")
    print("-" * 30)
    
    # Doublons sur code
    duplicates = con.execute("""
        SELECT COUNT(*) - COUNT(DISTINCT code) 
        FROM products
    """).fetchone()[0]
    print(f"Nombre de doublons potentiels (code) : {duplicates}")
    
    # Distribution Nutriscore
    print("\nDistribution du Nutri-Score :")
    nutri_dist = con.execute("""
        SELECT nutriscore_grade, COUNT(*) as count 
        FROM products 
        GROUP BY nutriscore_grade 
        ORDER BY count DESC
    """).df()
    print(nutri_dist.to_string(index=False))

    # c) ANALYSES NUTRITIONNELLES
    print("\n🍎 ANALYSES NUTRITIONNELLES")
    print("-" * 30)
    
    avg_stats = con.execute("""
        SELECT 
            ROUND(AVG(energy_100g), 2) as avg_energy,
            ROUND(AVG(fat_100g), 2) as avg_fat,
            ROUND(AVG(sugars_100g), 2) as avg_sugar,
            ROUND(AVG(proteins_100g), 2) as avg_protein,
            ROUND(AVG(salt_100g), 2) as avg_salt
        FROM products
    """).df()
    print("Moyennes nutritionnelles (pour 100g) :")
    print(avg_stats.to_string(index=False))
    
    print("\nProduit le plus calorique :")
    most_caloric = con.execute("""
        SELECT product_name, energy_100g 
        FROM products 
        ORDER BY energy_100g DESC 
        LIMIT 1
    """).df()
    print(most_caloric.to_string(index=False))
    
    print("\nTop 5 des produits les plus sucrés :")
    sweetest = con.execute("""
        SELECT product_name, sugars_100g 
        FROM products 
        ORDER BY sugars_100g DESC 
        LIMIT 5
    """).df()
    print(sweetest.to_string(index=False))

    # d) ANALYSES MARQUES
    print("\n🏷️ TOP MARQUES")
    print("-" * 30)
    
    top_brands = con.execute("""
        SELECT brands, COUNT(*) as count 
        FROM products 
        WHERE brands != 'Unknown' AND brands != ''
        GROUP BY brands 
        ORDER BY count DESC 
        LIMIT 10
    """).df()
    print(top_brands.to_string(index=False))
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    analyze_parquet()
