from brownie import Keeper

from helper_brownie import (
    BLOCK_CONFIRMATIONS_FOR_VERIFICATION,
    get_account,
    is_verifiable_contract,
)


def deploy():
    deployer = get_account()

    keeper = Keeper.deploy({"from": deployer})

    if is_verifiable_contract():
        keeper.tx.wait(BLOCK_CONFIRMATIONS_FOR_VERIFICATION)
        Keeper.publish_source(keeper)

    return keeper


def main():
    deploy()
