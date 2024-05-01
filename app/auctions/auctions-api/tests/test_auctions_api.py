# coding: utf-8

from fastapi.testclient import TestClient

from scavenger_auctions.models.auction import Auction  # noqa: F401
from scavenger_auctions.models.error_response import ErrorResponse  # noqa: F401


def test_auction_id_delete(client: TestClient):
    """Test case for auction_id_delete"""

    headers = {}
    # uncomment below to make a request
    # response = client.request(
    #    "DELETE",
    #    "/auction/{id}".format(id='id_example'),
    #    headers=headers,
    # )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_auction_id_get(client: TestClient):
    """Test case for auction_id_get"""

    headers = {}
    # uncomment below to make a request
    # response = client.request(
    #    "GET",
    #    "/auction/{id}".format(id='id_example'),
    #    headers=headers,
    # )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_auction_id_patch(client: TestClient):
    """Test case for auction_id_patch"""
    auction = {
        "starting_datetime": "2000-01-23T04:56:07.000+00:00",
        "starting_price": 0.8008281904610115,
        "name": "name",
        "ending_datetime": "2000-01-23T04:56:07.000+00:00",
        "id": "046b6c7f-0b8a-43b9-b35d-6489e6daee91",
        "current_bid": {
            "bid_amount": 6.027456183070403,
            "customer": {"id": "046b6c7f-0b8a-43b9-b35d-6489e6daee91", "pseudonym": "pseudonym"},
        },
    }

    headers = {}
    # uncomment below to make a request
    # response = client.request(
    #    "PATCH",
    #    "/auction/{id}".format(id='id_example'),
    #    headers=headers,
    #    json=auction,
    # )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_auction_post(client: TestClient):
    """Test case for auction_post"""
    auction = {
        "starting_datetime": "2000-01-23T04:56:07.000+00:00",
        "starting_price": 0.8008281904610115,
        "name": "name",
        "ending_datetime": "2000-01-23T04:56:07.000+00:00",
        "id": "046b6c7f-0b8a-43b9-b35d-6489e6daee91",
        "current_bid": {
            "bid_amount": 6.027456183070403,
            "customer": {"id": "046b6c7f-0b8a-43b9-b35d-6489e6daee91", "pseudonym": "pseudonym"},
        },
    }

    headers = {}
    # uncomment below to make a request
    # response = client.request(
    #    "POST",
    #    "/auction",
    #    headers=headers,
    #    json=auction,
    # )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200
