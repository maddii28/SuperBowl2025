import praw
import json
from datetime import datetime

# Initialize Reddit instance
reddit = praw.Reddit(
    client_id='//',
    client_secret='//',
    user_agent = 'python:my_superbowl_ads_scraper:v1.0 (by u/Constant-Rip9231)'
)

# Define brand keywords
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

# Define the subreddit and search query
subreddit_name = 'SuperBowlBetting'  # Replace with the relevant subreddit
search_query = '("Commercial" OR "ad")'

# Fetch the subreddit
subreddit = reddit.subreddit(subreddit_name)

# Initialize a dictionary to store brand comments
all_comments_data = {}

# Loop through the search results
for submission in subreddit.search(search_query, sort='new', limit=10):
    submission.comments.replace_more(limit=0)  # This avoids loading "MoreComments"
    
    # Initialize a dictionary for storing brand-specific comments for each submission
    brand_comments = {brand: [] for brand in brand_keywords}
    
    # Process comments for each post
    for comment in submission.comments.list():
        comment_text = comment.body.lower()  # Convert the comment to lowercase for easier matching
        
        # Check if any brand keyword is mentioned in the comment
        for brand, keywords in brand_keywords.items():
            for keyword in keywords:
                if keyword.lower() in comment_text:
                    brand_comments[brand].append({
                        "comment": comment.body,
                        "timestamp": datetime.utcfromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S')
                    })
                    break
    
    # Add submission and brand comments to all_comments_data
    all_comments_data[submission.id] = {
        "title": submission.title,
        "url": submission.url,
        "score": submission.score,
        "comments": brand_comments
    }

# Read existing data from the JSON file (if exists)
try:
    with open('reddit_comments.json', 'r') as json_file:
        existing_data = json.load(json_file)
except FileNotFoundError:
    existing_data = {}

# Append the new data
existing_data.update(all_comments_data)

# Save the updated data to the JSON file
with open('reddit_comments.json', 'w') as json_file:
    json.dump(existing_data, json_file, indent=4)

print("Data has been saved to reddit_comments.json")
