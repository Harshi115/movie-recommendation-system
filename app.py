"""
Movie Recommender System
=========================

Content-based recommender over the TMDB 5000 movies dataset. Builds a
bag-of-words similarity matrix from each movie's combined tags (overview +
genres + keywords + cast + crew, already stemmed) and recommends the most
similar titles to whichever movie the user picks.

Posters and overviews come from The Movie Database (TMDB) API — optional: the
app runs fine without a key, just without artwork. Get a free key at
https://www.themoviedb.org/settings/api and set it as TMDB_API_KEY, either in
Streamlit Cloud's app secrets or a local .streamlit/secrets.toml.
"""

import os
import random

import pandas as pd
import requests
import streamlit as st
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "movie_dict.pkl")
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"
PLACEHOLDER_POSTER = "https://placehold.co/500x750?text=No+Poster"


def get_api_key() -> str | None:
    return st.secrets.get("TMDB_API_KEY", os.environ.get("TMDB_API_KEY"))


@st.cache_data
def load_movies() -> pd.DataFrame:
    movies = pd.DataFrame(pd.read_pickle(DATA_PATH))
    return movies.drop_duplicates(subset="movie_id").reset_index(drop=True)


@st.cache_resource
def build_similarity(tags: tuple[str, ...]):
    """Bag-of-words + cosine similarity over the tag corpus. Cached on the
    tuple of tags so Streamlit only rebuilds it once per dataset version."""
    vectors = CountVectorizer(max_features=5000, stop_words="english").fit_transform(tags)
    return cosine_similarity(vectors)


@st.cache_data(ttl=60 * 60 * 12, show_spinner=False)
def fetch_tmdb_details(movie_id: int) -> dict:
    """Poster + overview + rating for one movie, from TMDB. Empty dict (not
    an exception) on any failure, so a flaky network never breaks the page —
    callers just fall back to Wikipedia, then the placeholder poster."""
    api_key = get_api_key()
    if not api_key:
        return {}
    try:
        resp = requests.get(
            f"https://api.themoviedb.org/3/movie/{movie_id}",
            params={"api_key": api_key, "language": "en-US"},
            timeout=5,
        )
        resp.raise_for_status()
        data = resp.json()
        return {
            "poster_url": f"{TMDB_IMAGE_BASE}{data['poster_path']}" if data.get("poster_path") else None,
            "overview": data.get("overview"),
            "rating": data.get("vote_average"),
            "release_date": data.get("release_date"),
            "source_url": f"https://www.themoviedb.org/movie/{movie_id}",
        }
    except requests.RequestException:
        return {}


@st.cache_data(ttl=60 * 60 * 12, show_spinner=False)
def fetch_wikipedia_details(title: str) -> dict:
    """Poster + overview for one movie, from Wikipedia — no API key needed,
    used whenever TMDB_API_KEY isn't configured. Searching "<title> film"
    rather than the bare title steers Wikipedia's search past disambiguation
    pages toward the actual film article in most cases; an empty dict on any
    miss or network failure just means the placeholder poster is shown."""
    try:
        search = requests.get(
            "https://en.wikipedia.org/w/api.php",
            params={
                "action": "query",
                "list": "search",
                "srsearch": f"{title} film",
                "srlimit": 1,
                "format": "json",
            },
            headers={"User-Agent": "movie-recommender-streamlit-app/1.0"},
            timeout=5,
        )
        search.raise_for_status()
        results = search.json().get("query", {}).get("search", [])
        if not results:
            return {}
        page_title = results[0]["title"]

        summary = requests.get(
            f"https://en.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(page_title)}",
            headers={"User-Agent": "movie-recommender-streamlit-app/1.0"},
            timeout=5,
        )
        summary.raise_for_status()
        data = summary.json()
        return {
            "poster_url": data.get("thumbnail", {}).get("source"),
            "overview": data.get("extract"),
            "source_url": data.get("content_urls", {}).get("desktop", {}).get("page"),
        }
    except requests.RequestException:
        return {}


def fetch_movie_details(movie_id: int, title: str) -> dict:
    """TMDB first (richer: rating, release date) when a key is configured,
    otherwise Wikipedia — both are keyless-safe, so there's always a best
    available answer rather than an all-or-nothing poster feature."""
    details = fetch_tmdb_details(movie_id)
    if details.get("poster_url"):
        return details
    return fetch_wikipedia_details(title) or details


def recommend(movies: pd.DataFrame, similarity, title: str, count: int) -> list[int]:
    """Row indices of the `count` movies most similar to `title`, excluding itself."""
    index = movies[movies["title"] == title].index[0]
    scored = sorted(enumerate(similarity[index]), key=lambda x: x[1], reverse=True)
    return [i for i, _ in scored[1 : count + 1]]


def render_movie_card(column, movies: pd.DataFrame, row_index: int):
    row = movies.iloc[row_index]
    details = fetch_movie_details(int(row["movie_id"]), row["title"])
    with column:
        st.image(details.get("poster_url") or PLACEHOLDER_POSTER, use_container_width=True)
        title_line = row["title"]
        if details.get("source_url"):
            title_line = f"[{title_line}]({details['source_url']})"
        st.markdown(f"**{title_line}**")
        meta_bits = []
        if details.get("rating"):
            meta_bits.append(f"⭐ {details['rating']:.1f}")
        if details.get("release_date"):
            meta_bits.append(details["release_date"][:4])
        if meta_bits:
            st.caption(" · ".join(meta_bits))
        if details.get("overview"):
            with st.expander("Overview"):
                st.write(details["overview"])
        if st.button("♥ Favorite", key=f"fav-{row_index}"):
            st.session_state.favorites.add(row["title"])
            st.toast(f"Added {row['title']} to favorites")


def main():
    movies = load_movies()
    similarity = build_similarity(tuple(movies["tags"]))
    st.session_state.setdefault("favorites", set())

    st.title("🎬 Movie Recommender")
    st.caption(f"Content-based recommendations over {len(movies):,} movies, by similar plot, genre and cast.")

    if not get_api_key():
        st.caption(
            "🔑 Posters are pulled from Wikipedia right now. Add a free TMDB_API_KEY to this "
            "app's secrets for ratings, release years and more reliable artwork."
        )

    with st.sidebar:
        st.header("Options")
        count = st.slider("Recommendations to show", min_value=3, max_value=15, value=5)
        st.divider()
        st.subheader("Favorites")
        if st.session_state.favorites:
            for fav in sorted(st.session_state.favorites):
                st.write(f"- {fav}")
        else:
            st.caption("Nothing favorited yet.")

    tab_recommend, tab_surprise = st.tabs(["Find similar movies", "Surprise me"])

    with tab_recommend:
        selected_title = st.selectbox(
            "Pick a movie you like",
            movies["title"].values,
            index=None,
            placeholder="Start typing a title…",
        )
        if selected_title and st.button("Recommend", type="primary"):
            indices = recommend(movies, similarity, selected_title, count)
            columns = st.columns(min(count, 5))
            for position, row_index in enumerate(indices):
                render_movie_card(columns[position % len(columns)], movies, row_index)

    with tab_surprise:
        st.write("Can't decide? Get a random pick and its closest matches.")
        if st.button("🎲 Surprise me"):
            st.session_state.surprise_title = random.choice(movies["title"].values)
        surprise_title = st.session_state.get("surprise_title")
        if surprise_title:
            st.subheader(surprise_title)
            indices = recommend(movies, similarity, surprise_title, count)
            columns = st.columns(min(count, 5))
            for position, row_index in enumerate(indices):
                render_movie_card(columns[position % len(columns)], movies, row_index)


if __name__ == "__main__":
    main()
