import httpx

def test_api_fruits():
    """Test manuel de l'API OpenFoodFacts pour les fruits."""
    response = httpx.get(
        "https://world.openfoodfacts.org/api/v2/search",
        params={
            "categories_tags": "fruits",
            "page": 1,
            "page_size": 5,
            "fields": "code,product_name,brands,nutriscore_grade,energy_100g"
        },
        timeout=30
    )
    
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Nombre de produits trouvés: {data.get('count', 0)}")
    print(f"Premier produit: {data['products'][0] if data.get('products') else 'Aucun'}")
    
    return data

if __name__ == "__main__":
    test_api_fruits()
