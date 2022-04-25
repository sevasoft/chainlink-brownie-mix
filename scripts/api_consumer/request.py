from brownie import APIConsumer

from helper_brownie import get_account
from helper_chainlink import API_CONSUMER, fund_with_link


def request(_api_id: str = ""):
    account = get_account()
    api_consumer = APIConsumer[-1]

    amount = API_CONSUMER[_api_id]["payment"]

    tx_fund_with_link = fund_with_link(_to=api_consumer.address, _from=account, _amount=amount)
    tx_fund_with_link.wait(1)

    print("Calling API Consumer contract to request external data.")

    tx_request = api_consumer.request(_api_id, {"from": account})
    tx_request.wait(1)


def main():
    api_id = input("Provide API ID: ")
    request(api_id)
