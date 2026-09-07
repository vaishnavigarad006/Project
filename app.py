from pathlib import Path

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "ml-100k"


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Movie Ratings & Streaming Trends",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================
# ============================================================
# THEME
# ============================================================

theme = st.sidebar.selectbox(
    "🎨 Dashboard Theme",
    ["Light", "Dark"],
    key="dashboard_theme"
)

if theme == "Dark":

    background = "#0E1117"
    text = "#FFFFFF"
    card = "#1A1F2B"
    border = "#30363D"

else:

    background = "#FFFFFF"
    text = "#111111"
    card = "#F7F7F7"
    border = "#DDDDDD"


st.markdown(
    f"""
    <style>

    .stApp {{
        background-color: {background};
        color: {text};
    }}

    .main-title {{
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }}

    .subtitle {{
        font-size: 18px;
        opacity: 0.7;
        margin-bottom: 25px;
    }}

    .metric-card {{
        background-color: {card};
        border: 1px solid {border};
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;
    }}

    .metric-title {{
        font-size: 16px;
        opacity: 0.7;
    }}

    .metric-value {{
        font-size: 30px;
        font-weight: 700;
    }}

    .section-title {{
        font-size: 28px;
        font-weight: 600;
        margin-top: 20px;
        margin-bottom: 15px;
    }}

    [data-testid="stMetric"] {{
        background-color: {card};
        border: 1px solid {border};
        padding: 15px;
        border-radius: 15px;
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    ratings_path = DATA_DIR / "u.data"
    movies_path = DATA_DIR / "u.item"

    if not ratings_path.exists():
        raise FileNotFoundError(f"Dataset not found: {ratings_path}")

    if not movies_path.exists():
        raise FileNotFoundError(f"Dataset not found: {movies_path}")

    # -----------------------------
    # Ratings
    # -----------------------------

    ratings = pd.read_csv(
        ratings_path,
        sep="\t",
        names=[
            "user_id",
            "movie_id",
            "rating",
            "timestamp"
        ]
    )

    # -----------------------------
    # Movie / Genre columns
    # -----------------------------

    genre_columns = [
        "unknown",
        "Action",
        "Adventure",
        "Animation",
        "Children's",
        "Comedy",
        "Crime",
        "Documentary",
        "Drama",
        "Fantasy",
        "Film-Noir",
        "Horror",
        "Musical",
        "Mystery",
        "Romance",
        "Sci-Fi",
        "Thriller",
        "War",
        "Western"
    ]

    movie_columns = [
        "movie_id",
        "title",
        "release_date",
        "video_release_date",
        "IMDb_URL"
    ] + genre_columns

    # -----------------------------
    # Movies
    # -----------------------------

    movies = pd.read_csv(
        movies_path,
        sep="|",
        encoding="latin-1",
        header=None,
        names=movie_columns
    )

    # -----------------------------
    # Merge
    # -----------------------------

    data = ratings.merge(
        movies,
        on="movie_id"
    )

    # -----------------------------
    # Extract release year
    # -----------------------------

    data["year"] = pd.to_numeric(
        data["title"].str.extract(r"\((\d{4})\)")[0],
        errors="coerce"
    )

    movies["year"] = pd.to_numeric(
        movies["title"].str.extract(r"\((\d{4})\)")[0],
        errors="coerce"
    )

    return ratings, movies, data, genre_columns


ratings, movies, data, genre_columns = load_data()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🎬 Movie Dashboard")

git --versionst.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate to:",
    [
        "🏠 Overview",
        "📊 Ratings",
        "🎭 Genres",
        "📈 Trends",
        "🔎 Search",
        "🤖 Recommendations"
    ]
)


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.markdown("---")
st.sidebar.header("🎛️ Dashboard Filters")


# Minimum rating

min_rating = st.sidebar.slider(
    "Minimum Rating ⭐",
    min_value=1,
    max_value=5,
    value=1
)


# Genre filter

genre_options = ["All Genres"] + genre_columns

selected_genre = st.sidebar.selectbox(
    "Select Genre 🎭",
    genre_options
)


# Year filter

valid_years = sorted(
    data["year"].dropna().astype(int).unique()
)

if len(valid_years) > 0:

    year_range = st.sidebar.slider(
        "Release Year 📅",
        min_value=int(min(valid_years)),
        max_value=int(max(valid_years)),
        value=(
            int(min(valid_years)),
            int(max(valid_years))
        )
    )

else:

    year_range = None




# ============================================================
# APPLY FILTERS
# ============================================================

filtered_data = data[
    data["rating"] >= min_rating
].copy()


# Genre filter

if selected_genre != "All Genres":

    filtered_data = filtered_data[
        filtered_data[selected_genre] == 1
    ]


# Year filter

if year_range is not None:

    filtered_data = filtered_data[
        filtered_data["year"].between(
            year_range[0],
            year_range[1]
        )
    ]


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🎬 Movie Ratings & Streaming Trends</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Interactive analysis of the MovieLens 100K dataset</div>',
    unsafe_allow_html=True
)


# ============================================================
# OVERVIEW PAGE
# ============================================================

if page == "🏠 Overview":

    st.markdown(
        '<div class="section-title">📌 Dashboard Overview</div>',
        unsafe_allow_html=True
    )

    # ============================================================
# KEY INSIGHTS
# ============================================================

st.divider()

st.subheader("💡 Key Insights")

if not filtered_data.empty:

    # -----------------------------
    # Most Popular Genre
    # -----------------------------

    genre_counts = {}

    for genre in genre_columns:
        genre_counts[genre] = (
            filtered_data[genre] == 1
        ).sum()

    popular_genre = max(
        genre_counts,
        key=genre_counts.get
    )

    popular_genre_count = genre_counts[popular_genre]

    # -----------------------------
    # Highest Rated Genre
    # -----------------------------

    genre_avg = {}

    for genre in genre_columns:

        genre_data = filtered_data[
            filtered_data[genre] == 1
        ]["rating"]

        if len(genre_data) > 0:
            genre_avg[genre] = genre_data.mean()

    if genre_avg:

        best_genre = max(
            genre_avg,
            key=genre_avg.get
        )

        best_genre_rating = genre_avg[best_genre]

    else:

        best_genre = "N/A"
        best_genre_rating = 0

    # -----------------------------
    # Most Rated Movie
    # -----------------------------

    movie_rating_counts = (
        filtered_data
        .groupby("title")
        .size()
    )

    if not movie_rating_counts.empty:

        most_rated_movie = (
            movie_rating_counts
            .idxmax()
        )

        most_rated_count = (
            movie_rating_counts
            .max()
        )

    else:

        most_rated_movie = "N/A"
        most_rated_count = 0

    # -----------------------------
    # Highest Rated Movie
    # -----------------------------

    movie_stats = (
        filtered_data
        .groupby("title")["rating"]
        .agg(
            Ratings="count",
            Average_Rating="mean"
        )
    )

    movie_stats = movie_stats[
        movie_stats["Ratings"] >= 20
    ]

    if not movie_stats.empty:

        best_movie = (
            movie_stats
            .sort_values(
                "Average_Rating",
                ascending=False
            )
            .index[0]
        )

        best_movie_rating = (
            movie_stats
            .loc[
                best_movie,
                "Average_Rating"
            ]
        )

    else:

        best_movie = "N/A"
        best_movie_rating = 0

    # -----------------------------
    # Most Active Year
    # -----------------------------

    year_counts = (
        filtered_data
        .dropna(subset=["year"])
        .groupby("year")
        .size()
    )

    if not year_counts.empty:

        active_year = int(
            year_counts.idxmax()
        )

        active_year_count = (
            year_counts.max()
        )

    else:

        active_year = "N/A"
        active_year_count = 0

    # -----------------------------
    # Display Insights
    # -----------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.info(
            f"🎭 **Most Popular Genre**\n\n"
            f"{popular_genre} — "
            f"{popular_genre_count:,} ratings"
        )

        st.success(
            f"⭐ **Highest Rated Genre**\n\n"
            f"{best_genre} — "
            f"{best_genre_rating:.2f} ⭐"
        )

        st.warning(
            f"🔥 **Most Rated Movie**\n\n"
            f"{most_rated_movie} — "
            f"{most_rated_count:,} ratings"
        )

    with col2:

        st.success(
            f"🏆 **Highest Rated Movie**\n\n"
            f"{best_movie} — "
            f"{best_movie_rating:.2f} ⭐"
        )

        st.info(
            f"📅 **Most Active Release Year**\n\n"
            f"{active_year} — "
            f"{active_year_count:,} ratings"
        )

        st.write(
            "💡 **Dashboard Insight:** "
            "Use the sidebar filters to explore how "
            "ratings and movie popularity change across "
            "different genres and years."
        )

    # -----------------------------
    # Metrics
    # -----------------------------

    total_movies = filtered_data["movie_id"].nunique()

    total_users = filtered_data["user_id"].nunique()

    total_ratings = len(filtered_data)

    average_rating = (
        filtered_data["rating"].mean()
        if len(filtered_data) > 0
        else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "🎥 Total Movies",
        f"{total_movies:,}"
    )

    col2.metric(
        "👥 Total Users",
        f"{total_users:,}"
    )

    col3.metric(
        "📝 Total Ratings",
        f"{total_ratings:,}"
    )

    col4.metric(
        "⭐ Average Rating",
        f"{average_rating:.2f}"
    )

    st.divider()

    # -----------------------------
    # Rating Distribution
    # -----------------------------

    st.subheader("📊 Rating Distribution")

    if not filtered_data.empty:

        rating_counts = (
            filtered_data["rating"]
            .value_counts()
            .sort_index()
            .reset_index()
        )

        rating_counts.columns = [
            "Rating",
            "Number of Ratings"
        ]

        fig = px.bar(
            rating_counts,
            x="Rating",
            y="Number of Ratings",
            title="Distribution of Movie Ratings",
            text="Number of Ratings"
        )

        fig.update_layout(
            xaxis=dict(
                tickmode="linear",
                dtick=1
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.warning("No ratings match the selected filters.")


    # -----------------------------
    # Top movies
    # -----------------------------

    st.subheader("🏆 Top Rated Movies")

    if not filtered_data.empty:

        movie_ratings = (
            filtered_data
            .groupby("title")["rating"]
            .agg(
                Ratings="count",
                Average_Rating="mean"
            )
        )

        popular_movies = movie_ratings[
            movie_ratings["Ratings"] >= 20
        ]

        top_movies = (
            popular_movies
            .sort_values(
                "Average_Rating",
                ascending=False
            )
            .head(10)
            .reset_index()
        )

        top_movies["Average_Rating"] = (
            top_movies["Average_Rating"].round(2)
        )

        st.dataframe(
            top_movies,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# RATINGS PAGE
# ============================================================

elif page == "📊 Ratings":

    st.markdown(
        '<div class="section-title">📊 Rating Analysis</div>',
        unsafe_allow_html=True
    )

    # -----------------------------
    # Rating metrics
    # -----------------------------

    if filtered_data.empty:

        st.warning("No data available for the selected filters.")

    else:

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Highest Rating",
            f"{filtered_data['rating'].max()} ⭐"
        )

        col2.metric(
            "Lowest Rating",
            f"{filtered_data['rating'].min()} ⭐"
        )

        col3.metric(
            "Average Rating",
            f"{filtered_data['rating'].mean():.2f} ⭐"
        )

        st.divider()

        # -----------------------------
        # Rating Distribution
        # -----------------------------

        rating_counts = (
            filtered_data["rating"]
            .value_counts()
            .sort_index()
            .reset_index()
        )

        rating_counts.columns = [
            "Rating",
            "Count"
        ]

        fig = px.bar(
            rating_counts,
            x="Rating",
            y="Count",
            title="Rating Distribution",
            text="Count"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # -----------------------------
        # Most Rated Movies
        # -----------------------------

        st.subheader("🔥 Most Rated Movies")

        most_rated = (
            filtered_data
            .groupby("title")
            .size()
            .sort_values(
                ascending=False
            )
            .head(10)
            .reset_index(name="Ratings")
        )

        fig = px.bar(
            most_rated,
            x="Ratings",
            y="title",
            orientation="h",
            title="Top 10 Most Rated Movies"
        )

        fig.update_layout(
            yaxis=dict(
                categoryorder="total ascending"
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # -----------------------------
        # Top Rated Movies
        # -----------------------------

        st.subheader("🏆 Highest Rated Movies")

        movie_stats = (
            filtered_data
            .groupby("title")["rating"]
            .agg(
                Ratings="count",
                Average_Rating="mean"
            )
        )

        movie_stats = movie_stats[
            movie_stats["Ratings"] >= 20
        ]

        top_rated = (
            movie_stats
            .sort_values(
                "Average_Rating",
                ascending=False
            )
            .head(10)
            .reset_index()
        )

        top_rated["Average_Rating"] = (
            top_rated["Average_Rating"].round(2)
        )

        st.dataframe(
            top_rated,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# GENRE PAGE
# ============================================================

elif page == "🎭 Genres":

    st.markdown(
        '<div class="section-title">🎭 Genre Analysis</div>',
        unsafe_allow_html=True
    )

    # -----------------------------
    # Genre popularity
    # -----------------------------

    genre_counts = {}

    for genre in genre_columns:

        count = filtered_data[
            filtered_data[genre] == 1
        ]["rating"].count()

        genre_counts[genre] = count

    genre_counts = (
        pd.Series(genre_counts)
        .sort_values(ascending=False)
        .reset_index()
    )

    genre_counts.columns = [
        "Genre",
        "Ratings"
    ]

    st.subheader("🔥 Genre Popularity")

    fig = px.bar(
        genre_counts,
        x="Genre",
        y="Ratings",
        title="Ratings by Genre"
    )

    fig.update_layout(
        xaxis_tickangle=-45
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # -----------------------------
    # Average genre rating
    # -----------------------------

    genre_average = {}

    for genre in genre_columns:

        genre_data = filtered_data[
            filtered_data[genre] == 1
        ]["rating"]

        if len(genre_data) > 0:

            genre_average[genre] = genre_data.mean()

        else:

            genre_average[genre] = 0

    genre_average = (
        pd.Series(genre_average)
        .sort_values(ascending=False)
        .reset_index()
    )

    genre_average.columns = [
        "Genre",
        "Average Rating"
    ]

    genre_average["Average Rating"] = (
        genre_average["Average Rating"].round(2)
    )

    st.subheader("⭐ Average Rating by Genre")

    fig = px.bar(
        genre_average,
        x="Genre",
        y="Average Rating",
        title="Average Rating by Genre",
        text="Average Rating"
    )

    fig.update_layout(
        xaxis_tickangle=-45
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# TRENDS PAGE
# ============================================================

elif page == "📈 Trends":

    st.markdown(
        '<div class="section-title">📈 Movie Trends</div>',
        unsafe_allow_html=True
    )

    # -----------------------------
    # Movies released by year
    # -----------------------------

    movies_per_year = (
        movies
        .dropna(subset=["year"])
        .groupby("year")
        .size()
        .reset_index(name="Movies")
    )

    st.subheader("🎬 Movies Released Over the Years")

    fig = px.line(
        movies_per_year,
        x="year",
        y="Movies",
        markers=True,
        title="Number of Movies Released by Year"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # -----------------------------
    # Ratings by year
    # -----------------------------

    ratings_year = (
        filtered_data
        .dropna(subset=["year"])
        .groupby("year")
        .size()
        .reset_index(name="Ratings")
    )

    st.subheader("📝 Ratings Activity Over Time")

    fig = px.line(
        ratings_year,
        x="year",
        y="Ratings",
        markers=True,
        title="Number of Ratings by Movie Release Year"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # -----------------------------
    # Average rating by year
    # -----------------------------

    average_year = (
        filtered_data
        .dropna(subset=["year"])
        .groupby("year")["rating"]
        .mean()
        .reset_index()
    )

    average_year.columns = [
        "Year",
        "Average Rating"
    ]

    st.subheader("⭐ Average Rating Trend")

    fig = px.line(
        average_year,
        x="Year",
        y="Average Rating",
        markers=True,
        title="Average Rating by Year"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# SEARCH PAGE
# ============================================================

elif page == "🔎 Search":

    st.markdown(
        '<div class="section-title">🔎 Movie Search</div>',
        unsafe_allow_html=True
    )

    search = st.text_input(
        "Enter movie name:",
        placeholder="Example: Toy Story"
    )

    if search:

        search_results = data[
            data["title"].str.contains(
                search,
                case=False,
                na=False
            )
        ]

        if not search_results.empty:

            movie_summary = (
                search_results
                .groupby("title")
                .agg(
                    Ratings=("rating", "count"),
                    Average_Rating=("rating", "mean")
                )
                .sort_values(
                    "Average_Rating",
                    ascending=False
                )
            )

            movie_summary["Average_Rating"] = (
                movie_summary["Average_Rating"].round(2)
            )

            st.success(
                f"{len(movie_summary)} movie(s) found."
            )

            st.dataframe(
                movie_summary,
                use_container_width=True
            )

            # -----------------------------
            # Movie selection
            # -----------------------------

            selected_search_movie = st.selectbox(
                "Select a movie to view details:",
                movie_summary.index.tolist()
            )

            movie_data = data[
                data["title"] == selected_search_movie
            ]

            if not movie_data.empty:

                avg_rating = movie_data["rating"].mean()

                rating_count = len(movie_data)

                st.divider()

                col1, col2 = st.columns(2)

                col1.metric(
                    "⭐ Average Rating",
                    f"{avg_rating:.2f}"
                )

                col2.metric(
                    "📝 Number of Ratings",
                    f"{rating_count:,}"
                )

                st.subheader("Rating Distribution")

                selected_ratings = (
                    movie_data["rating"]
                    .value_counts()
                    .sort_index()
                    .reset_index()
                )

                selected_ratings.columns = [
                    "Rating",
                    "Count"
                ]

                fig = px.bar(
                    selected_ratings,
                    x="Rating",
                    y="Count",
                    title=f"Ratings for {selected_search_movie}"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

        else:

            st.warning(
                "No movie found. Try another search."
            )

    else:

        st.info(
            "Enter a movie name above to search the dataset."
        )


# ============================================================
# RECOMMENDATION PAGE
# ============================================================

elif page == "🤖 Recommendations":

    st.markdown(
        '<div class="section-title">🤖 Movie Recommendation System</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Select a movie and get recommendations based on "
        "shared movie genres."
    )

    movie_list = sorted(
        movies["title"]
        .dropna()
        .unique()
    )

    selected_movie = st.selectbox(
        "🎬 Select a movie:",
        movie_list
    )

    number_of_recommendations = st.slider(
        "Number of recommendations:",
        min_value=5,
        max_value=20,
        value=10
    )

    if st.button(
        "🚀 Recommend Movies",
        use_container_width=True
    ):

        selected_row = movies[
            movies["title"] == selected_movie
        ]

        if not selected_row.empty:

            selected_genres = (
                selected_row.iloc[0][genre_columns]
                .values
            )

            similarity_scores = []

            for _, movie in movies.iterrows():

                movie_genres = (
                    movie[genre_columns]
                    .values
                )

                similarity = sum(
                    selected_genres[i] == 1
                    and movie_genres[i] == 1
                    for i in range(len(genre_columns))
                )

                similarity_scores.append(
                    similarity
                )

            movies_copy = movies.copy()

            movies_copy["similarity"] = (
                similarity_scores
            )

            recommendations = (
                movies_copy[
                    movies_copy["title"] != selected_movie
                ]
                .sort_values(
                    "similarity",
                    ascending=False
                )
                .head(number_of_recommendations)
            )

            recommendations = recommendations[
                recommendations["similarity"] > 0
            ]

            st.subheader(
                f"🎯 Movies similar to {selected_movie}"
            )

            if not recommendations.empty:

                display_recommendations = (
                    recommendations[
                        [
                            "title",
                            "year",
                            "similarity"
                        ]
                    ]
                    .rename(
                        columns={
                            "title": "Movie",
                            "year": "Release Year",
                            "similarity": "Genre Similarity"
                        }
                    )
                )

                st.dataframe(
                    display_recommendations,
                    use_container_width=True,
                    hide_index=True
                )

            else:

                st.warning(
                    "No similar movies were found."
                )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🎬 Movie Ratings & Streaming Trends | "
    "Built with Python, Pandas, Plotly and Streamlit"
)