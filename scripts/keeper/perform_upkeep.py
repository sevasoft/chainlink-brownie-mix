from brownie import Keeper, network
from brownie.network.web3 import Web3

from helper_brownie import CHAINS, get_account
from scripts.keeper.check_upkeep import check_upkeep


def perform_upkeep():
    """"""
    account = get_account()
    keeper = Keeper[-1]
    upkeep_needed, perform_data = check_upkeep()

    if network.show_active in CHAINS["local"]:
        account.transfer(keeper.address, Web3.toWei(0.1, "ether"))

    if upkeep_needed == True:
        keeper.performUpkeep.call(perform_data, {"from": account})

        print("Performed Upkeep!")

        return True
    else:
        print("Did not perform upkeep.")
        return False


def main():
    perform_upkeep()
