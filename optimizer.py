import requests
import csv
import time
from collections import defaultdict

# --- CONFIGURATION ---
CSV_FILENAME = 'collection.csv'
API_KEY = '' # Optional, but recommended to avoid rate limits at dev.pokemontcg.io
API_URL = 'https://api.pokemontcg.io/v2/cards'

def get_missing_pokemon(filename):
    """Reads the CSV and returns a set of missing National Pokédex numbers."""
    missing = set()
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Assumes columns: 'PokedexNumber', 'Name', 'Status'
                if row['Status'].strip().lower() == 'missing':
                    try:
                        dex_num = int(row['Number'])
                        missing.add(dex_num)
                    except ValueError:
                        continue
    except FileNotFoundError:
        print(f"Error: Could not find {filename}. Please create it first.")
        exit()
    return missing

def fetch_all_cards(api_key):
    """Fetches all cards from the API and extracts their Pokedex numbers and Set names."""
    headers = {'X-Api-Key': api_key} if api_key else {}
    set_data = defaultdict(set) # Maps Set Name -> Set of Pokedex Numbers
    
    page = 1
    max_retries = 3 # How many times will retry if server fails or something happens
    print("Fetching card data from Pokemon TCG API... (This might take a moment)")
    
    while True:
        retries = 0
        success = False
        
        while retries < max_retries and not success:
            # We only select the fields we need to keep the payload small
            response = requests.get(f"{API_URL}?page={page}&select=nationalPokedexNumbers,set", headers=headers)
            
            if response.status_code == 200:
                success = True
            elif response.status_code >= 500: # Errores del servidor (como el 504)
                print(f"Server timeout (Error {response.status_code}) on page {page}. Retrying in 5 seconds... ({retries+1}/{max_retries})")
                time.sleep(5)
                retries += 1
            elif response.status_code == 429: # Límite de peticiones real
                print("Rate limit reached. Waiting 10 seconds before retrying...")
                time.sleep(10)
                retries += 1
            else:
                print(f"API Error: {response.status_code}. Stopping fetch.")
                break # Sale del loop de reintentos si es un error fatal
                
        if not success:
            print("Failed to fetch page after multiple attempts. Processing with partial data...")
            break # Sale del loop principal y pasa a calcular
            
        data = response.json()
        cards = data.get('data', [])
        
        if not cards:
            break # No more cards to fetch
            
        for card in cards:
            dex_numbers = card.get('nationalPokedexNumbers', [])
            set_name = card.get('set', {}).get('name', 'Unknown Set')
            
            if dex_numbers:
                for num in dex_numbers:
                    set_data[set_name].add(num)
                    
        print(f"Fetched page {page}...")
        page += 1
        time.sleep(0.5) # Be gentle with the API
        
    return set_data
    """Fetches all cards from the API and extracts their Pokedex numbers and Set names."""
    headers = {'X-Api-Key': api_key} if api_key else {}
    set_data = defaultdict(set) # Maps Set Name -> Set of Pokedex Numbers
    
    page = 1
    print("Fetching card data from Pokemon TCG API... (This might take a moment)")
    
    while True:
        # We only select the fields we need to keep the payload small
        response = requests.get(f"{API_URL}?page={page}&select=nationalPokedexNumbers,set", headers=headers)
        
        if response.status_code != 200:
            print(f"API Error: {response.status_code}. If rate limited, please add an API key.")
            break
            
        data = response.json()
        cards = data.get('data', [])
        
        if not cards:
            break # No more cards to fetch
            
        for card in cards:
            dex_numbers = card.get('nationalPokedexNumbers', [])
            set_name = card.get('set', {}).get('name', 'Unknown Set')
            
            if dex_numbers:
                for num in dex_numbers:
                    set_data[set_name].add(num)
                    
        print(f"Fetched page {page}...")
        page += 1
        time.sleep(0.5) # Be gentle with the API
        
    return set_data

def calculate_best_sets(missing_pokemon, set_data):
    """Calculates the yield of new Pokemon per set and ranks them."""
    results = []
    
    for set_name, set_pokemon in set_data.items():
        if not set_pokemon:
            continue
            
        # Intersection: Pokemon in the set that are also in your missing list
        new_hits = set_pokemon.intersection(missing_pokemon)
        total_unique_in_set = len(set_pokemon)
        
        hit_ratio = len(new_hits) / total_unique_in_set
        
        results.append({
            'set_name': set_name,
            'new_hits_count': len(new_hits),
            'total_in_set': total_unique_in_set,
            'probability': hit_ratio * 100
        })
        
    # Sort by highest probability of a new hit
    results.sort(key=lambda x: x['probability'], reverse=True)
    return results

def main():
    print("--- National Dex TCG Optimizer ---")
    missing_pokemon = get_missing_pokemon(CSV_FILENAME)
    
    if not missing_pokemon:
        print("Congratulations! Your missing list is empty. You caught 'em all!")
        return
        
    print(f"You are currently missing {len(missing_pokemon)} Pokemon.")
    
    set_data = fetch_all_cards(API_KEY)
    ranked_sets = calculate_best_sets(missing_pokemon, set_data)
    
    print("\n--- TOP EXPANSIONS TO BUY ---")
    # Display the top 10 sets
    for i, s in enumerate(ranked_sets[:10], 1):
        print(f"{i}. {s['set_name']}")
        print(f"   Probability of pulling a new Pokemon: {s['probability']:.2f}%")
        print(f"   ({s['new_hits_count']} missing Pokemon out of {s['total_in_set']} unique in set)\n")

if __name__ == "__main__":
    main()
    input("\nPresioná Enter para salir...")