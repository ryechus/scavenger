# coding: utf-8

import importlib
import pkgutil
import uuid
from http.client import HTTPException
from typing import Dict, List, Union  # noqa: F401

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
from sqlmodel import Session, select

import openapi_server.impl
from scavenger_auctions.apis.auctions_api_base import BaseAuctionsApi  # noqa: F401
from scavenger_auctions.models.auction import Auction
from scavenger_auctions.models.auction_list import AuctionList
from scavenger_auctions.models.error_response import ErrorResponse
from scavenger_auctions.models.extra_models import TokenModel  # noqa: F401
from scavenger_auctions.sql_models.core import Auction as AuctionSQLModel
from scavenger_auctions.sql_models.core import engine

router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.delete(
    "/auction/{id}",
    responses={
        200: {"description": "DELETED"},
        "4XX": {"model": ErrorResponse, "description": "CLIENT ERROR"},
        "5XX": {"model": ErrorResponse, "description": "SERVER ERROR"},
    },
    tags=["auctions"],
    response_model=None,
)
async def auction_id_delete(
    id: str = Path(..., description=""),
) -> Union[Response, HTTPException]:
    with Session(engine) as session:
        auction = session.get(AuctionSQLModel, uuid.UUID(id).hex)
        if not auction:
            raise HTTPException(status_code=404, detail="Auction not found")

        auction.is_deleted = True
        session.add(auction)
        session.commit()
        session.refresh(auction)

        return Response(status_code=200)


@router.get(
    "/auction/{id}",
    responses={
        200: {"model": Auction, "description": "OK"},
        "4XX": {"model": ErrorResponse, "description": "CLIENT ERROR"},
        "5XX": {"model": ErrorResponse, "description": "SERVER ERROR"},
    },
    tags=["auctions"],
    response_model_by_alias=True,
)
async def auction_id_get(
    id: str = Path(..., description=""),
) -> Auction:
    with Session(engine) as session:
        auction = session.get(AuctionSQLModel, uuid.UUID(id).hex)
        if not auction:
            raise HTTPException(status_code=404, detail="Auction not found")

        return Auction(**auction.dict())


@router.patch(
    "/auction/{id}",
    responses={
        200: {"model": Auction, "description": "CHANGED"},
        "4XX": {"model": ErrorResponse, "description": "CLIENT ERROR"},
        "5XX": {"model": ErrorResponse, "description": "SERVER ERROR"},
    },
    tags=["auctions"],
    response_model_by_alias=True,
)
async def auction_id_patch(
    id: str = Path(..., description=""),
    auction: Auction = Body(None, description=""),
) -> Auction:
    with Session(engine) as session:
        updates = auction.to_dict()
        auction = session.get(AuctionSQLModel, uuid.UUID(id).hex)
        if not auction:
            raise HTTPException(status_code=404, detail="Auction not found")

        auction.sqlmodel_update(updates)

        session.add(auction)
        session.commit()
        session.refresh(auction)

        return Auction(**auction.dict())


@router.get(
    "/auctions",
    responses={
        200: {"model": AuctionList, "description": "OK"},
        "4XX": {"model": ErrorResponse, "description": "CLIENT ERROR"},
        "5XX": {"model": ErrorResponse, "description": "SERVER ERROR"},
    },
    tags=["auctions"],
    response_model_by_alias=True,
)
async def auctions_get() -> AuctionList:
    with Session(engine) as session:
        auctions = session.exec(select(AuctionSQLModel).where(AuctionSQLModel.is_deleted == False)).all()
        return AuctionList(data=[Auction(**auction.dict()) for auction in auctions])


@router.post(
    "/auctions",
    responses={
        200: {"model": Auction, "description": "CREATED"},
        "4XX": {"model": ErrorResponse, "description": "CLIENT ERROR"},
        "5XX": {"model": ErrorResponse, "description": "SERVER ERROR"},
    },
    tags=["auctions"],
    response_model_by_alias=True,
)
async def auctions_post(
    auction: Auction = Body(None, description=""),
) -> Auction:
    auction_deserialized = AuctionSQLModel(**auction.to_dict())
    with Session(engine) as session:
        session.add(auction_deserialized)
        session.commit()
        session.refresh(auction_deserialized)
        return Auction(**auction_deserialized.dict())
