import dash
from dash import dcc, html, Input, Output, dash_table
import requests
import pandas as pd
import plotly.express as px

# Fetch data from Flask API
response = requests.get("http://127.0.0.1:5000/data")

print("Status Code:", response.status_code)
print("Headers:", response.headers)
print("Raw Text:", repr(response.text))  # Shows if it's empty or has an HTML error

try:
    data = response.json()
except requests.exceptions.JSONDecodeError as e:
    print("JSON decoding failed. Response content was:", repr(response.text))
    data = None

# Convert to DataFrame
df = pd.DataFrame(data)

# Extract sentiment scores
df["Positive"] = df["sentiment_score"].apply(lambda x: x["pos"])
df["Neutral"] = df["sentiment_score"].apply(lambda x: x["neu"])
df["Negative"] = df["sentiment_score"].apply(lambda x: x["neg"])
df["Compound"] = df["sentiment_score"].apply(lambda x: x["compound"])

# Initialize Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Super Bowl Ad Sentiment Analysis", style={"textAlign": "center"}),

    # Dropdown for brand selection
    dcc.Dropdown(
        id="brand-dropdown",
        options=[{"label": brand, "value": brand} for brand in df["brand_name"].unique()],
        value="Jeep",
        clearable=False
    ),

    # Sentiment Bar Chart
    dcc.Graph(id="sentiment-bar"),

    # Table of comments
    dash_table.DataTable(
        id="comment-table",
        columns=[{"name": i, "id": i} for i in ["brand_name", "comment", "Positive", "Neutral", "Negative", "Compound"]],
        style_table={'overflowX': 'auto'}
    ),

    # Text-to-Speech button
    html.Button("Read Positive Comment", id="tts-button", n_clicks=0),
    html.Audio(id="audio", controls=True, autoPlay=False)
])

# Callback for updating the sentiment bar chart
@app.callback(
    Output("sentiment-bar", "figure"),
    Input("brand-dropdown", "value")
)
def update_bar_chart(selected_brand):
    filtered_df = df[df["brand_name"] == selected_brand]
    fig = px.bar(filtered_df, x=["Positive", "Neutral", "Negative"], y=filtered_df["brand_name"],
                 title=f"Sentiment Distribution for {selected_brand}", barmode="group")
    return fig

# Callback for updating the comment table
@app.callback(
    Output("comment-table", "data"),
    Input("brand-dropdown", "value")
)
def update_table(selected_brand):
    return df[df["brand_name"] == selected_brand].to_dict("records")

# Callback for text-to-speech
@app.callback(
    Output("audio", "src"),
    Input("tts-button", "n_clicks"),
    Input("brand-dropdown", "value")
)
def generate_audio(n_clicks, selected_brand):
    if n_clicks > 0:
        import pyttsx3
        engine = pyttsx3.init()
        pos_comment = df[(df["brand_name"] == selected_brand) & (df["Positive"] > 0.1)]["comment"].values
        if len(pos_comment) > 0:
            text = pos_comment[0]  # Get the first positive comment
            engine.save_to_file(text, "positive_comment.mp3")
            engine.runAndWait()
            return "positive_comment.mp3"
    return ""

if __name__ == '__main__':
    app.run_server(debug=True)
