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
from scavenger_auctions.apis.auctions_api_base import BaseAuctionsApi  # noqa: F401
from scavenger_auctions.models.auction import Auction
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
        201: {"description": "DELETED"},
        "4XX": {"model": ErrorResponse, "description": "CLIENT ERROR"},
        "5XX": {"model": ErrorResponse, "description": "SERVER ERROR"},
    },
    tags=["auctions"],
    response_model_by_alias=True,
)
async def auction_id_delete(
    id: str = Path(..., description=""),
) -> None:
    ...


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
) -> AuctionSQLModel:
    with Session(engine) as session:
        auction = session.get(AuctionSQLModel, uuid.UUID(id).hex)
        if not auction:
            raise HTTPException(status_code=404, detail="Auction not found")

        return auction


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
    ...


@router.post(
    "/auction",
    responses={
        200: {"model": Auction, "description": "CREATED"},
        "4XX": {"model": ErrorResponse, "description": "CLIENT ERROR"},
        "5XX": {"model": ErrorResponse, "description": "SERVER ERROR"},
    },
    tags=["auctions"],
    response_model_by_alias=True,
)
async def auction_post(
    auction: Auction = Body(None, description=""),
) -> Auction:
    auction_deserialized = AuctionSQLModel(**auction.to_dict())
    with Session(engine) as session:
        session.add(auction_deserialized)
        session.commit()
        session.refresh(auction_deserialized)
        return Auction(**auction_deserialized.dict())
