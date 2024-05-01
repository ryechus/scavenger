# coding: utf-8

from fastapi.testclient import TestClient

from scavenger_auctions.models.bid import Bid  # noqa: F401
from scavenger_auctions.models.error_response import ErrorResponse  # noqa: F401


def test_bid_id_get(client: TestClient):
    """Test case for bid_id_get"""

    headers = {}
    # uncomment below to make a request
    # response = client.request(
    #    "GET",
    #    "/bid/{id}".format(id='id_example'),
    #    headers=headers,
    # )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_bid_post(client: TestClient):
    """Test case for bid_post"""
    bid = {
        "client_timestamp": "2000-01-23T04:56:07.000+00:00",
        "max_bid_amount": 6.027456183070403,
        "bid_amount": 0.09008281904610115,
        "auction_id": "046b6c7f-0b8a-43b9-b35d-6489e6daee91",
        "id": "046b6c7f-0b8a-43b9-b35d-6489e6daee91",
        "customer_id": "046b6c7f-0b8a-43b9-b35d-6489e6daee91",
    }

    headers = {}
    # uncomment below to make a request
    # response = client.request(
    #    "POST",
    #    "/bid",
    #    headers=headers,
    #    json=bid,
    # )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200
