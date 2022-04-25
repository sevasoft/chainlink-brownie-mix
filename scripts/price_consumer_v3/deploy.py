from brownie import PriceConsumerV3

from helper_brownie import (
    BLOCK_CONFIRMATIONS_FOR_VERIFICATION,
    get_account,
    is_verifiable_contract,
)


def deploy():
    deployer = get_account()

    price_consumer_v3 = PriceConsumerV3.deploy({"from": deployer})

    if is_verifiable_contract():
        price_consumer_v3.tx.wait(BLOCK_CONFIRMATIONS_FOR_VERIFICATION)
        PriceConsumerV3.publish_source(price_consumer_v3)

    return price_consumer_v3


def main():
    deploy()
