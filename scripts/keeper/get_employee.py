from brownie import Keeper


def get_employee(_id=None):
    employee = Keeper[-1].getEmployee(int(_id))
    print(employee)

    return employee


def main():
    get_employee()
