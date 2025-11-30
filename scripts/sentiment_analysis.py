
import pandas as pd
import numpy as np
import re
import warnings
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from langdetect import detect
from deep_translator import GoogleTranslator
from sklearn.feature_extraction.text import TfidfVectorizer

warnings.filterwarnings("ignore")


def load_data(filepath):
    """Loads CSV and ensures review_id exists."""
    print(f"Loading data from {filepath}...")
    df = pd.read_csv(filepath)
    if "review_id" not in df.columns:
        df = df.reset_index().rename(columns={"index": "review_id"})
    return df


def detect_and_translate(text):
    """Detects language and translates Amharic to English."""
    try:
        lang = detect(str(text))
    except:
        lang = "unknown"
        
    if lang == "am":
        try:
            return GoogleTranslator(source='auto', target='en').translate(text)
        except:
            return text
    return text

def clean_text(text):
    """Basic text cleaning."""
    text = str(text).lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def preprocess_reviews(df, text_col="review"):
    print("Step 1: Translating (this may take time)...")
    df["review_en"] = df[text_col].apply(detect_and_translate)
    print("Step 2: Cleaning text...")
    df["clean_review"] = df["review_en"].apply(clean_text)
    return df


def analyze_sentiment_vader(df, text_col="clean_review"):
    print("Step 3: Running Sentiment Analysis (VADER)...")
    sia = SentimentIntensityAnalyzer()

    def get_score_and_label(text):
        scores = sia.polarity_scores(str(text))
        compound = scores['compound']
        if compound >= 0.05:
            label = "positive"
        elif compound <= -0.05:
            label = "negative"
        else:
            label = "neutral"
        return label, compound

    df[['sentiment_label', 'sentiment_score']] = df[text_col].apply(
        lambda x: pd.Series(get_score_and_label(x))
    )
    return df


def extract_top_keywords(df, text_col="clean_review", n=10):
    print("Step 4: Extracting keywords for discovery...")
    tfidf = TfidfVectorizer(stop_words="english", max_features=1000, ngram_range=(1, 2))
    try:
        tfidf.fit(df[text_col])
        feature_names = np.array(tfidf.get_feature_names_out())
        results = {}
        for bank in df["bank"].unique():
            bank_reviews = df[df["bank"] == bank][text_col]
            if len(bank_reviews) > 0:
                mat = tfidf.transform(bank_reviews)
                mean_scores = mat.mean(axis=0).A1
                top_indices = mean_scores.argsort()[::-1][:n]
                results[bank] = feature_names[top_indices]
        return results
    except ValueError:
        return {}

def assign_themes(df, text_col="clean_review"):
    print("Step 5: Assigning Themes...")
    
    THEME_DICT = {
        "Access Issues": ["login", "otp", "error", "fail", "password", "cant access"],
        "Transaction Performance": ["transfer", "slow", "delay", "payment", "transaction", "hanged"],
        "UI/UX": ["ui", "interface", "design", "app", "easy", "user friendly"],
        "Customer Support": ["support", "help", "service", "customer", "call"],
        "Features": ["update", "feature", "add", "option", "version"]
    }

    def get_theme(text):
        detected = []
        for theme, kws in THEME_DICT.items():
            for kw in kws:
                # \b matches word boundaries
                if re.search(r'\b' + re.escape(kw) + r'\b', text):
                    detected.append(theme)
                    break 
        if not detected:
            return ["Other"]
        return detected

    df["identified_themes"] = df[text_col].apply(get_theme)
    df["themes_str"] = df["identified_themes"].apply(lambda x: ", ".join(x))
    return df


def run_pipeline(input_path, output_path, summary_path):
    df = load_data(input_path)
    
    df = preprocess_reviews(df)
    
    df = analyze_sentiment_vader(df)
    
    df = assign_themes(df)
    
    output_cols = ["review_id", "review", "sentiment_label", "sentiment_score", "themes_str"]
    final_df = df[[c for c in output_cols if c in df.columns]].copy()
    final_df.rename(columns={"themes_str": "identified_themes", "review": "review_text"}, inplace=True)
    final_df.to_csv(output_path, index=False)
    
    summary = df.groupby(["bank", "rating"]).agg({
        "sentiment_score": "mean"
    }).reset_index()
    summary.to_csv(summary_path, index=False)
    
    print("Pipeline finished successfully.")
    
    keywords = extract_top_keywords(df)
    return final_df, summary, keywords