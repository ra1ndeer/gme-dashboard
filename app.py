import dash
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import dash_core_components as dcc 
import dash_html_components as html

from dash.dependencies import Input, Output, State



def get_gme_plot(df):
    """
        Plots the GME pricing info starting at April 1st 2020
    """
    fig_yahoo = go.Figure()
    fig_yahoo.add_trace(go.Scatter(
        x=df.index,
        y=df["High"],
        mode="lines",
        name="High",
        marker_color=colors["positive"]
        ))
    fig_yahoo.add_trace(go.Scatter(
        x=df.index,
        y=df["Low"],
        mode="lines",
        name="Low",
        marker_color=colors["negative"]
        ))
    fig_yahoo.add_trace(go.Scatter(
        x=df.index,
        y=df["Close"],
        mode="lines",
        name="Close",
        marker_color=colors["header"]
        ))
    

    fig_yahoo.update_yaxes(gridwidth=1, 
                           zeroline=False, 
                           type="log")
    fig_yahoo.update_layout(layout)
    fig_yahoo_title = {"text": "GME daily stock pricing (USD), in logarithmic scale", 
                       "xanchor": "center", 
                       "yanchor": "top", 
                       "x": 0.5, 
                       "y": 0.99}
    fig_yahoo.update_layout(height=729, 
                            width=1155, 
                            legend={"x": 0, 
                                    "y":1}, 
                            title=fig_yahoo_title)
    
    return fig_yahoo



def get_body_sentiment_plot(df):
    
    pos_masked_df = df[df["body_sentiment"] > 0.05]
    neg_masked_df = df[df["body_sentiment"] < -0.05]
    neu_masked_df = df[(df["body_sentiment"] < 0.05) & (df["body_sentiment"] > -0.05)]
    fig_body = go.Figure(data=[
        go.Bar(name="Positive", 
               x=pos_masked_df.index, 
               y=pos_masked_df["body_sentiment"], 
               marker_color=colors["positive"]),
        go.Bar(name="Negative", 
               x=neg_masked_df.index, 
               y=neg_masked_df["body_sentiment"], 
               marker_color=colors["negative"]),
        go.Bar(name="Neutral", 
               x=neu_masked_df.index, 
               y=neu_masked_df["body_sentiment"]+0.01, 
               marker_color=colors["neutral"])
    ])
    fig_body.update_layout(layout)
    fig_body.update_traces(marker_line_width=0)
    fig_body_title = {"text": "r/wallstreetbets mean daily post body sentiment", 
                      "xanchor": "center", 
                      "yanchor": "top", 
                      "x": 0.5, 
                      "y": 0.97}
    fig_body.update_layout(height=233, 
                           legend={"x": 0, 
                                   "y": 1}, 
                           title=fig_body_title)
                           
    return fig_body
    
    

def get_title_sentiment_plot(df):
    """
        Plots the mean daily post title sentiment on r/wallstreetbets
    """
    pos_masked_df = df[df["title_sentiment"] > 0.05]
    neg_masked_df = df[df["title_sentiment"] < -0.05]
    neu_masked_df = df[(df["title_sentiment"] < 0.05) & (df["title_sentiment"] > -0.05)]
    fig_title = go.Figure(data=[
        go.Bar(name="Positive", 
               x=pos_masked_df.index, 
               y=pos_masked_df["title_sentiment"], 
               marker_color=colors["positive"]),
        go.Bar(name="Negative", 
               x=neg_masked_df.index, 
               y=neg_masked_df["title_sentiment"], 
               marker_color=colors["negative"]),
        go.Bar(name="Neutral", 
               x=neu_masked_df.index, 
               y=neu_masked_df["title_sentiment"]+0.01, # offset added for visibility
               marker_color=colors["neutral"])
    ])
    fig_title.update_layout(layout)
    fig_title.update_traces(marker_line_width=0)
    fig_title_title = {"text": "r/wallstreetbets mean daily post title sentiment", 
                       "xanchor": "center", 
                       "yanchor": "top", 
                       "x": 0.5, 
                       "y": 0.97}
    fig_title.update_layout(height=233, 
                            legend={"x": 0, 
                                    "y":1}, 
                            title=fig_title_title)
                            
    return fig_title



def get_posts_plot(df):
    """
        Plots the daily post count on r/wallstreetbets
    """
    fig_posts = go.Figure(data=[
        go.Bar(name="Number of Posts", 
               x=df.index, 
               y=df["counts"], 
               marker_color=colors["header"])
        ])

    
    fig_posts.update_xaxes(showgrid=False, 
                           zeroline=False)
    fig_posts.update_yaxes(gridwidth=1, 
                           zeroline=False, 
                           type="log")
    fig_posts.update_layout(layout)
    fig_posts.update_traces(marker_line_width=0)
    fig_posts_title = {"text": "r/wallstreetbets daily posts count, in logarithmic scale", 
                       "xanchor": "center", 
                       "yanchor": "top", 
                       "x": 0.5, 
                       "y": 0.97}
    fig_posts.update_layout(height=233, 
                            title=fig_posts_title)
    return fig_posts



# stylesheet
external_stylesheets = ['https://github.com/plotly/dash-app-stylesheets/blob/master/dash-technical-charting.css']

# colors
colors = {
    "background": "#f7f7f7",
    "plot_background": "#ffffff",
    "header_text": "#f2f2f2",
    "text": "#000000",
    "header": "#333436",
    "positive": "#1d853e",
    "negative": "#cc0e0e",
    "neutral": "#878787",
    "close": "#d4af1c",
    "url": "#8eb1ed"
    }

# this variable exists because Dash is an idiotic library
relay_status = [None, None, None, None]

