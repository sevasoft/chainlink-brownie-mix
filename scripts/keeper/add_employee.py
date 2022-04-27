from brownie import Keeper

from helper_chainlink import KEEPER


def add_employee(_id: str = ""):
    employee = KEEPER[_id]["employee"]
    payment_interval = KEEPER[_id]["payment_interval"]
    salary = KEEPER[_id]["salary"]

    tx = Keeper[-1].addEmployee(employee, payment_interval, salary)
    tx.wait(1)


def main():
    add_employee(input("Provide employee ID: "))
