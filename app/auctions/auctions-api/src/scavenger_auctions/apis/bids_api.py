# coding: utf-8

import importlib
import pkgutil
import uuid
from http.client import HTTPException
from typing import Dict, List  # noqa: F401

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    Path,
    Query,
    Response,
    Security,
    status,
)
from sqlmodel import Session

import openapi_server.impl
from scavenger_auctions.apis.bids_api_base import BaseBidsApi
from scavenger_auctions.models.bid import Bid
from scavenger_auctions.models.error_response import ErrorResponse
from scavenger_auctions.models.extra_models import TokenModel  # noqa: F401
from scavenger_auctions.sql_models.core import Bid as BidSQLModel
from scavenger_auctions.sql_models.core import engine

router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/bid/{id}",
    responses={
        102: {"description": "BID PROCESSING"},
        200: {"model": Bid, "description": "OK"},
        "4XX": {"model": ErrorResponse, "description": "CLIENT ERROR"},
        "5XX": {"model": ErrorResponse, "description": "SERVER ERROR"},
    },
    tags=["bids"],
    response_model_by_alias=True,
)
async def bid_id_get(
    id: str = Path(..., description=""),
) -> Bid:
    with Session(engine) as session:
        bid = session.get(BidSQLModel, uuid.UUID(id).hex)
        if not bid:
            raise HTTPException(status_code=404, detail="Auction not found")

        return Bid(**bid.dict())


@router.post(
    "/bid",
    responses={
        201: {"model": Bid, "description": "CREATED"},
        "4XX": {"model": ErrorResponse, "description": "CLIENT ERROR"},
        "5XX": {"model": ErrorResponse, "description": "SERVER ERROR"},
    },
    tags=["bids"],
    response_model_by_alias=True,
)
async def bid_post(
    bid: Bid = Body(None, description=""),
) -> Bid:
    bid_deserialized = BidSQLModel(**bid.to_dict())
    with Session(engine) as session:
        session.add(bid_deserialized)
        session.commit()
        session.refresh(bid_deserialized)

        return Bid(**bid_deserialized.dict())
