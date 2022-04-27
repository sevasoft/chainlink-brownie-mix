from brownie import Keeper

from helper_brownie import get_account


def check_upkeep():
    """"""
    account = get_account()
    keeper = Keeper[-1]

    upkeepNeeded, performData = keeper.checkUpkeep.call("", {"from": account})

    print(f"The status of this upkeep is currently: {upkeepNeeded}")
    print(f"Here is the perform data: {performData}")

    return upkeepNeeded, performData


def main():
    check_upkeep()
