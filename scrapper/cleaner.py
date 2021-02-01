import pandas as pd

def main():
    date_range = pd.date_range('04-01-2020', '01-30-2021')

    # load reddit data and prepare the daily data
    df_reddit = pd.read_csv("db.csv") 
    df_reddit = df_reddit.drop(columns=["id"])
    df_reddit["date"] = pd.DatetimeIndex(data=df_reddit["date"])
    df_reddit = df_reddit.set_index("date")
    df_reddit_counts = df_reddit.groupby(df_reddit.index.date).count().drop(columns=["body_sentiment", "title_sentiment"])
    df_reddit_counts = df_reddit_counts.reindex(date_range, fill_value=0)
    df_reddit = df_reddit.resample("d").mean()
    df_reddit["counts"] = df_reddit_counts["score"]

    # load the yahoo data and prepare the daily data
    df_yahoo = pd.read_csv("GME.csv")
    df_yahoo["Date"] = pd.DatetimeIndex(data=df_yahoo["Date"])
    df_yahoo = df_yahoo.set_index("Date")
    df_yahoo = df_yahoo.reindex(date_range, method="pad")

    # concatenate dataframes and output to file
    df = pd.concat([df_yahoo, df_reddit], axis=1)
    df.to_csv("daily_data.csv")


if __name__ == "__main__":
    main()