# some common layout settings
layout = go.Layout(
    margin=go.layout.Margin(
        l=15, 
        r=15, 
        b=15, 
        t=30, 
        pad=5,
    ),
    plot_bgcolor=colors["background"],
    paper_bgcolor=colors["plot_background"],
    font={"color":colors["text"]},
    autosize=True
    )




df = pd.read_csv("daily_data.csv", 
                    index_col=0)
df["index"] = df.index
# dropping the last day collected (Jan 30) because it was 2AM of Jan 30 
# when I ran the web scrapper so it isn't a full day of data
df = df.drop(df.index[-1]) 

app = dash.Dash(__name__, 
                external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div(children=[
    html.Div([
        html.H1("r/wallstreetbets vs. Wall Street", 
                className="row", 
                style={"font-family": "Helvetica", 
                        'backgroundColor': colors["header"], 
                        'color': colors['header_text'], 
                        "margin": 0, 
                        "padding-left": 10, 
                        "padding-top": 10, 
                        "padding-right": 10, 
                        "padding-bottom": 5}),
        html.P(children=["A sentiment analysis of r/wallstreetbets posts pertaining GME (GameStop) using VADER: ", 
                    dcc.Link("paper link", 
                             href="https://www.researchgate.net/publication/275828927_VADER_A_Parsimonious_Rule-based_Model_for_Sentiment_Analysis_of_Social_Media_Text", 
                             target="_blank", 
                             style={"font-family": "Helvetica", 
                                    "color": colors["url"]})],
                style={"font-family": "Helvetica", 
                        'backgroundColor': colors["header"], 
                        'color': colors['header_text'], 
                        "margin": 0, 
                        "padding-left": 10, 
                        "padding-top": 5, 
                        "padding-right": 10, 
                        "padding-bottom": 10})
        ]),
        html.Div([
            html.Div([
                    dcc.Graph(id="gme_stock", 
                                config={'doubleClick': 'autosize'})
                ], className="eight columns", 
                    style={"margin-left": 10, 
                            "margin-right": 0, 
                            "margin-top": 20, 
                            "margin-bottom": 20}), 
            html.Div([
                html.Div([
                    dcc.Graph(id="sentiment_title", 
                                config={'doubleClick': 'autosize'})
                    ], className="row", 
                        style={"margin-left": 10, 
                                "margin-right": 20, 
                                "margin-top": 20, 
                                "margin_bottom": 10, 
                                "display": "flex", 
                                "flex-direction": "row"}),
                html.Div([
                    dcc.Graph(id="sentiment_body", 
                                config={'doubleClick': 'autosize'})
                    ], className="row", 
                        style={"margin-left": 10, 
                                "margin-right": 20, 
                                "margin-top": 10, 
                                "margin_bottom": 10, 
                                "display": "flex", 
                                "flex-direction": "row"}),
                html.Div([
                    dcc.Graph(id="count", 
                                config={'doubleClick': 'autosize'})
                ], className="row", 
                    style={"margin-left": 10, 
                            "margin-right": 20, 
                            "margin-top": 10, 
                            "margin_bottom": 20, 
                            "display": "flex", 
                            "flex-direction": "row"}),
                ], className="four columns")
        ], style={"display": "flex", 
                    "flex-direction": "row"}),
        html.Div([
            html.P(children=["Author: Luís Franco | Contact: luisbap1999@gmail.com | Github repository: ", 
                                dcc.Link("link", 
                                        href="https://github.com/", 
                                        target="_blank", 
                                        style={"font-family": "Helvetica", 
                                                "color": colors["url"]}),
                                " | LinkedIn: ",
                                dcc.Link("link", 
                                        href="https://www.linkedin.com/in/ra1ndeer/", 
                                        target="_blank", 
                                        style={"font-family": "Helvetica", 
                                                "color": colors["url"]})], 
                                        style={"font-family": "Helvetica", 
                                                'backgroundColor': colors["header"], 
                                                'color': colors['header_text'], 
                                                "margin": 0, 
                                                "padding": 10})
            ])
    ], style={'backgroundColor': colors['background']})
                

# the one and only callback which was horribly hard to 
# do because of severe lack of documentation
@app.callback([Output("gme_stock", "figure"), 
                Output('sentiment_title', 'figure'), 
                Output('sentiment_body', 'figure'), 
                Output('count', 'figure')],
                [Input("gme_stock", "relayoutData"),
                Input("sentiment_title", "relayoutData"),
                Input("sentiment_body", "relayoutData"),
                Input("count", "relayoutData")])
def zoom_event(relayout_data0, relayout_data1, relayout_data2, relayout_data3):
    my_figures = [get_gme_plot(df), get_title_sentiment_plot(df), get_body_sentiment_plot(df), get_posts_plot(df)]

    # hacky solution for the fact that Dash doesn't allow the
    # same Output object to be used for more than one callback
    global relay_status
    current_master = 0

    if relayout_data0 != relay_status[0]:
        relay_status[0] = relayout_data0
        current_master =  0
    if relayout_data1 != relay_status[1]:
        relay_status[1] = relayout_data1
        current_master = 1
    if relayout_data2 != relay_status[2]:
        relay_status[2] = relayout_data2
        current_master = 2
    if relayout_data3 != relay_status[3]:
        relay_status[3] = relayout_data3
        current_master = 3
    
    # if one zooms, they all zoom
    for fig in my_figures:
        try:
            fig.update_xaxes(range=[relay_status[current_master]["xaxis.range[0]"], relay_status[current_master]["xaxis.range[1]"]])
        except (KeyError, TypeError):
            fig['layout']["xaxis"]["autorange"] = True


    return my_figures


if __name__ == "__main__":
    app.run_server(debug=False)
