from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

# ------------------------
# Simple corpus: intent phrase -> reply
# ------------------------
corpus = {
    "hello": "Hello! How can I assist you today?",
    "hi": "Hi there! What would you like to explore?",
    "hey": "Hey! How can I help you?",
    
    "what is this project": "This application analyzes FIFA World Cup data with dashboards and visual insights.",
    "about project": "This application explores hosting nations, stadiums, goals, teams, and rounds.",
    "what does this application do": "It visualizes World Cup statistics like hosting patterns, stadium activity, goals, and team performance.",
    
    "dataset used": "The dataset contains FIFA World Cup match details such as year, teams, goals, stadiums, rounds, and host countries.",
    "where data comes from": "The data is taken from historical FIFA World Cup match results.",
    
    "hosting nation": "The 'Top Hosting Nations' chart shows which countries hosted the World Cup most frequently.",
    "which country hosted most world cups": "You can see the hosting frequency in the 'Top Hosting Nations' visualization.",
    
    "most matches stadium": "Stadiums with the highest number of matches are shown in the stadium analysis.",
    "stadium analysis": "Stadiums are ranked based on their match counts.",
    
    "goals over time": "The 'Goals Over Time' chart shows goal trends across different World Cup editions.",
    "goal trend": "Goal-scoring trends per year can be seen in the visualizations.",
    
    "team conceded most goals": "The 'Highest Goals Conceded' section shows teams with the most conceded goals.",
    "worst defense team": "Teams with the highest conceded goals are shown in the conceded goals chart.",
    
    "goal rich stadiums": "The 'Goal-Rich Stadiums' chart shows stadiums with the highest goals.",
    "stadiums with most goals": "Top stadiums by total goals are shown in goal insights.",
    
    "round analysis": "The 'Round Match Density' chart shows which rounds have the most matches.",
    "which round has most matches": "You can see round-wise match count in the round density visualization.",
    
    "dashboard help": "Use filters like Year and Country to update KPIs and charts dynamically.",
    "how to use dashboard": "The dashboard lets you filter data and view updated statistics instantly.",
    
    "bye": "Goodbye! Have a great day!",
    "thank you": "You're welcome! Happy exploring!"
}

# ------------------------
# Preprocess text
# ------------------------
def preprocess_text(text: str):
    tokens = word_tokenize(text.lower())
    return [lemmatizer.lemmatize(t) for t in tokens if t.isalpha()]

# ------------------------
# Get reply using fuzzy keyword matching on keys of corpus
# ------------------------
def get_reply(user_input: str) -> str:
    user_tokens = set(preprocess_text(user_input))

    best_key = None
    best_score = 0

    for key in corpus.keys():
        key_tokens = set(preprocess_text(key))
        score = len(user_tokens & key_tokens)  # common words

        if score > best_score:
            best_score = score
            best_key = key

    if best_score == 0 or best_key is None:
        return "Sorry, I didn't understand that. You can ask about the project, dataset, goals, stadiums, rounds or dashboard."

    return corpus[best_key]
