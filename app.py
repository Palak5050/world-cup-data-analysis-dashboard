import streamlit as st
import pandas as pd
import plotly.express as px
import random
from chatbot import get_reply


# -------------------------------------------------
# Helper for shades
# -------------------------------------------------
def get_shade_color(shades):
    return random.choice(shades)

def apply_dark_theme(fig, show_legend=True):

    # Transparent background + global white color
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="white"),
        showlegend=show_legend,

        # Chart Title (Center + Bold + White)
        title=dict(
            x=0.5,  # center align
            xanchor="center",
            font=dict(
                color="lavender",
                size=20,
                family="Arial Black"
            )
        ),

        # Legend styling (if enabled)
        legend=dict(
            font=dict(color="white"),
            bgcolor='rgba(0,0,0,0)'
        ),
    )

    # X-axis styling
    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        title_font=dict(color="white", size=15, family="Arial Black"),
        tickfont=dict(color="white", size=13, family="Arial"),
    )

    # Y-axis styling
    fig.update_yaxes(
        showgrid=False,
        zeroline=False,
        title_font=dict(color="white", size=15, family="Arial Black"),
        tickfont=dict(color="white", size=13, family="Arial"),
    )

    return fig

# -------------------------------------------------
# Page Setup + Basic Theming
# -------------------------------------------------
st.set_page_config(
    page_title="World Cup Analysis",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown("""
<style>
/* GLOBAL */
html, body, [data-testid="stAppViewContainer"] {
    color:#e0f2fe !important;
    background:transparent !important;
    text-shadow:0 0 6px rgba(0,0,0,0.5) !important;
}
body, p, h1, h2, h3, h4, h5, h6 {color:#e0f2fe !important;}
strong, b {color:#f0f9ff !important;}

/* TABS */
.stTabs [data-baseweb="tab"] {
    background:rgba(255,255,255,0.08) !important;
    border-radius:8px !important;
    color:#dbeafe !important;
    font-weight:600 !important;
    margin-right:6px !important;
    padding:8px 16px !important;
    backdrop-filter:blur(8px) !important;
    border:1px solid rgba(148,163,184,0.3) !important;
}
.stTabs [data-baseweb="tab"]:hover {
    border-color:rgba(191,219,254,0.8) !important;
}
.stTabs [aria-selected="true"] {
    background:rgba(37,99,235,0.9) !important;
    color:#fff !important;
    border-bottom:3px solid #e0f2fe !important;
    box-shadow:0 0 12px rgba(37,99,235,0.8) !important;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background:rgba(0,0,0,0.55) !important;
    backdrop-filter:blur(10px) !important;
    color:#e2e8f0 !important;
    border-right:1px solid rgba(148,163,184,0.4) !important;
}
section[data-testid="stSidebar"] * {color:#e2e8f0 !important;}

/* TEXT INPUTS */
.stTextInput > div > div > input {
    background:rgba(255,255,255,0.25) !important;
    color:#000 !important;
    border-radius:10px !important;
    border:1px solid rgba(255,255,255,0.3) !important;
    backdrop-filter:blur(10px) !important;
    padding:10px 14px !important;
    font-weight:600 !important;
}
.stTextInput > div > div > input::placeholder {
    color:rgba(15,23,42,0.7) !important;
}

/* SELECTBOX & MULTISELECT */
.stSelectbox > div,
div[data-testid="stMultiSelect"] > div {
    background:rgba(255,255,255,0.25) !important;
    backdrop-filter:blur(12px) !important;
    border-radius:10px !important;
    border:1px solid rgba(255,255,255,0.35) !important;
}
.stSelectbox span,
div[data-testid="stMultiSelect"] span {
    color:#000 !important;
    font-weight:600 !important;
}
div[role="listbox"] {
    background:rgba(255,255,255,0.95) !important;
    color:#000 !important;
    border-radius:12px !important;
    backdrop-filter:blur(14px) !important;
    box-shadow:0 10px 25px rgba(15,23,42,0.4);
}
div[role="option"] {
    color:#000 !important;
    padding:10px 14px !important;
    font-size:15px !important;
    font-weight:500 !important;
}

/* BUTTONS */
.stButton > button {
    background:rgba(37,99,235,0.9) !important;
    color:#e0f2fe !important;
    border-radius:10px !important;
    border:1px solid rgba(255,255,255,0.25) !important;
    padding:8px 18px !important;
    font-weight:600 !important;
    box-shadow:0 0 12px rgba(37,99,235,0.7);
    backdrop-filter:blur(6px);
}
.stButton > button:hover {
    background:rgba(59,130,246,0.98) !important;
    box-shadow:0 0 15px rgba(59,130,246,0.9);
}

/* SECTION TITLES */
div.section-title {
    font-size:22px;
    font-weight:700;
    margin-bottom:8px;
    color:#fff !important;
    text-shadow:0 0 8px rgba(15,23,42,0.8);
}

/* MARKDOWN + CAPTION */
div.stMarkdown, div.stMarkdown p, div.stMarkdown span {color:#e0f2fe !important;}
.stCaption, .stCaption p {color:#e5e7eb !important;}

/* ALERTS */
div[data-testid="stAlert"] {border-radius:10px !important;}

/* LAYOUT */
.block-container {padding-top:2rem;}
section.main > div {background:transparent !important;}

/* PLOTLY FONT */
.js-plotly-plot .plotly .main-svg {
    font-family:"Arial",sans-serif !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown(r"""
    <style>
    .stApp {
        background-image: url("https://i.imgur.com/pJ7MkhI.jpeg");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚽ World Cup Analysis Application", anchor=False)
st.markdown(
    '<div class="subtitle">Interactive FIFA World Cup insights with dashboards, visuals and stats.</div>',
    unsafe_allow_html=True,
)
st.write("")

# -------------------------------------------------
# Load Data
# -------------------------------------------------
try:
    df = pd.read_excel("world_cup_results.xlsx")

    df["Total_Goals_in_Match"] = df["Team G"] + df["Opponent G"]

    match_df = df.drop_duplicates(subset=["Year", "Game #"]).copy()
    match_df["Total_Goals_in_Match"] = match_df["Team G"] + match_df["Opponent G"]

    st.success("✅ Data loaded successfully!")
except Exception as e:
    st.error(f"❌ Error loading data: {e}")
    st.stop()

# KPIs (overall)
total_matches = len(match_df)
total_years = match_df["Year"].nunique()
total_teams = df["Team"].nunique()
total_goals = int(match_df["Total_Goals_in_Match"].sum())

# -------------------------------------------------
# Sidebar – Questions (Q1–Q6)
# -------------------------------------------------
st.sidebar.title("📌 Questions")
question = st.sidebar.radio(
    "Select Question for Visuals",
    (
        "Q1: Top Hosting Nations",
        "Q2: Stadium Match Frequency",
        "Q3: Goals Over Time",
        "Q4: Highest Goals Conceded",
        "Q5: Goal-Rich Stadiums",
        "Q6: Round Match Density",
    ),
)
st.sidebar.markdown("---")
st.sidebar.caption("Tip: Use Dashboard tab for filters.")

# -------------------------------------------------
# Login state
# -------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None

# -------------------------------------------------
# Tabs
# -------------------------------------------------
tab_home, tab_chatbot, tab_login, tab_visuals, tab_dashboard, tab_about = st.tabs(
    ["🏠 Home", "👽 AI Chatbot", "🔐 Log In", "📈 Visuals", "📊 Dashboard", "ℹ️ About"]
)

# =================================================
# HOME TAB
# =================================================
with tab_home:
    st.markdown('<div class="section-title">🏠 Home</div>', unsafe_allow_html=True)

    st.markdown(
    """
<div style="
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    padding: 22px;
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.20);
    box-shadow: 0px 4px 20px rgba(0,0,0,0.45);
    color: #e0f2fe;
    font-size: 16px;
    line-height: 1.7;
">

<h3 style="color:#e0f2fe; margin-top:0;">📘 Welcome to the World Cup Analysis Application</h3>

This application provides an <b>interactive and visually rich analysis</b> of FIFA World Cup historical data.
Using dashboards, charts, and insights, we explore key analytical points:

<br>

<ul style="color:#e2e8f0;">
  <li>🌍 <b>Host Country Analysis</b> — Which nations have hosted the World Cup most often?</li>
  <li>🏟️ <b>Stadium Overview</b> — Which stadiums conducted the highest number of matches?</li>
  <li>📈 <b>Goal Trends</b> — How goal scoring changed across different World Cup years?</li>
  <li>🚨 <b>Defensive Statistics</b> — Which teams conceded the most goals?</li>
  <li>🥅 <b>High-Scoring Stadiums</b> — Where were the most goals recorded?</li>
  <li>🔁 <b>Round Match Density</b> — Which rounds had the most matches?</li>
</ul>

Navigate through the tabs above to explore <b>dashboards, visuals, raw data, and insights</b>.

</div>
""",
    unsafe_allow_html=True
)


    st.write("")
    st.markdown("##### 🌍 Matches by Host Country (Top 5)")

    host_counts = (
        match_df["Country"]
        .value_counts()
        .reset_index()
    )
    host_counts.columns = ["Country", "Matches"]
    host_counts = host_counts.head(5)
    fig = px.pie(
        host_counts,
        values="Matches",
        names="Country",
        hole=0.4,)
    fig.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',   # chart outer background
    plot_bgcolor='rgba(0,0,0,0)',     # inside graph background
    legend=dict(
        font=dict(color="white"),
        )
    )
    
    st.plotly_chart(fig, use_container_width=True, key="home_pie")

# =================================================
# CHATBOT TAB
# =================================================
with tab_chatbot:
    st.markdown('<div class="section-title">👽 AI Chatbot</div>', unsafe_allow_html=True)
    st.write("Ask me about the project, dataset, visuals, and analysis.")

    user_input = st.text_input("**You:** ", "")
    if user_input:
        response = get_reply(user_input)
        st.markdown(f"**Bot:** {response}")

# =================================================
# LOGIN TAB
# =================================================
with tab_login:
    st.markdown('<div class="section-title">🔐 Log In</div>', unsafe_allow_html=True)

    credentials = {
        "palak": "palak123",
        "wine": "wine123",
        "pass": "pass1",
    }

    if not st.session_state.logged_in:
        st.subheader("Login Required")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.button("Login")

        if login_button:
            if username in credentials and credentials[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"🤗 Welcome, {username}!")
            else:
                st.error("👽 Invalid username or password")
    else:
        st.success(f"✅ You are already logged in as {st.session_state.username}")

# =================================================
# VISUALS TAB  (LOCKED UNTIL LOGIN)
# =================================================
with tab_visuals:
    st.markdown('<div class="section-title">📈 Visuals</div>', unsafe_allow_html=True)

    if not st.session_state.logged_in:
        st.warning("🔒 Please log in to access Visuals.")
    else:
        st.caption("Select a question from the sidebar to see its interactive chart here.")


        # Q1 – hosting countries (bar)
        if question.startswith("Q1"):
            st.subheader("Q1: Which countries hosted the World Cup most often?")
            

            q1 = (
        match_df.groupby("Country")["Year"]
        .nunique()
        .reset_index(name="Times_Hosted")
        .sort_values("Times_Hosted", ascending=False)
    )

            fig = px.bar(
        q1,
        x="Times_Hosted",
        y="Country",
        orientation="h",
        text="Times_Hosted",
        color="Times_Hosted",
        title="Top Hosting Nations",
    )
            fig.update_traces(textposition="outside")
    # Apply your dark theme styling
            fig = apply_dark_theme(fig, show_legend=False)

            st.plotly_chart(fig, use_container_width=True)


        # Q2 – stadium with most games per country (TREEMAP)
        elif question.startswith("Q2"):
            st.subheader("Q2: Which stadium hosts the highest number of games in each country?")
            st.caption("**Stadium Match Frequency(Treemap)**")

            games_per_stadium = (
                match_df.groupby(["Country", "Stadium"])
                .size()
                .reset_index(name="Matches")
            )

            idx = games_per_stadium.groupby("Country")["Matches"].idxmax()
            q2 = (
                games_per_stadium.loc[idx]
                .sort_values("Matches", ascending=False)
                .reset_index(drop=True)
            )

            # Treemap chart
            fig = px.treemap(
                q2,
                path=["Country", "Stadium"],
                values="Matches",
                title="Stadium Match Frequency"
            )
            #  Enable labels inside treemap blocks
            fig.update_traces(
            textinfo="label+value",
            hovertemplate="<b>%{label}</b><br>Matches: %{value}<extra></extra>")
            fig = apply_dark_theme(fig, show_legend=True)

            st.plotly_chart(fig, use_container_width=True, key="visual_q2")

        # Q3 – total goals by year (line)
        elif question.startswith("Q3"):
            st.subheader("Q3: How have total goals changed across different World Cups/years?")
            st.caption("**Goals Over Time**")

            goals_per_year = (
                match_df.groupby("Year")["Total_Goals_in_Match"]
                .sum()
                .reset_index(name="Total_Goals")
                .sort_values("Year")
            )
            fig = px.line(
                goals_per_year,
                x="Year",
                y="Total_Goals",
                markers=True,
                text="Total_Goals",
                title="Goals Over Time",
            )
            fig.update_traces(marker_color="#430de5", line_color="#d83cfb")
            fig = apply_dark_theme(fig, show_legend=False)

            st.plotly_chart(fig, use_container_width=True, key="visual_q3")

        # Q4 – team conceding most goals (horizontal bar)
        elif question.startswith("Q4"):
            st.subheader("Q4: Which team conceded the most goals in World Cups?")
            conceded_per_team = (
                df.groupby("Team")["Opponent G"].sum().reset_index(name="Goals_Conceded").sort_values("Goals_Conceded", ascending=False)
                .head(10)
            )

            fig = px.bar(conceded_per_team,x="Goals_Conceded",y="Team",
                color="Goals_Conceded",text="Goals_Conceded",title="Most Goals Conceded",
            )
            fig.update_traces(textposition="outside")
            fig = apply_dark_theme(fig, show_legend=False)
            st.plotly_chart(fig, use_container_width=True, key="visual_q4")

        # Q5 – stadium with most goals scored (bar, top 15)
        elif question.startswith("Q5"):
            st.subheader("Q5: Which stadium has seen the most goals scored?")
            goals_per_stadium = (
                match_df.groupby("Stadium")["Total_Goals_in_Match"]
                .sum()
                .reset_index(name="Total_Goals")
                .sort_values("Total_Goals", ascending=False)
                .head(10)
            )

            fig = px.bar( goals_per_stadium,x="Total_Goals",y="Stadium",color="Total_Goals",text="Total_Goals",title="Goal-Rich Stadiums",)
            fig.update_traces(textposition="outside")
            fig = apply_dark_theme(fig, show_legend=False)
            st.plotly_chart(fig, use_container_width=True, key="visual_q5")

        # Q6 – rounds with most matches
        elif question.startswith("Q6"):
            st.subheader("Q6: Which rounds had the most matches?")
            st.caption(" **Round Match Density**")

            matches_per_round = (
                match_df.groupby("Round")
                .size()
                .reset_index(name="Matches")
                .sort_values("Matches", ascending=False)
            )

            fig = px.bar(
                matches_per_round,y="Round", x="Matches", text="Matches",title="Round Match Density",color="Matches"
            )
            fig.update_traces(textposition="outside")
            fig = apply_dark_theme(fig, show_legend=False)
            st.plotly_chart(fig, use_container_width=True, key="visual_q6")

# DASHBOARD TAB  (LOCKED UNTIL LOGIN)
with tab_dashboard:
    st.markdown('<div class="section-title">📊 Dashboard – Interactive</div>', unsafe_allow_html=True)

    if not st.session_state.logged_in:
        st.warning("🔒 Please log in to access the Dashboard.")
    else:
        st.markdown("### 🎛 Filters")
        country_filter = st.selectbox(
        "Select Host Country",
        options=["All"] + sorted(match_df["Country"].unique()),
        index=0,   # "All" pre-selected
        key="dash_country",
)
        
        filtered_matches = match_df.copy()
        if country_filter != "All":
          filtered_matches = filtered_matches[filtered_matches["Country"] == country_filter]

        df_filtered = df[df["Year"].isin(filtered_matches["Year"].unique())]

        # Row 1
        r1c1, r1c2 = st.columns(2)
        with r1c1:
            purple_shades = ["#c4b5fd", "#a78bfa", "#6d28d9"]
            q1_dash = (
                filtered_matches.groupby("Country")["Year"]
                .nunique()
                .reset_index(name="Times_Hosted")
                .sort_values("Times_Hosted", ascending=False)
            )
            if not q1_dash.empty:
                fig = px.bar(q1_dash, x="Country", y="Times_Hosted", text="Times_Hosted",title="Top Hosting Nations",)
                fig.update_traces(
                    marker_color=[get_shade_color(purple_shades) for _ in q1_dash["Country"]],
                    textposition="outside",
                )
                fig = apply_dark_theme(fig, show_legend=False)
                st.plotly_chart(fig, use_container_width=True, key="dash_q1")
        with r1c2:
            games = (
                filtered_matches.groupby(["Country", "Stadium"]).size().reset_index(name="Matches")
            )
            if not games.empty:
                idx = games.groupby("Country")["Matches"].idxmax()
                q2_dash = games.loc[idx].sort_values("Matches", ascending=False)
                fig = px.bar(q2_dash, x="Stadium", y="Matches", text="Matches", title="Stadium Match Frequency")
                fig.update_traces(
                    marker_color=[get_shade_color(purple_shades) for _ in q2_dash["Stadium"]],
                    textposition="outside",
                )
                fig = apply_dark_theme(fig, show_legend=False)
                st.plotly_chart(fig, use_container_width=True, key="dash_q2")

        st.markdown("---")

        # Row 2
        r2c1, r2c2 = st.columns(2)
        with r2c1:
            goals = (
                filtered_matches.groupby("Year")["Total_Goals_in_Match"]
                .sum()
                .reset_index(name="Total_Goals")
            )
            if not goals.empty:
                fig = px.line(goals, x="Year", y="Total_Goals", markers=True,title="Goals Over Time",text="Total_Goals",)
                fig.update_traces(marker_color="#b91c1c", line_color="#d83cfb")
                fig = apply_dark_theme(fig, show_legend=False)
                st.plotly_chart(fig, use_container_width=True, key="dash_q3")

        with r2c2:
            conceded = (
                df_filtered.groupby("Team")["Opponent G"] .sum().reset_index(name="Goals_Conceded")
                .sort_values("Goals_Conceded", ascending=False)
                .head(10)
            )
            if not conceded.empty:
                fig = px.bar(
                    conceded,
                    x="Goals_Conceded",
                    y="Team",
                    orientation="h",
                    text="Goals_Conceded",
                    title="Most Goals Conceded",
                )
                fig.update_traces(
                    marker_color=[get_shade_color(purple_shades) for _ in conceded["Team"]],
                    textposition="outside",
                )
                fig = apply_dark_theme(fig, show_legend=True) 
                st.plotly_chart(fig, use_container_width=True, key="dash_q4")

        st.markdown("---")
        # Row 3 
        stadium_goals = (
                filtered_matches.groupby("Stadium")["Total_Goals_in_Match"].sum().reset_index(name="Total_Goals")
                .sort_values("Total_Goals", ascending=False).head(5))
        if not stadium_goals.empty:
                fig = px.bar(stadium_goals, x="Stadium", y="Total_Goals", text="Total_Goals",title="Goal-Rich Stadiums",)
                fig.update_traces(
                    marker_color=[get_shade_color(purple_shades) for _ in stadium_goals["Stadium"]],
                    textposition="outside",
                )
                fig = apply_dark_theme(fig, show_legend=False) 
                st.plotly_chart(fig, use_container_width=True, key="dash_q5")

    # Sort rounds by match count (highest → lowest)
        rounds = (filtered_matches.groupby("Round").size().reset_index(name="Matches")
        .sort_values("Matches", ascending=False
                     )
    )

        if not rounds.empty:
            fig = px.bar( rounds,x="Round",y="Matches",text="Matches",title="Round Match Density",
        )
            fig.update_traces(
            marker_color=[get_shade_color(purple_shades) for _ in rounds["Round"]],textposition="outside",
            )
            fig = apply_dark_theme(fig, show_legend=False) 
            st.plotly_chart(fig, use_container_width=True, key="dash_q6")
        else:
            st.info("No round data found for the selected filters.")

with tab_about:
    st.markdown('<div class="section-title">ℹ️ About</div>', unsafe_allow_html=True)
    st.markdown(
        """
        This World Cup Analysis Application was developed to provide interactive insights into FIFA World Cup historical data.
        It features dashboards, visualizations, and an AI chatbot to help users explore hosting patterns, stadium activity, goal trends, team performance, and round statistics.

        **Key Features:**
        - Interactive dashboards with filters for dynamic data exploration.
        - Visualizations including bar charts, line graphs, and pie charts.
        - An AI-powered chatbot for answering questions about the project and dataset.
        - A data explorer for viewing raw data and dataset information.

        **Dataset:**
        The dataset used contains detailed match results from FIFA World Cups, including information on years, teams, goals scored, stadiums, rounds, and host countries.""")

st.markdown(
    """
    <div style='text-align: center; padding: 20px; margin-top: 80px;
                font-size: 14px; color: white;'>
        Developed by <b>Palak Sharma 💕</b> | Data Analytics Project 2025
    </div>
    """,
    unsafe_allow_html=True
)
