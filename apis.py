from datetime import datetime
import enum
from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import Response
from requests import request
from StealApp.models import Trade, TradeDetails
from typing import List, Union, final
from StealApp.db import get_session
from sqlmodel import Session, select

trades_router = APIRouter(prefix= "/trades")

def filter(query_dict,responses,session):
    filters= {k: v for k, v in query_dict.items() if v is not None}
    flag_trade_details=False
    trade_detail=""
    if filters: 
        for response in responses.copy():
            flag_trade_details=False
            for filter in filters.keys():
                if filter == "max" or filter=="min" or filter == "tradeType":
                    if not flag_trade_details:
                        result=session.exec(select(TradeDetails).where(TradeDetails.id==response.trade_detail_id))
                        trade_detail= result.first()
                        flag_trade_details=True
                    
                    if filter == "tradeType":
                        if not trade_detail.buySellIndicator == filters[filter]:
                            responses.remove(response)
                            break
                        continue
                    if filter == "max":
                        if trade_detail.price > filters[filter]:
                            responses.remove(response)
                            break
                        continue
                    else:
                        if trade_detail.price < filters[filter]:
                            responses.remove(response)
                            break
                        continue
                if filter == "end":
                    if not response.trade_date_time <= filters[filter]:

                        responses.remove(response)
                        break
                    continue
                if filter == "start":
                    if not response.trade_dat_time >= filters[filter]:

                        responses.remove(response)
                        break
                    continue
                if filter == "search":
                    if not response.counterparty.contains(filters[filter]) or response.instrument_name.contains(filters[filter]) or \
                        response.trader.contains(filters[filter]) or response.instrument_id.contains(filters[filter]):

                        responses.remove(response)
                        break
                    continue
                    
                if not getattr(response,filter) == filters[filter]:
                    responses.remove(response)

    return responses

def sorted(responses_to_sort, type_sort):
    if type_sort == "+i_id":
        responses_to_sort.sort(key=lambda x: x.instrument_id)
    elif type_sort == "-i_id":
        responses_to_sort.sort(key=lambda x: x.instrument_id,reverse=True)
    elif type_sort == "+asset":
        responses_to_sort.sort(key=lambda x: x.asset_class)
    elif type_sort == "-asset":
        responses_to_sort.sort(key=lambda x: x.asset_class,reverse=True)     
    elif type_sort == "+trader":
        responses_to_sort.sort(key=lambda x: x.trader)
    elif type_sort == "-trader":
        responses_to_sort.sort(key=lambda x: x.trader,reverse=True) 
          
    return responses_to_sort

@trades_router.get("/", response_model=List[Trade])
async def get_trades(offset:int |None = None, limit:int | None= None, search:str | None  = None, assetClass: str | None = None ,
                    start: datetime | None = None , end : datetime | None = None , maxPrice: int |None = None,
                    minPrice: int |None= None, tradeType: str | None = None, sort_by:str |None = None,
                    session: Session = Depends(get_session)):

    query_dict = {
        "search" : search,
        "asset_class" : assetClass,
        "end" : end,
        "start" : start,
        "tradeType" : tradeType,
        "max": maxPrice,
        "min":minPrice
    }
    result = session.exec(select(Trade))
    responses = result.all()
    responses = filter(query_dict= query_dict,responses=responses,session=session)
    
    if responses:
        if limit and offset:
            responses = responses[offset:limit]
        elif limit:
            responses = responses[:limit]
        elif offset:
            responses = responses[offset:limit]
        if sort_by:
         sorted(responses,sort_by)
        
        return responses
    


    return Response(f"No trades found", status_code= status.HTTP_400_BAD_REQUEST)

@trades_router.get("/{trade_id}")
async def get_trade_by_id(trade_id: str, session: Session =Depends(get_session)):
    request = session.exec(select(Trade)).where(Trade.trade_id == trade_id)
    result = request.first()

    if result:
        return result
    
    return Response(f"No trade exists with the id {trade_id}", status_code= status.HTTP_400_BAD_REQUEST)