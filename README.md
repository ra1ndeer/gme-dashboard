# gme-dashboard

Live dashboard link: [here](http://gme-app.herokuapp.com/)

## What is this?

The subreddit r/wallstreetbets has been at "war" with Wall Street hedge funds, particularly through GameStop's stock (GME). So I decided I'd have some fun with data.

## Data

Data was scrapped using [Pushshift](https://pushshift.io/). Scrapping criterion was pretty basic: get all posts on r/wallstreetbets with the word GME, in the title or body, from April 1st 2020 to Jan 29th 2021. Sentiment analysis was performed with [VADER](https://www.researchgate.net/publication/275828927_VADER_A_Parsimonious_Rule-based_Model_for_Sentiment_Analysis_of_Social_Media_Text) for post body and title separately. Data was then average on a daily basis.

Financial data was obtained through [Yahoo Finance](https://finance.yahoo.com/), with missing data (weekends, when the market is closed) filled with the previous value.

## Dashboard

Dashboard was build using [Dash](https://plotly.com/dash/).

## Author
* Luís Franco | luisbap1999@gmail.com | [LinkedIn](https://www.linkedin.com/in/ra1ndeer/)
