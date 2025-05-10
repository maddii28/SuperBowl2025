import json

# Load the JSON file
file_path = "filtered_comments.json"

with open(file_path, "r") as file:
    data = json.load(file)  # Assuming data is a list of comments (strings)

# Define your brand keyword dictionary
brand_keywords = {
    # Brands with potential variations and single-word mentions
    "Taco Bell": ["tacobell", "taco", "bell", "taco bell", "tbell", "taco bell ad", "tbell ad", "taco bell food", "tbell food"],
    "Michelob Ultra": ["michelob", "ultra", "michelobultra", "michelob beer", "michelob ultra beer", "michelob ultra ad", "ultrabeer", "michelob ad"],
    "Pringles": ["pringles", "pringleschips", "pringles chips", "pringles ad", "pringles original", "pringles sour cream", "pringles bbq", "pringlescan", "pringles can"],
    "Reese's": ["reese", "reesescups", "reesescup", "reeses peanut butter cups", "reeses ad", "reeses cup", "reeses candy", "reese peanut butter"],
    "GoDaddy": ["godaddy", "godaddycom", "godaddy website", "godaddy.com", "godaddy hosting", "godaddy ad", "go daddy", "go daddy ad"],
    "Bud Light": ["budlight", "bud", "light", "bud light", "bud light beer", "bud light ad", "bud beer", "budweiser", "bud ad", "light beer"],
    "Booking.com": ["booking", "booking.com", "booking com", "booking ad"],
    "Bosch": ["bosch", "bosch tools", "bosch ad", "bosch appliances", "bosch usa"],
    "Budweiser": ["budweiser", "bud", "buds", "bud ad", "bud beer", "budweiser ad"],
    "Cirkul": ["cirkul", "cirkul water", "cirkul ad", "cirkul drink"],
    "Coffee mate": ["coffeemate", "coffee mate", "coffe mate ad", "coffee mate creamer", "coffee mate ad"],
    "Coors Light": ["coorslight", "coors", "light beer", "coors light ad", "coors beer"],
    "Disney": ["disney", "disneyland", "disney ad", "disney brand", "disney plus", "disney princess"],
    "DoorDash": ["doordash", "door dash", "doordash ad", "door dash food", "dash food"],
    "Doritos": ["doritos", "dorito", "doritos chips", "doritos ad", "doritos nacho cheese", "doritos cool ranch"],
    "Dove": ["dove", "dove soap", "dove ad", "dove products", "dove beauty"],
    "Dunkin'": ["dunkin", "dunkin donuts", "dunkin ad", "dunkin coffee", "dunkin drink"],
    "Duracell": ["duracell", "duracell battery", "duracell ad", "duracell brand"],
    "Fetch": ["fetch", "fetch rewards", "fetch ad", "fetch shopping"],
    "GoDaddy": ["godaddy", "godaddycom", "godaddy hosting", "godaddy ad"],
    "Häagen-Dazs": ["haagen dazs", "haagen dazs ice cream", "haagen dazs ad"],
    "Instacart": ["instacart", "instacart delivery", "instacart ad"],
    "Jeep": ["jeep", "jeep cars", "jeep ad", "jeep vehicle", "jeep wrangler"],
    "Kia": ["kia", "kia cars", "kia ad", "kia vehicle", "kia motors"],
    "Lay's": ["lays", "lays chips", "lays ad", "lays potato chips", "lays snack"],
    "Liquid Death": ["liquid death", "liquid death water", "liquid death ad"],
    "Little Caesars": ["little caesars", "little caesars pizza", "little caesars ad", "little caesars brand"],
    "MSC Cruises": ["msc cruises", "msc ad", "msc brand", "msc boat", "msc cruise"],
    "Meta": ["meta", "meta ad", "meta facebook", "meta company", "facebook", "instagram", "whatsapp"],
    "Michelob Ultra": ["michelob", "michelob ultra", "michelob beer", "michelob ultra ad"],
    "Mountain Dew": ["mountain dew", "mountain dew ad", "dew", "mountain dew soda", "mountain dew drink"],
    "NerdWallet": ["nerdwallet", "nerd wallet", "nerdwallet ad"],
    "Nerds": ["nerds", "nerd candy", "nerds ad", "nerds brand"],
    "Novartis": ["novartis", "novartis ad", "novartis brand"],
    "Nyx Cosmetics": ["nyx cosmetics", "nyx", "nyx ad", "nyx makeup", "nyx brand"],
    "OpenAI": ["openai", "openai ad", "openai products", "chatgpt", "gpt", "open ai"],
    "Pfizer": ["pfizer", "pfizer ad", "pfizer vaccine", "pfizer brand"],
    "Poppi": ["poppi", "poppi drink", "poppi ad", "poppi beverage"],
    "Pringles": ["pringles", "pringles chips", "pringles ad", "pringles flavor", "pringles sour cream", "pringles bbq"],
    "Reese's": ["reeses", "reeses cups", "reeses peanut butter cups", "reeses ad", "reeses candy"],
    "Ritz": ["ritz", "ritz crackers", "ritz ad", "ritz snack"],
    "Rocket Mortgage": ["rocket mortgage", "rocket mortgage ad", "rocket home loan", "rocket mortgage brand"],
    "STōK Cold Brew Coffee": ["stok", "stok coffee", "stok cold brew", "stok ad", "stok cold brew coffee"],
    "Skechers": ["skechers", "skechers shoes", "skechers ad", "skechers brand"],
    "Squarespace": ["squarespace", "squarespace ad", "squarespace website", "squarespace brand"],
    "Stella Artois": ["stella artois", "stella beer", "stella artois ad", "stella beer ad"],
    "Taco Bell": ["tacobell", "taco", "bell", "tbell", "taco bell ad", "taco bell food"],
    "Tubi": ["tubi", "tubi tv", "tubi ad", "tubi brand", "tubi streaming"],
    "TurboTax": ["turbotax", "turbotax ad", "turbotax brand", "tax"],
    "Uber Eats": ["ubereats", "ubereats delivery", "uber eats", "ubereats ad", "ubereats food"],
    "WeatherTech": ["weathertech", "weather tech", "weathertech ad", "weathertech brand"],
}


# Flatten the keyword list
keyword_list = [keyword.lower() for keywords in brand_keywords.values() for keyword in keywords]

# Filter comments that contain at least one keyword
filtered_comments = [comment for comment in data if any(keyword in comment.lower() for keyword in keyword_list)]

# Remove duplicates while maintaining order
unique_comments = list(dict.fromkeys(filtered_comments))

# Overwrite the original JSON file with the unique filtered comments
with open(file_path, "w") as file:
    json.dump(unique_comments, file, indent=4)

print(f"Updated {file_path} with {len(unique_comments)} unique filtered comments.")
