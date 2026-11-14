def add_price_features(df):
    g = df.groupby("unique_id")["sell_price"]
    df["price_ratio"] = df["sell_price"] / g.transform("mean")      # < 1 = discount
    df["price_change_7d"] = df["sell_price"] / g.shift(7) - 1
    return df