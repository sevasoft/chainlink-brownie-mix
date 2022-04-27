import time

from brownie import network

from helper_brownie import CHAINS
from helper_chainlink import KEEPER
from scripts.keeper.add_employee import add_employee
from scripts.keeper.check_upkeep import check_upkeep
from scripts.keeper.deploy import deploy
from scripts.keeper.perform_upkeep import perform_upkeep


def main():
    employee_id = "1"

    if network.show_active() in CHAINS["local"]:
        deploy()
        add_employee(employee_id)

        time.sleep(KEEPER[employee_id]["payment_interval"])

        check_upkeep()
        perform_upkeep()
