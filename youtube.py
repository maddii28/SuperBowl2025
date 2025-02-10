import googleapiclient.discovery
import googleapiclient.errors
import json
from datetime import datetime
import os

# Set up YouTube Data API client
def get_youtube_comments(video_id, api_key, brand_keywords):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
    
    # Initialize an empty list for filtered comments
    filtered_comments = []
    
    try:
        request = youtube.commentThreads().list(part="snippet", videoId=video_id, textFormat="plainText")
        response = request.execute()
    except googleapiclient.errors.HttpError as e:
        print(f"HTTP Error: {e}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    
    while response:
        try:
            for item in response.get('items', []):  # Use `.get()` to avoid KeyErrors
                try:
                    comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                    timestamp = item['snippet']['topLevelComment']['snippet']['publishedAt']
                except KeyError:
                    print("Skipping a comment due to missing data.")
                    continue

                # Check if comment contains any brand keyword
                brand_name = match_brand_keywords(comment, brand_keywords)
                if brand_name:
                    filtered_comments.append({
                        "scraper": "YouTube",
                        "brand_name": brand_name,
                        "comment": comment,
                        "timestamp": timestamp
                    })
            
            # Check if there are more comments to fetch
            if 'nextPageToken' in response:
                request = youtube.commentThreads().list(
                    part="snippet", videoId=video_id, textFormat="plainText", pageToken=response['nextPageToken']
                )
                response = request.execute()
            else:
                break
        except googleapiclient.errors.HttpError as e:
            print(f"HTTP Error while paginating: {e}")
            break
        except Exception as e:
            print(f"An error occurred while processing comments: {e}")
            break
    
    return filtered_comments

# Function to check if comment matches any brand keyword
def match_brand_keywords(comment, brand_keywords):
    for brand, keywords in brand_keywords.items():
        if any(keyword.lower() in comment.lower() for keyword in keywords):
            return brand
    return None

# Save to CSV function
def save_to_json(comments, file_name="superbowl_comments.json"):
    """ Saves the comments to a JSON file. """
    try:
        # Check if file exists and handle empty or corrupt JSON files
        if os.path.isfile(file_name):
            with open(file_name, "r") as file:
                try:
                    existing_data = json.load(file)
                except json.JSONDecodeError:
                    # Handle case where JSON is empty or invalid, initialize with an empty list
                    existing_data = []
        else:
            existing_data = []

        # Append new comments to existing data
        existing_data.extend(comments)

        # Write the updated data back to the file
        with open(file_name, "w") as file:
            json.dump(existing_data, file, indent=4)

    except Exception as e:
        print(f"Error while writing to JSON: {e}")



# Example brand keywords dictionary
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


# Example YouTube video ID (replace with actual video ID)
video_id = "BIgJO3Uk19w"
api_key = "AIzaSyCjyfnbyeUZjIo9ZYa6DWBhXIbkIYId5Z0"

# Scrape comments
filtered_comments = get_youtube_comments(video_id, api_key, brand_keywords)

# Save the filtered comments to a CSV file
save_to_json(filtered_comments)

print(f"Saved {len(filtered_comments)} comments to JSON.")
