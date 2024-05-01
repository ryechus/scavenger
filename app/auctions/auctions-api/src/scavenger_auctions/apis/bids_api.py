# coding: utf-8

import importlib
import pkgutil
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

import openapi_server.impl
from scavenger_auctions.apis.bids_api_base import BaseBidsApi
from scavenger_auctions.models.bid import Bid
from scavenger_auctions.models.error_response import ErrorResponse
from scavenger_auctions.models.extra_models import TokenModel  # noqa: F401

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
    ...


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
    ...
