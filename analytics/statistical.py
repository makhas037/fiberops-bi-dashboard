def describe(df):
    try:
        return df.describe().to_dict()
    except Exception:
        return {"rows": len(df) if hasattr(df, '__len__') else 0}
