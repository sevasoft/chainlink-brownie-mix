from brownie import APIConsumer

from helper_brownie import (
    BLOCK_CONFIRMATIONS_FOR_VERIFICATION,
    get_account,
    is_verifiable_contract,
)
from helper_chainlink import API_CONSUMER


def deploy():
    deployer = get_account()
    link_token = API_CONSUMER["link_token"]

    api_consumer = APIConsumer.deploy(link_token, {"from": deployer})

    if is_verifiable_contract():
        api_consumer.tx.wait(BLOCK_CONFIRMATIONS_FOR_VERIFICATION)
        APIConsumer.publish_source(api_consumer)

    return api_consumer


def main():
    deploy()
