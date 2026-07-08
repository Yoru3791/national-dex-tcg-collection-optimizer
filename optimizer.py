import requests
import csv
import time
from collections import defaultdict

# --- CONFIGURATION ---
CSV_FILENAME = 'collection.csv'
API_KEY = '' # Optional, but recommended
API_URL = 'https://api.pokemontcg.io/v2/cards'
CARDS_PER_PACK = 8 

def get_missing_pokemon(filename):
    missing = set()
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Status'].strip().lower() == 'missing':
                    try:
                        dex_num = int(row['Number'])
                        missing.add(dex_num)
                    except ValueError:
                        continue
    except FileNotFoundError:
        print(f"\n[!] Error: Could not find {filename}.")
        print("Please make sure the file exists in the same folder as the script.")
        exit()
    return missing

def fetch_all_cards(api_key):
    headers = {'X-Api-Key': api_key} if api_key else {}
    set_data = defaultdict(set) 
    
    page = 1
    max_retries = 3
    print("\nFetching data from the Pokémon TCG API... (This might take a moment)")
    
    while True:
        retries = 0
        success = False
        
        while retries < max_retries and not success:
            response = requests.get(f"{API_URL}?page={page}&select=nationalPokedexNumbers,set", headers=headers)
            
            if response.status_code == 200:
                success = True
            elif response.status_code >= 500:
                print(f"Server error. Retrying... ({retries+1}/{max_retries})")
                time.sleep(5)
                retries += 1
            elif response.status_code == 429:
                print("Rate limit reached. Waiting 10 seconds...")
                time.sleep(10)
                retries += 1
            else:
                print(f"Fatal API error: {response.status_code}.")
                break
                
        if not success:
            break
            
        data = response.json()
        cards = data.get('data', [])
        
        if not cards:
            break 
            
        for card in cards:
            dex_numbers = card.get('nationalPokedexNumbers', [])
            set_name = card.get('set', {}).get('name', 'Unknown Set')
            
            if dex_numbers:
                for num in dex_numbers:
                    set_data[set_name].add(num)
                    
        print(f"Page {page} fetched...")
        page += 1
        time.sleep(0.5)
        
    return set_data

def calculate_best_sets(missing_pokemon, set_data):
    results = []
    for set_name, set_pokemon in set_data.items():
        if not set_pokemon: continue
        new_hits = set_pokemon.intersection(missing_pokemon)
        total_unique = len(set_pokemon)
        hit_ratio = len(new_hits) / total_unique
        
        results.append({
            'set_name': set_name,
            'new_hits_count': len(new_hits),
            'total_in_set': total_unique,
            'probability': hit_ratio * 100
        })
        
    results.sort(key=lambda x: x['probability'], reverse=True)
    return results

def find_set_case_insensitive(set_name, set_data):
    """Searches for the set name ignoring case."""
    for key in set_data.keys():
        if key.lower() == set_name.lower().strip():
            return key
    return None

def analyze_product_yield(set_name, packs, missing_pokemon, set_data):
    """Calculates stats for a specific product."""
    real_set_name = find_set_case_insensitive(set_name, set_data)
    
    if not real_set_name:
        return None
        
    set_pokemon = set_data[real_set_name]
    new_hits = set_pokemon.intersection(missing_pokemon)
    
    total_unique = len(set_pokemon)
    missing_in_set = len(new_hits)
    hit_ratio = missing_in_set / total_unique if total_unique > 0 else 0
    
    # Approximation of useful Pokémon cards pulled
    total_cards_pulled = packs * CARDS_PER_PACK
    expected_new_pokemon = total_cards_pulled * hit_ratio
    
    return {
        'name': real_set_name,
        'missing_in_set': missing_in_set,
        'total_unique': total_unique,
        'ratio': hit_ratio * 100,
        'expected_yield': expected_new_pokemon
    }

def print_yield_result(result, packs):
    print(f"\n--- Analysis for {result['name']} ({packs} packs) ---")
    print(f"Unique useful cards from the set: {result['missing_in_set']} out of {result['total_unique']} ({result['ratio']:.2f}%)")
    print(f"Opening {packs} packs (approx {packs * CARDS_PER_PACK} Pokémon cards):")
    print(f" -> Very high probability of pulling duplicates." if result['ratio'] < 20 else " -> Good chance of pulling new cards.")
    print(f" -> Statistically, you would pull approx {result['expected_yield']:.1f} new Pokémon for your Pokédex.")

def main():
    print("--- Pokédex TCG Optimizer ---")
    missing_pokemon = get_missing_pokemon(CSV_FILENAME)
    
    if not missing_pokemon:
        print("You are not missing any Pokémon! Collection complete.")
        input("\nPress Enter to exit...")
        return
        
    print(f"You are currently missing {len(missing_pokemon)} Pokémon.")
    set_data = fetch_all_cards(API_KEY)
    
    while True:
        print("\n" + "="*40)
        print(" MAIN MENU ")
        print("="*40)
        print("1. View Top expansions to buy (General ranking)")
        print("2. Evaluate a specific product (Enter Set and Pack Quantity)")
        print("3. Compare two products")
        print("4. Exit")
        
        opcion = input("\nChoose an option (1-4): ")
        
        if opcion == '1':
            ranked_sets = calculate_best_sets(missing_pokemon, set_data)
            print("\n--- TOP EXPANSIONS TO BUY ---")
            for i, s in enumerate(ranked_sets[:10], 1):
                print(f"{i}. {s['set_name']}")
                print(f"   Probability of a useful pull: {s['probability']:.2f}% ({s['new_hits_count']}/{s['total_in_set']})")
                
        elif opcion == '2':
            set_name = input("Enter the expansion name (e.g., 'Surging Sparks'): ")
            packs = int(input("How many packs are you opening?: "))
            
            result = analyze_product_yield(set_name, packs, missing_pokemon, set_data)
            if result:
                print_yield_result(result, packs)
            else:
                print(f"[!] Set '{set_name}' not found. Check the English spelling.")
                
        elif opcion == '3':
            print("\n-- Product A --")
            set_a = input("Expansion name for Product A: ")
            packs_a = int(input("Number of packs for Product A: "))
            
            print("\n-- Product B --")
            set_b = input("Expansion name for Product B: ")
            packs_b = int(input("Number of packs for Product B: "))
            
            res_a = analyze_product_yield(set_a, packs_a, missing_pokemon, set_data)
            res_b = analyze_product_yield(set_b, packs_b, missing_pokemon, set_data)
            
            if not res_a or not res_b:
                print("[!] One of the sets was not found. Please try again.")
                continue
                
            print_yield_result(res_a, packs_a)
            print_yield_result(res_b, packs_b)
            
            print("\n*** VERDICT ***")
            if res_a['expected_yield'] > res_b['expected_yield']:
                print(f"You should buy Product A ({res_a['name']}). You would get approx {res_a['expected_yield'] - res_b['expected_yield']:.1f} MORE new Pokémon than with Product B.")
            elif res_b['expected_yield'] > res_a['expected_yield']:
                print(f"You should buy Product B ({res_b['name']}). You would get approx {res_b['expected_yield'] - res_a['expected_yield']:.1f} MORE new Pokémon than with Product A.")
            else:
                print("Both yield almost the same results. Choose the one with the best art or lowest price.")
                
        elif opcion == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
    # Esto evita que la consola se cierre de golpe si hacés doble clic
    input("\nPress Enter to exit...")