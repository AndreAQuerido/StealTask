from sqlmodel import Session, create_engine
from StealApp.models import *
import random

engine = create_engine(url="sqlite:///./steal.db", connect_args={"check_same_thread": False})

#dependency
def get_session():
    with Session(engine) as session:
        yield session


def populate_table():
    options={"AAPL":"Apple","TSLA":"Tesla","AMZN":"Amazon"}
    buy_sell=["BUY","SELL"]
    with Session(engine) as session:
        for i in range(0,3):
            trade_details1 = TradeDetails(buySellIndicator=random.choice(buy_sell),price=round(random.uniform(10.5,300.70),2),quantity=2)
            session.add(trade_details1)
            session.commit()
            session.refresh(trade_details1)
        for index, (key, value) in enumerate(options.items()):
                trade=Trade(asset_class="Stock",instrument_id = key ,instrument_name = value, trade_detail_id = index + 1, trade_id = f"{index + 1}",trader="Andre")
                session.add(trade)
                session.commit()
                
