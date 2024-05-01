# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from scavenger_auctions.models.bid import Bid
from scavenger_auctions.models.error_response import ErrorResponse


class BaseBidsApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseBidsApi.subclasses = BaseBidsApi.subclasses + (cls,)

    def bid_id_get(
        self,
        id: str,
    ) -> Bid: ...

    def bid_post(
        self,
        bid: Bid,
    ) -> Bid: ...
