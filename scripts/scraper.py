import pandas as pd
from google_play_scraper import app, reviews, Sort

def fetch_reviews(app_ids, count_per_app=450, lang='en', country='us'):
    
    dataset = []

    for app_id in app_ids:
        try:
            app_info = app(
                app_id,
                lang=lang,
                country=country
            )
            app_title = app_info['title']
            print(f"Scraping {count_per_app} reviews for: {app_title}...")
            app_reviews, _ = reviews(
                app_id,
                lang=lang,
                country=country,
                sort=Sort.NEWEST,
                count=count_per_app
            )
            for review in app_reviews:
                dataset.append({
                    'App Name': app_title,
                    'Review Text': review['content'],
                    'Rating': review['score'],
                    'Date': review['at']
                })
                
        except Exception as e:
            print(f"Error scraping {app_id}: {e}")

    return pd.DataFrame(dataset)