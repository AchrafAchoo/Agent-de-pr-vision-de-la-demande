import numpy as np
import pandas as pd


def add_calendar_features(df: pd.DataFrame) -> pd.DataFrame:
    df["dow"] = df["ds"].dt.dayofweek
    df["day"] = df["ds"].dt.day
    df["week"] = df["ds"].dt.isocalendar().week.astype(int)
    df["month"] = df["ds"].dt.month
    df["year"] = df["ds"].dt.year
    df["is_weekend"] = (df["dow"] >= 5).astype(int)

    if "event_name_1" in df.columns:
        df["has_event"] = df["event_name_1"].notna().astype(int)

    # SNAP flag of the row's own state
    snap_cols = {"CA": "snap_CA", "TX": "snap_TX", "WI": "snap_WI"}
    if "state_id" in df.columns and all(c in df.columns for c in snap_cols.values()):
        df["snap"] = np.select(
            [df["state_id"] == s for s in snap_cols],
            [df[c] for c in snap_cols.values()],
            default=0,
        )
    return df