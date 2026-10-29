# 🍔 SnackBot Pro — Smart Assistant for On-Demand Food Services

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![Polars](https://img.shields.io/badge/Polars-CD792C?style=for-the-badge&logo=polars&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![NLP](https://img.shields.io/badge/NLP-SentenceTransformers-blueviolet?style=for-the-badge)

**An intelligent, NLP-powered food recommendation chatbot that helps users find snacks and food combos based on natural language queries and budget**

*Final Year Project — B.Sc Computer Science with Data Analytics*
*Dr. N.G.P. Arts and Science College, Coimbatore — March 2026*

[🚀 Features](#-features) · [🧠 How It Works](#-how-it-works) · [📊 Performance](#-performance) · [⚙️ Installation](#%EF%B8%8F-installation) · [📸 Screenshots](#-screenshots)

</div>

---

## 📌 Project Overview

**SnackBot Pro** is a smart food recommendation system that allows users to find food items using **natural language queries** instead of manually browsing menus. Users can simply type requests like *"snacks under ₹200"* or *"combo for ₹150"* and the system intelligently recommends the best matching items.

> **Problem:** Traditional restaurant menu systems rely on exact keyword search — they fail when users type in natural language or use different wording.

> **Solution:** SnackBot Pro uses NLP + Machine Learning to understand the **meaning** of queries, not just the keywords.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🗣️ **Natural Language Search** | Type queries like "cheap spicy snacks" or "something under ₹100" |
| 💰 **Budget-Based Combo Finder** | Automatically finds best food combinations within your budget |
| 🧠 **Semantic Search** | Understands meaning, not just exact words — powered by Sentence Transformers |
| 🔄 **Hybrid Recommendation** | Combines exact match + semantic search for best accuracy |
| 📦 **Smart Fallback** | If exact match fails, semantic search kicks in automatically |
| ✅ **Availability Filter** | Only shows currently available food items |
| 💬 **Chat Interface** | Streamlit-powered chatbot-style UI |
| ⚡ **Fast Performance** | Caching mechanisms reduce database load and model reload time |

---

## 🧠 How It Works

### System Architecture

```
User Query (Natural Language)
        ↓
Streamlit Chat Interface
        ↓
Query Preprocessing
  • Lowercase conversion
  • Stop word removal
  • Numeric value extraction (budget)
  • Intent detection (combo / search)
        ↓
┌─────────────────────────────┐
│     Intent Classification   │
│  Combo Query? → Combo Module│
│  Keyword Match? → Exact     │
│  Unclear? → Semantic Search │
└─────────────────────────────┘
        ↓
PostgreSQL Database (Menu Data)
        ↓
Machine Learning Module
  • Sentence Transformer (all-MiniLM-L6-v2)
  • Nearest Neighbors (Cosine Similarity)
        ↓
Recommendation Engine
  • Rank by relevance + price
  • Budget utilization score
        ↓
Results displayed in Streamlit UI
```

### Algorithms Used

**1. Sentence Transformer Model (`all-MiniLM-L6-v2`)**
- Converts menu items and user queries into dense vector embeddings
- Captures semantic meaning beyond exact keyword matching
- Enables understanding queries like *"cheap spicy snacks"* even if exact words aren't in the menu

**2. Nearest Neighbors Algorithm**
- Compares query embedding with all stored menu embeddings
- Uses **Cosine Similarity** as the distance metric
- Returns top-K most semantically similar food items

**3. Combo Optimization Logic**
- Generates all possible item pairs using `itertools.combinations`
- Filters combinations within the specified budget
- Ranks by **budget utilization score** (Total Price / Budget)
- Returns best value combinations

**4. Hybrid Recommendation Model (Final)**
- Layer 1: Exact keyword match (fast, precise)
- Layer 2: Semantic search with embeddings (intelligent fallback)
- Layer 3: Availability + price filtering
- Combines scores using a weighted hybrid ranking formula

---

## 📊 Performance

### Algorithm Comparison

| Algorithm | Precision@K | Recall | MRR |
|-----------|-------------|--------|-----|
| Keyword-Based Search | 0.58 | 0.60 | 0.55 |
| Pure Semantic Search | 0.66 | 0.70 | 0.63 |
| **Hybrid Model (Ours)** | **0.78** | **0.80** | **0.76** |

> The Hybrid Recommendation Model outperforms both traditional keyword search and pure semantic search across all metrics.

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|-----------|
| **Frontend** | Streamlit |
| **Backend / Language** | Python 3.8+ |
| **Database** | PostgreSQL |
| **DB Connector** | SQLAlchemy + psycopg2 |
| **Data Processing** | Polars |
| **ML Framework** | Scikit-learn |
| **NLP Model** | SentenceTransformers (`all-MiniLM-L6-v2`) |
| **Other Libraries** | re, itertools, typing |

---

## ⚙️ Installation

### Prerequisites

- Python 3.8 or above
- PostgreSQL 14+
- pgAdmin 4
- pip

### Step 1 — Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/snackbot-pro.git
cd snackbot-pro
```

### Step 2 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3 — Set Up PostgreSQL Database

Open pgAdmin 4 and run:

```sql
CREATE DATABASE snackbot_db;
```

Then create the menu table:

```sql
CREATE TABLE menu (
    id           SERIAL PRIMARY KEY,
    item_name    VARCHAR(200),
    category     VARCHAR(100),
    price        DECIMAL(10,2),
    availability VARCHAR(10),
    description  TEXT,
    timing       VARCHAR(100)
);
```

### Step 4 — Configure Database Connection

Open `app.py` and update:

```python
DB_URL = "postgresql://postgres:YOUR_PASSWORD@localhost:5432/snackbot_db"
```

### Step 5 — Run the Application

```bash
streamlit run app.py
```

Open your browser at: `http://localhost:8501`

---

## 📁 Project Structure

```
snackbot-pro/
│
├── 📄 app.py                    # Main Streamlit application
├── 📄 database.py               # PostgreSQL connection and queries
├── 📄 recommender.py            # ML recommendation engine
├── 📄 embeddings.py             # Sentence Transformer embeddings
├── 📄 combo_finder.py           # Budget-based combo logic
├── 📄 requirements.txt          # Python dependencies
├── 📁 data/
│   └── menu_data.csv            # Sample menu dataset
├── 📁 screenshots/
│   ├── home_screen.png
│   ├── chat_interface.png
│   ├── item_recommendation.png
│   ├── combo_result.png
│   └── alternative_suggestions.png
└── 📝 README.md
```

---

## 📸 Screenshots

### 🏠 Application Home Screen
> Clean chatbot interface with SnackBot Control panel
> <img width="1366" height="768" alt="Output 1" src="https://github.com/user-attachments/assets/4d569289-e4cc-4dfd-badc-71572ec48fc3" />


### 💬 Chat Interface
> Natural language query processing in real-time
> <img width="1366" height="768" alt="Output 2" src="https://github.com/user-attachments/assets/25b4f6b0-805f-40a8-a7c0-3b45c7865c93" />


### 🍽️ Item Recommendation Output
> Structured results showing dish name, category, price and availability
> <img width="1366" height="768" alt="Output 3" src="https://github.com/user-attachments/assets/b827d92a-281a-49cd-8f31-65e083692445" />


### 🎁 Combo Recommendation Result
> Best combo suggestions within user's specified budget
> <img width="1366" height="768" alt="Output 3" src="https://github.com/user-attachments/assets/26c2ec51-db00-4fe5-99e4-4d6863cc3169" />


### 🔄 Alternative Suggestions Screen
> Smart fallback — when no direct match found, semantic alternatives are shown
> <img width="1366" height="768" alt="Output 4" src="https://github.com/user-attachments/assets/ddfabb6c-3be1-4a07-80fd-9bf97cb89ce2" />


---

## 💡 Sample Queries to Try

```
"Paneer under 200"
"Combos for 150"
"Spicy snacks"
"Show burgers"
"Breakfast items"
"Drinks under 50"
"Combo for 250"
"Available items"
```

---

## 🔮 Future Enhancements

- 🛒 Online ordering and payment integration
- 👤 Personalized recommendations based on user history
- ☁️ Cloud deployment (AWS / Heroku / Streamlit Cloud)
- 🎙️ Voice-based query input
- 📊 Real-time menu updates and inventory management
- 🤖 Advanced transformer models for better NLP accuracy

---

## 📋 Hardware Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| Processor | Intel Core i3 | Intel Core i5 or higher |
| RAM | 4 GB | 8 GB or above |
| Storage | 10 GB free | 20 GB free |
| Architecture | 64-bit | 64-bit |
| Internet | Required | Required |

---

## 📦 requirements.txt

```
streamlit
pandas
polars
sqlalchemy
psycopg2-binary
scikit-learn
sentence-transformers
torch
```

---

## 👨‍💻 Author

**Rizwan T**
Reg. No.: 231DA146
B.Sc Computer Science with Data Analytics
Dr. N.G.P. Arts and Science College, Coimbatore
Affiliated to Bharathiar University

**Project Guide:** Dr. V. Santhana Lakshmi, M.Sc., M.Phil., Ph.D.
Associate Professor, Department of Computer Science with Data Analytics

📧 Connect: [https://www.linkedin.com/in/rizwan-t-dataanalyst/](https://www.linkedin.com/in/mohammad-rizwan-66345b362)
🐙 GitHub: [github.com/Rizwan877822](https://github.com/Rizwan877822)

---

## 📜 License

This project is submitted as a final year academic project.
MIT License — feel free to use and build upon this work.

---

<div align="center">

⭐ **If you found this project helpful, give it a star!** ⭐

*"Making food discovery intelligent — one query at a time"* 🍔🤖

</div>
