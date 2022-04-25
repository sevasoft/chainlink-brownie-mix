from brownie import APIConsumer

from helper_brownie import get_account
from helper_chainlink import API_CONSUMER


def set_api(_id: str = "") -> None:
    account = get_account()
    api_consumer = APIConsumer[-1]

    api: dict = API_CONSUMER[_id]

    print("\nCalling API Consumer contract to setup a new API.")

    tx = api_consumer.setAPI(
        api["url"],
        api["path"],
        api["http"],
        api["oracle"],
        api["payment"],
        api["job_id"],
        {"from": account},
    )

    tx.wait(1)


def main():
    set_api(input("Provide API ID: "))
