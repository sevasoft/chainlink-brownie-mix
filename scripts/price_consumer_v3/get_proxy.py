from brownie import PriceConsumerV3, network


def get_proxy(_id: str = "") -> str:

    """
    @notice Call PriceConsumerV3 contract to read proxy address.
    @param _id Price feed ID (e.g. 1).
    """

    print(
        f"Calling PriceConsumerV3 contract {PriceConsumerV3[-1].address} on network {network.show_active()}"
    )

    proxy = PriceConsumerV3[-1].proxy(_id)
    pair = PriceConsumerV3[-1].pair(_id)

    print(
        f"Successfully called contract {PriceConsumerV3[-1].address} to get proxy.\n",
        f"The price feed proxy address of {pair} pair is {proxy}",
    )

    return proxy


def main():
    get_proxy(input("Price feed ID: "))
