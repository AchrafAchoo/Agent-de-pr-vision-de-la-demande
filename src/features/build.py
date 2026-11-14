from .calendar import add_calendar_features
from .price import add_price_features
from .lags import add_lag_features

CAT_COLS = ["item_id", "dept_id", "cat_id", "store_id", "state_id"]


def build_features(df, horizon=28):
    df = add_calendar_features(df)
    df = add_price_features(df)
    df = add_lag_features(df, horizon=horizon)
    for c in CAT_COLS:
        if c in df.columns:
            df[c] = df[c].astype("category")   # LightGBM handles these natively
    return df