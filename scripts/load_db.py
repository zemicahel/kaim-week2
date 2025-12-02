import pandas as pd
from sqlalchemy import create_engine, text
import os


import pandas as pd
from sqlalchemy import create_engine, text

def get_engine(user, password, host, port, db_name):
    """Creates SQLAlchemy engine."""
    if password:
        url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}"
    else:
        url = f"postgresql+psycopg2://{user}@{host}:{port}/{db_name}"
        
    try:
        engine = create_engine(url)
        with engine.connect() as conn:
            pass
        print(f"Successfully connected to database: {db_name}")
        return engine
    except Exception as e:
        print(f"Connection Failed: {e}")
        return None

def create_schema(engine, schema_path):
    """Executes the SQL schema file to create tables."""
    print(f"Applying schema from {schema_path}...")
    try:
        with engine.connect() as conn:
            with open(schema_path, "r") as file:
                sql_script = file.read()
                for statement in sql_script.split(';'):
                    if statement.strip():
                        conn.execute(text(statement))
            conn.commit()
        print("Schema created/reset successfully.")
    except FileNotFoundError:
        print(f"Error: Schema file not found at {schema_path}")

def load_data(engine, cleaned_csv_path, analyzed_csv_path):
    print("Loading datasets...")
    
    try:
        df_meta = pd.read_csv(cleaned_csv_path) 
        df_nlp = pd.read_csv(analyzed_csv_path) 
    except FileNotFoundError as e:
        print(f"Error loading CSVs: {e}")
        return

    if "review_id" not in df_meta.columns:
        df_meta.reset_index(inplace=True)
        df_meta.rename(columns={"index": "review_id"}, inplace=True)
        
    df_meta['review_id'] = df_meta['review_id'].astype(str)
    df_nlp['review_id'] = df_nlp['review_id'].astype(str)
    
    full_df = pd.merge(
        df_meta[['review_id', 'bank', 'rating', 'date', 'source']], 
        df_nlp[['review_id', 'review_text', 'sentiment_label', 'sentiment_score', 'identified_themes']], 
        on="review_id", 
        how="inner"
    )
    
    print(f"Merged Data Shape: {full_df.shape}")

    unique_banks = full_df['bank'].unique()
    for bank in unique_banks:
        sql = text("""
            INSERT INTO banks (bank_name, app_name) 
            VALUES (:name, :name) 
            ON CONFLICT (bank_name) DO NOTHING
        """)
        with engine.connect() as conn:
            conn.execute(sql, {"name": bank})
            conn.commit()
    
    with engine.connect() as conn:
        db_banks = pd.read_sql("SELECT bank_name, bank_id FROM banks", conn)
    
    bank_map = dict(zip(db_banks['bank_name'], db_banks['bank_id']))
    full_df['bank_id'] = full_df['bank'].map(bank_map)

    reviews_table = full_df[[
        'review_id', 'bank_id', 'review_text', 'rating', 'date', 
        'sentiment_label', 'sentiment_score', 'identified_themes', 'source'
    ]].copy()
    
    reviews_table.rename(columns={'date': 'review_date'}, inplace=True)
    
    print("Inserting reviews into PostgreSQL...")
    reviews_table.to_sql('reviews', engine, if_exists='replace', index=False)
    print(f"Success! {len(reviews_table)} rows inserted.")