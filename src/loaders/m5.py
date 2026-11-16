from pathlib import Path
import numpy as np
import pandas as pd

DATA_DIR = Path(__file__).resolve().parents[2] / "data"


def load_m5_frames(directory, states=None, stores=None, max_series=None):
    """Load M5 frames, filtering wide sales rows before converting them to long format."""
    if max_series is not None and max_series < 1:
        raise ValueError("max_series must be a positive integer.")

    if not states and not stores and max_series is None:
        from datasetsforecast.m5 import M5
        return M5.load(str(directory))

    path = Path(directory) / "m5" / "datasets"
    key_cols = ["item_id", "dept_id", "cat_id", "store_id", "state_id"]
    sales_dtypes = {
        "item_id": "category",
        "dept_id": "category",
        "cat_id": "category",
        "store_id": "category",
        "state_id": "category",
        **{f"d_{i}": np.float32 for i in range(1, 1970)},
    }

    selected_chunks = []
    selected_count = 0
    for chunk in pd.read_csv(
        path / "sales_train_evaluation.csv",
        dtype=sales_dtypes,
        chunksize=1000,
    ):
        if states:
            chunk = chunk[chunk["state_id"].isin(states)]
        if stores:
            chunk = chunk[chunk["store_id"].isin(stores)]
        if max_series is not None:
            chunk = chunk.head(max_series - selected_count)
        if not chunk.empty:
            selected_chunks.append(chunk)
            selected_count += len(chunk)
        if max_series is not None and selected_count >= max_series:
            break

    if not selected_chunks:
        raise ValueError("No M5 series matched the requested filters.")

    sales_train = pd.concat(selected_chunks, ignore_index=True)
    selected_keys = sales_train[key_cols].drop_duplicates()
    test_days = [f"d_{i}" for i in range(1942, 1970)]
    sales_test = pd.read_csv(
        path / "sales_test_evaluation.csv",
        usecols=key_cols + test_days,
        dtype={**{col: sales_dtypes[col] for col in key_cols},
               **{col: np.float32 for col in test_days}},
    )
    sales_test = sales_test.merge(selected_keys, on=key_cols, how="inner")
    sales = sales_train.merge(sales_test, on=key_cols, how="left")

    cal_dtypes = {
        "wm_yr_wk": np.uint16,
        "event_name_1": "category",
        "event_type_1": "category",
        "event_name_2": "category",
        "event_type_2": "category",
        "snap_CA": np.uint8,
        "snap_TX": np.uint8,
        "snap_WI": np.uint8,
    }
    calendar = pd.read_csv(
        path / "calendar.csv",
        dtype=cal_dtypes,
        usecols=list(cal_dtypes) + ["date"],
        parse_dates=["date"],
    )
    calendar["d"] = "d_" + (np.arange(len(calendar)) + 1).astype(str)
    calendar["d"] = calendar["d"].astype("category")
    for col in ("event_name_1", "event_type_1", "event_name_2", "event_type_2"):
        calendar[col] = calendar[col].cat.add_categories("nan").fillna("nan")

    sales["id"] = sales["item_id"].astype(str) + "_" + sales["store_id"].astype(str)
    sales["id"] = sales["id"].astype("category")
    long = sales.melt(
        id_vars=["id"] + key_cols,
        var_name="d",
        value_name="y",
    )
    long["d"] = long["d"].astype(calendar["d"].dtype)
    long = long.merge(calendar, on="d")
    long = long.sort_values(["id", "date"])
    nonzero = long["y"].gt(0).groupby(long["id"], observed=True).cummax()
    long = long[nonzero]

    price_dtypes = {
        "store_id": "category",
        "item_id": "category",
        "wm_yr_wk": np.uint16,
        "sell_price": np.float32,
    }
    selected_items = set(sales["item_id"].astype(str))
    selected_stores = set(sales["store_id"].astype(str))
    price_chunks = []
    for chunk in pd.read_csv(
        path / "sell_prices.csv",
        dtype=price_dtypes,
        chunksize=250000,
    ):
        chunk = chunk[
            chunk["item_id"].isin(selected_items)
            & chunk["store_id"].isin(selected_stores)
        ]
        if not chunk.empty:
            price_chunks.append(chunk)
    prices = pd.concat(price_chunks, ignore_index=True)
    long = long.merge(prices, on=["store_id", "item_id", "wm_yr_wk"])
    long = long.drop(columns=["d", "wm_yr_wk"])
    long = long.rename(columns={"id": "unique_id", "date": "ds"})

    y_df = long[["unique_id", "ds", "y"]]
    static_cols = ["item_id", "dept_id", "cat_id", "store_id", "state_id"]
    s_df = long[["unique_id"] + static_cols].groupby("unique_id", observed=True).head(1)
    x_df = long[long.columns.drop(["y"] + static_cols)]
    return y_df, x_df, s_df


def load_m5(states=None, stores=None, max_series=None, use_cache=True) -> pd.DataFrame:
    """Return M5 in the common format: unique_id, ds, y + exogenous + static columns."""
    has_filter = bool(states) or bool(stores) or max_series is not None
    cache_files = [
        DATA_DIR / "m5_sales.parquet",
        DATA_DIR / "m5_exog.parquet",
        DATA_DIR / "m5_static.parquet",
    ]
    if use_cache and not has_filter and all(path.exists() for path in cache_files):
        Y = pd.read_parquet(DATA_DIR / "m5_sales.parquet")
        X = pd.read_parquet(DATA_DIR / "m5_exog.parquet")
        S = pd.read_parquet(DATA_DIR / "m5_static.parquet")
    else:
        Y, X, S = load_m5_frames(DATA_DIR, states, stores, max_series)

    # --- merge into one dataframe ---
    df = Y.merge(X, on=["unique_id", "ds"], how="left")
    df = df.merge(S, on="unique_id", how="left")
    df["ds"] = pd.to_datetime(df["ds"])

    # --- promo proxy: price below 95% of the item's average price ---
    if "sell_price" in df.columns:
        avg_price = df.groupby("unique_id", observed=True)["sell_price"].transform("mean")
        df["promo"] = (df["sell_price"] / avg_price < 0.95).astype(int)

    return df.sort_values(["unique_id", "ds"]).reset_index(drop=True)


if __name__ == "__main__":
    df = load_m5(states=["CA"], max_series=500)
    print(df.shape)
    print(df.columns.tolist())
    print(df.head())