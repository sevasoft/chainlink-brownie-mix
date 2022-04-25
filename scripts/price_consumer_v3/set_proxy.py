from brownie import PriceConsumerV3, network

from helper_brownie import get_account
from helper_chainlink import PRICE_CONSUMER_V3


def set_price_feed_proxy(_id: str = ""):

    """
    @notice Call PriceConsumerV3 contract to set price feed proxy address.
    @param _id Price feed ID that is assigned in the config (e.g. 1).
    """

    account = get_account()
    price_consumer_v3 = PriceConsumerV3[-1]

    print(
        f"Calling PriceConsumerV3 contract {price_consumer_v3.address} on network {network.show_active()}"
    )

    pair = PRICE_CONSUMER_V3[_id]["pair"]
    proxy = PRICE_CONSUMER_V3[_id]["proxy"]

    tx = price_consumer_v3.setPriceFeedProxy(pair, proxy, {"from": account})
    tx.wait(1)

    print(
        "Set successfully the price feed proxy to {price_consumer_v3.address}. Transaction Hash: {tx.hash}\n",
        "Run the following to read just set price feed proxy:\n",
        f"brownie run scripts/price_consumer_v3/get_price.py get_latest_price {pair} --network {network.show_active()}",
    )


def main():
    set_price_feed_proxy(input("Price feed proxy ID: "))
