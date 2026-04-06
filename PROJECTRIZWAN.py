import streamlit as st
import polars as pl
import re
import itertools
from sqlalchemy import create_engine
from sentence_transformers import SentenceTransformer
from sklearn.neighbors import NearestNeighbors
from typing import Dict, List

# ---------------- Configuration ----------------
st.set_page_config(page_title="🍔 SnackBot Pro", page_icon="🍔", layout="wide")

DB_URL = "postgresql+psycopg2://postgres:rizwan@localhost:5432/rizwan"
EMBED_MODEL = "all-MiniLM-L6-v2"


# ---------------- Data Engine ----------------
@st.cache_data(ttl=300)
def load_and_clean_data() -> pl.DataFrame:
    engine = create_engine(DB_URL)
    try:
        with engine.connect() as conn:
            df = pl.read_database("SELECT * FROM menu", connection=conn)
    except Exception as e:
        st.error(f"Database Connection Failed: {e}")
        return pl.DataFrame()

    df = df.with_columns([
        pl.col("item_name").fill_null("Unknown Item"),
        pl.col("price").cast(pl.Float64).fill_null(0.0),
        pl.col("category").fill_null("General"),
        pl.col("availability").str.to_lowercase().fill_null("no"),
        pl.col("description").fill_null("No description available.")
    ])

    df = df.with_columns(
        pl.col("item_name").str.to_lowercase().alias("name_match")
    )
    return df


MENU_DF = load_and_clean_data()


@st.cache_resource
def get_search_tools(data_list: List[str]):
    model = SentenceTransformer(EMBED_MODEL)
    embeddings = model.encode(data_list, convert_to_numpy=True)
    nn = NearestNeighbors(metric="cosine").fit(embeddings)
    return model, nn


# ---------------- Search Logic ----------------
def find_best_combos(budget: float, k: int = 3):
    available_items = MENU_DF.filter(pl.col("availability") == "yes").to_dicts()
    combos = []
    for i1, i2 in itertools.combinations(available_items, 2):
        total = i1["price"] + i2["price"]
        if total <= budget:
            utilization = total / budget
            combos.append({"items": (i1, i2), "total": total, "score": utilization})
    return sorted(combos, key=lambda x: x["score"], reverse=True)[:k]


def run_smart_query(user_query: str, max_results: int, available_only: bool):
    q = user_query.lower().strip()
    data = MENU_DF
    if available_only:
        data = data.filter(pl.col("availability") == "yes")

    if data.is_empty():
        return {"intent": "empty", "data": [], "term": q}

    # 1. Check for Combos
    price_found = re.search(r"(\d+)", q)
    limit = float(price_found.group(1)) if price_found else None
    if any(word in q for word in ["combo", "pair", "deal", "together"]) and limit:
        return {"intent": "combo", "data": find_best_combos(limit, max_results)}

    # 2. Semantic Search (Better than Exact Search)
    clean_keyword = re.sub(r"(under|below|for|combo|deal|items|food|show)\s*\d*", "", q).strip()

    data_dicts = data.to_dicts()
    # We combine name, category, and description for the best semantic match
    texts = [f"{i['item_name']} {i['category']} {i['description']}" for i in data_dicts]

    model, nn = get_search_tools(texts)
    q_emb = model.encode([q])

    n_to_fetch = min(max_results, len(data_dicts))
    distances, indices = nn.kneighbors(q_emb, n_neighbors=n_to_fetch)

    # Filter results by price limit if provided
    final_results = []
    for idx in indices[0]:
        item = data_dicts[idx]
        if limit is None or item['price'] <= limit:
            final_results.append(item)

    return {"intent": "search", "data": final_results, "term": clean_keyword}


# ---------------- Sidebar ----------------
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/hamburger.png", width=80)
    st.title("⚙️ SnackBot Control")
    st.divider()
    k_slider = st.select_slider("Results density", options=[1, 3, 5, 10], value=5)
    only_available = st.toggle("Show Available Only", value=True)
    st.divider()
    if st.button("🗑️ Reset Conversation", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

# ---------------- Main UI ----------------
st.title("🍔 SnackBot Pro")
st.caption("Intelligent food recommendations at your fingertips.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for chat in st.session_state.chat_history:
    avatar = "👤" if chat["role"] == "user" else "🍔"
    with st.chat_message(chat["role"], avatar=avatar):
        st.markdown(chat["content"])

prompt = st.chat_input("Hungry? Ask for 'paneer under 200' or 'combos for 150'")

if prompt:
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🍔"):
        with st.status("🔍 Searching the menu...", expanded=True) as status:
            result = run_smart_query(prompt, k_slider, only_available)
            status.update(label="✅ Recommendations Ready!", state="complete", expanded=False)

        response_content = ""

        if result["intent"] == "empty" or not result["data"]:
            st.info(f"I couldn't find any available items matching '{prompt}'.")
            response_content = "No results found."

        elif result["intent"] == "combo":
            for combo in result["data"]:
                with st.container(border=True):
                    item0, item1 = combo['items'][0], combo['items'][1]
                    item_details = f"**{item0['item_name']}** + **{item1['item_name']}**"
                    c1, c2 = st.columns([5, 1], vertical_alignment="center")
                    c1.markdown(item_details)
                    c2.metric("Total", f"₹{int(combo['total'])}")
                    response_content += f"{item_details} - Total: ₹{int(combo['total'])}\n\n"

        elif result["intent"] == "search":
            for item in result["data"]:
                with st.container(border=True):
                    col1, col2, col3 = st.columns([3, 2, 1], vertical_alignment="center")
                    col1.markdown(f"**{item['item_name']}**")
                    col1.caption(item['description'])
                    col2.write(f"📁 {item['category']}")
                    col3.metric("Price", f"₹{int(item['price'])}")
                    response_content += f"**{item['item_name']}** - ₹{int(item['price'])}\n\n"

    st.session_state.chat_history.append({"role": "assistant", "content": response_content})