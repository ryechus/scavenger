# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from scavenger_auctions.models.auction import Auction
from scavenger_auctions.models.error_response import ErrorResponse


class BaseAuctionsApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseAuctionsApi.subclasses = BaseAuctionsApi.subclasses + (cls,)

    def auction_id_delete(
        self,
        id: str,
    ) -> None:
        ...

    def auction_id_get(
        self,
        id: str,
    ) -> Auction:
        ...

    def auction_id_patch(
        self,
        id: str,
        auction: Auction,
    ) -> Auction:
        ...

    def auction_post(
        self,
        auction: Auction,
    ) -> Auction:
        ...
