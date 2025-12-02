# 📱 Google Play Store Review Analytics

<p align="center">
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/PostgreSQL-13+-336791.svg" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/NLP-DistilBERT%20%2F%20SpaCy-orange" alt="NLP">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT">
  <img src="https://img.shields.io/badge/Status-Completed-green" alt="Status: Completed">
</p>

## 10 Academy: Artificial Intelligence Mastery - Week 2 Challenge
**Uncovering actionable insights from Ethiopian banking app reviews through Data Engineering and NLP.**

---

## 📖 Project Overview

This project is a full-stack data engineering and NLP pipeline designed to scrape, analyze, and store user feedback for major Ethiopian banking applications (**CBE, Bank of Abyssinia, Dashen Bank**). 

The system moves beyond simple star ratings by utilizing **Transformer models (BERT)** to quantify sentiment and **Thematic Analysis** to pinpoint specific satisfaction drivers (e.g., "Good UI") and pain points (e.g., "Login Loops"). The final data is persisted in a **PostgreSQL** database for scalability.

### 🚀 Key Features
*   **Data Collection:** Automated scraping of 1,300+ reviews using `google-play-scraper`.
*   **Advanced NLP Engine:**
    *   **Translation:** Amharic → English via `deep-translator`.
    *   **Cleaning:** Lemmatization and stop-word removal using `SpaCy`.
    *   **Sentiment:** High-accuracy scoring using Hugging Face's `distilbert-base-uncased`.
*   **Data Engineering:** Relational database storage (ETL) using **PostgreSQL** and SQLAlchemy.
*   **Actionable Insights:** Automated generation of "Pain Points" vs. "Drivers" and visualization of sentiment trends.

---

## 📂 Repository Structure
<p align="center">
<img src="Images/filestructure.png" alt="File Structure" width="80%">
<br>
<em>Fig 1: Project Directory Structure</em>
</p>

🛠 Installation & Setup
1. Clone the Repository
code
Bash
download
content_copy
expand_less
git clone https://github.com/zemicahel/kaim-week2.git
cd kaim-week2
2. Virtual Environment
code
Bash
download
content_copy
expand_less
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
3. Install Dependencies

This project requires NLP libraries and Database drivers.

code
Bash
download
content_copy
expand_less
pip install pandas numpy google-play-scraper transformers torch spacy psycopg2-binary sqlalchemy deep-translator seaborn wordcloud

Important: Download the SpaCy English model:

code
Bash
download
content_copy
expand_less
python -m spacy download en_core_web_sm
4. Database Setup (PostgreSQL)

Ensure PostgreSQL is running locally. Create a database named newami (or update load_db.py with your credentials).

📊 Workflow & Methodology

The pipeline is executed in four phases corresponding to the project tasks.

Phase 1: Data Collection (ETL - Extract)

Script: scripts/scraper.py & scripts/processor.py

Fetches the latest ~450 reviews per bank.

Cleans data, removes duplicates, and standardizes date formats.

Phase 2: NLP Analysis (ETL - Transform)

Script: scripts/sentiment_analysis.py

Step 1: Translates non-English reviews.

Step 2: Sentiment Analysis: Uses DistilBERT (Transformer) to assign labels (POSITIVE/NEGATIVE) and confidence scores. Fallback to VADER included for legacy support.

Step 3: Thematic Tagging: Uses Regex and SpaCy lemmas to categorize reviews into: Access Issues, Transaction Performance, UI/UX, Customer Support.

Phase 3: Data Warehousing (ETL - Load)

Script: scripts/load_db.py

Defines a relational schema (banks and reviews tables).

Loads the processed/analyzed CSV data into PostgreSQL.

Ensures referential integrity between Bank IDs and Reviews.

Database Schema:

Banks: bank_id (PK), bank_name
Reviews: review_id (PK), bank_id (FK), text, sentiment_score, themes

Phase 4: Insights & Reporting

Notebook: notebooks/analysis.ipynb

Generates the Final Report.

Visualizations: Sentiment Heatmaps, Trend Lines (Time-Series), and Word Clouds.

Automated Insights: Programmatically identifies the lowest-scoring theme (Pain Point) and highest-scoring theme (Driver) for each bank.

📉 Outputs & Results

The following assets are generated:

File / Asset	Description
data/cleaned/task2_reviews_analyzed_bert.csv	Final dataset with BERT scores and Themes.
PostgreSQL Database	Persistent storage of all structured data.
Final_Report.pdf	Executive summary with strategic recommendations.
Sample Insight

"While UI/UX is a strong satisfaction driver across all apps, Access Issues (Login loops, OTP failures) remains the primary cause of churn, correlating with a 40% drop in sentiment scores."

🤝 Contributing

Contributions are welcome! Please follow the standard Git workflow:

Fork the Project

Create your Feature Branch (git checkout -b feature/AmazingFeature)

Commit your Changes

Push to the Branch

Open a Pull Request

📜 License

Distributed under the MIT License. See LICENSE for more information.

📞 Contact

Zemicahel

![alt text](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)


![alt text](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)

code
Code
download
content_copy
expand_less