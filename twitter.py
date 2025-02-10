import time
import tweepy
import json
import threading

# Set your Twitter API credentials
api_key = '//'
api_secret_key = '//'
bearer_token = '//'

# Authenticate using Tweepy
client = tweepy.Client(bearer_token=bearer_token)

# Function to get tweets with exponential backoff
def get_tweets_with_backoff(query, max_results=100):
    backoff_time = 60  # Start with 60 seconds delay for the first attempt

    while True:
        try:
            # Search for recent tweets using the provided query
            tweets = client.search_recent_tweets(query=query, max_results=max_results)
            
            if tweets.data:  # Ensure that there are tweets returned
                return tweets.data
            else:
                print(f"No tweets found for the query: {query}.")
                return []

        except tweepy.errors.TooManyRequests as e:
            # If rate limit is exceeded, print a message and wait before retrying
            print(f"Rate limit exceeded. Retrying in {backoff_time} seconds...")
            time.sleep(backoff_time)
            backoff_time = min(backoff_time * 2, 300)  # Limit to 5 minutes max wait time

        except tweepy.errors.Unauthorized as e:
            # Handle Unauthorized error if credentials are incorrect
            print("Unauthorized error: Check your API credentials.")
            return []

        except Exception as e:
            # Catch any other errors that occur
            print(f"An error occurred: {e}")
            return []

# Brand keywords dictionary
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

# Function to fetch tweets for multiple brands concurrently
def fetch_and_save_brand_tweets():
    all_brand_tweets = {}

    def fetch_brand_tweets(brand, keywords):
        brand_tweets = []
        for keyword in keywords:
            print(f"Fetching tweets for {brand} with keyword: {keyword}")
            tweets = get_tweets_with_backoff(keyword)
            for tweet in tweets:
                brand_tweets.append({
                    "tweet_id": tweet.id,
                    "text": tweet.text,
                    "author": tweet.author_id,
                    "created_at": tweet.created_at
                })

        if brand_tweets:
            all_brand_tweets[brand] = brand_tweets

    # Create threads for each brand
    threads = []
    for brand, keywords in brand_keywords.items():
        thread = threading.Thread(target=fetch_brand_tweets, args=(brand, keywords))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    # Save the tweets to a JSON file
    with open("twitter_comments.json", "w") as f:
        json.dump(all_brand_tweets, f, indent=4)
    
    print("Tweets have been saved to 'brand_tweets.json'.")

# Execute the function to fetch and save tweets
fetch_and_save_brand_tweets()
