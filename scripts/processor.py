import pandas as pd

def process_and_save(df, output_file='bank_reviews.csv'):
    if df.empty:
        print("DataFrame is empty. No processing done.")
        return

    print("Processing data...")

    df = df.rename(columns={
        'Review Text': 'review',
        'Rating': 'rating',
        'Date': 'date',
        'App Name': 'bank'
    })

    df['source'] = 'Google Play'

    initial_count = len(df)
    df = df.dropna(subset=['review'])
    df = df.drop_duplicates(subset=['review', 'bank'])
    
    dropped_count = initial_count - len(df)
    if dropped_count > 0:
        print(f"Removed {dropped_count} duplicate/empty rows.")
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
    df = df[['review', 'rating', 'date', 'bank', 'source']]
    try:
        df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"Success! Saved {len(df)} rows to '{output_file}'")
    except Exception as e:
        print(f"Error saving file: {e}")