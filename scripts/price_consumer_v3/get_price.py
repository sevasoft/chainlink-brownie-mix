from brownie import PriceConsumerV3


def get_price(_id: str = "") -> int:

    """
    @notice Call PriceConsumerV3 contract to read the latest price.
    @param _id Price feed ID (e.g. 1).
    """

    print("Calling PriceConsumerV3 contract to read the latest price...")

    price = PriceConsumerV3[-1].price(_id)
    pair = PriceConsumerV3[-1].pair(_id)

    print(f"Received successfully the latest price from {PriceConsumerV3[-1].address}")
    print(f"The latest price of {pair} pair is {price}")

    return price


def main():
    get_price(input("Price feed ID: "))
