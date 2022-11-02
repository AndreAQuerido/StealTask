from datetime import datetime
from sqlalchemy import Column, DateTime, table
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy.sql import func
from typing import Optional


class TradeDetails(SQLModel,table=True):
    __tablename__ = "trade_details"
    id: Optional[int] = Field(primary_key=True)
    buySellIndicator : str
    price : float
    quantity: int

class Trade(SQLModel, table = True):
    trade_id : str = Field(primary_key = True)
    asset_class : Optional[str] = Field(default=None, description ="The asset class of the instrument traded. E.g. Bond, Equity, FX...etc")
    counterparty : Optional[str] = Field(default=None, description ="The counterparty the trade was executed with. May not always be available")
    instrument_id : str = Field(description ="The ISIN/ID of the instrument traded. E.g. TSLA, AAPL, AMZN...etc")
    instrument_name : str = Field(description ="The name of the instrument traded.")
    trade_date_time : Optional[datetime] = Field(sa_column = Column(DateTime(timezone = True),server_default= func.now()))
    trade_detail_id: Optional[int] = Field(foreign_key="trade_details.id")
    trader: str = Field(description = "The name of the Trader")