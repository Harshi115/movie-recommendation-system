# 🎬 Movie Recommender

A content-based movie recommender over the TMDB 5000 movies dataset. Pick a
movie you like, and it finds similar titles by comparing each movie's combined
tags (overview, genres, keywords, cast and crew) with cosine similarity over a
bag-of-words vectorization — no user ratings needed, so it works from the
very first search.

## Features

- **Search and recommend**: type any of the ~4,800 movies and get the most
  similar titles, with posters and an overview.
- **Surprise me**: a random pick plus its closest matches, for when you can't
  decide what to search for.
- **Favorites**: mark movies you like as you browse; they're listed in the
  sidebar for the rest of your session.
- **No setup required for posters**: they come from Wikipedia by default —
  no account, no API key. Add a TMDB key (see below) for ratings and release
  years too, and slightly more reliable artwork.

## Running it locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Open the URL Streamlit prints (usually `http://localhost:8501`).

### Posters and overviews

These work out of the box via Wikipedia — nothing to configure. Adding a
free [TMDB](https://www.themoviedb.org/settings/api) key additionally
brings in each movie's rating and release year, and TMDB's own artwork
(preferred over Wikipedia's when both are available). Once you have a key,
create `.streamlit/secrets.toml` (already gitignored) with:

```toml
TMDB_API_KEY = "your-key-here"
```

## Deploying

This is a stock Streamlit app, so it deploys the same way most anywhere:

- **Streamlit Community Cloud**: connect this repo at
  [share.streamlit.io](https://share.streamlit.io), set `app.py` as the entry
  point, and add `TMDB_API_KEY` under the app's Secrets.
- **Hugging Face Spaces**: create a Space with the Streamlit SDK, and push
  this repo to it; add `TMDB_API_KEY` under the Space's Settings → Variables
  and secrets.
- **Docker / any host**: `requirements.txt` has everything needed —
  `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`.

## How the recommendations work

`data/movie_dict.pkl` carries three columns per movie: `movie_id`, `title`,
and `tags` — a single pre-stemmed string combining the movie's overview,
genres, keywords, top cast and director. At startup, `app.py`:

1. Vectorizes `tags` with `CountVectorizer` (top 5,000 words, English stop
   words removed).
2. Computes a cosine-similarity matrix between every pair of movies.
3. For a chosen movie, returns the N movies with the highest similarity
   score (excluding the movie itself).

Both steps are cached (`@st.cache_data` / `@st.cache_resource`), so they run
once per app instance, not on every search.

## Project structure

```
app.py                  the whole app
data/movie_dict.pkl      movie_id + title + tags for ~4,800 movies
legacy/                 an earlier MySQL-backed login/register flow,
                         kept for reference — not wired into app.py, since
                         it needs a locally-running MySQL server and stored
                         passwords in plain text
requirements.txt
```

## Credits

Dataset: [TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)
(Kaggle). Poster art and metadata: [The Movie Database (TMDB)](https://www.themoviedb.org/).
This product uses the TMDB API but is not endorsed or certified by TMDB.
