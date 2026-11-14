def add_lag_features(df, horizon=28, lags=(0, 7, 14), windows=(7, 28)):
    g = df.groupby("unique_id")["y"]
    for l in lags:
        df[f"lag_{horizon + l}"] = g.shift(horizon + l)
    shifted = g.shift(horizon)
    for w in windows:
        df[f"roll_mean_{w}"] = shifted.groupby(df["unique_id"]).transform(
            lambda s: s.rolling(w, min_periods=1).mean()
        )
        df[f"roll_std_{w}"] = shifted.groupby(df["unique_id"]).transform(
            lambda s: s.rolling(w, min_periods=2).std()
        )
    return df