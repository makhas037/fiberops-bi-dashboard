from datetime import datetime


def format_currency(value: float, currency_symbol: str = "$") -> str:
    try:
        return f"{currency_symbol}{value:,.2f}"
    except Exception:
        return f"{currency_symbol}{value}"


def format_date(dt: datetime) -> str:
    try:
        return dt.strftime("%Y-%m-%d %H:%M")
    except Exception:
        return str(dt)
