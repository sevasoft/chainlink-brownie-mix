from brownie import PriceConsumerV3, network


def get_decimals(_id: str = "") -> int:

    """
    @param _id Price feed ID (e.g. 1).
    """

    price_consumer_v3 = PriceConsumerV3[-1]

    print(
        f"Calling PriceConsumerV3 contract {price_consumer_v3.address} on network {network.show_active()}"
    )

    decimals = price_consumer_v3.decimals(_id)

    print(
        f"Successfully called {price_consumer_v3.address}",
        f"The amount of decimals returned by {_id} price feed ID is {decimals}",
    )

    return decimals


def main():
    print(get_decimals(input("Price feed ID: ")))
