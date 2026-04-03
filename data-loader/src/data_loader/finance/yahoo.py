from typing import Literal, Annotated

import pandas as pd
from pydantic import BaseModel, Field
import yfinance as yf

from ..utils import configure_logging


TickerSymbol = Annotated[str, Field(min_length=1, max_length=4)]
log = configure_logging(streaming=True)


class YahooFinanceLoader(BaseModel):
    """
    Object class to retrieve prices from yahoo finance repo
    """
    tickers: list[TickerSymbol] | None = None
    price_type: Literal['Open', 'Close', 'High', 'Low'] | None = None
    time_period: Literal['5y', '1y', 'ytd', '10y', 'max'] | None = None
    time_interval: Literal[
        '1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo'
    ] | None = None

    def get_stock_price_history(
        self,
        ticker_symbol: str,
        **kwargs
    ) -> pd.DataFrame:
        time_period = kwargs.get("time_period", self.time_period or "1y")
        time_interval = kwargs.get("time_interval", self.time_interval or "1d")
        stock = yf.Ticker(ticker_symbol)
        ts = stock.history(
            period=time_period,
            interval=time_interval
        )
        log.info(
            f"Retrieved market data for {ticker_symbol} with time_period {time_period}"
            f" and time_interval {time_interval}")
        return ts
