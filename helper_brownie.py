from os import error

from brownie import accounts, config, network
from brownie import (
    LinkToken,
    MockOracle,
    MockV3AggregatorETHUSDT,
    VRFCoordinatorV2Mock,
    accounts,
    config,
    network,
    web3,
)


CHAINS = {
    "local": ["ganache-local", "development", "hardhat", "localhost"],
    "test": ["rinkeby", "kovan", "mumbai"],
    "main": ["mainnet", "polygon"],
}

BLOCK_CONFIRMATIONS_FOR_VERIFICATION: int = 1 if network.show_active() in CHAINS["local"] else 6


def is_verifiable_contract() -> bool:
    return config["networks"][network.show_active()].get("verify", False)


def get_account(index=None, id=None, wallet=None):
    """Return current user account."""
    if index and (network.show_active() in CHAINS["local"]):
        return accounts[index]
    elif network.show_active() in CHAINS["local"]:
        return accounts[0]
    elif id:
        return accounts.load(id)
    elif wallet:
        return config["wallets"][wallet]
    return accounts.add(config["wallets"][network.show_active()]["from_key"])


def get_mock(_provider: str = "", _service: str = "", _id: str = "", _name: str = ""):

    if network.show_active() not in CHAINS["local"]:
        raise error(f"You are on {network.show_active()}. Switch to development.")

    MOCK = {
        "chainlink": {
            "api_consumer": {
                "link_token": LinkToken,
                "1": {
                    "oracle": MockOracle,
                },
            },
            "price_consumer_v3": {
                "1": {
                    "proxy": MockV3AggregatorETHUSDT,
                }
            },
            "vrf_coordinator_v2": {"1": {"vrf_coordinator": VRFCoordinatorV2Mock}},
        }
    }

    contract_type = (
        MOCK[_provider][_service][_id][_name] if _id else MOCK[_provider][_service][_name]
    )

    if len(contract_type) <= 0:
        deploy_mocks()
    contract = contract_type[-1]

    return contract


DECIMALS = 18
INITIAL_VALUE = web3.toWei(2000, "ether")
BASE_FEE = 100000000000000000  # The premium
GAS_PRICE_LINK = 1e9  # Some value calculated depending on the Layer 1 cost and Link


def deploy_mocks():
    """
    Use this script if you want to deploy mocks to a testnet
    """
    print(f"The active network is {network.show_active()}")
    print("Deploying Mocks...")
    account = get_account()
    print("Deploying Mock Link Token...")
    link_token = LinkToken.deploy({"from": account})
    print("Deploying Mock Price Feed ETH/USDT...")
    mock_price_feed = MockV3AggregatorETHUSDT.deploy(DECIMALS, INITIAL_VALUE, {"from": account})
    print(f"Deployed to {mock_price_feed.address}")
    print("Deploying Mock VRFCoordinator...")
    mock_vrf_coordinator = VRFCoordinatorV2Mock.deploy(BASE_FEE, GAS_PRICE_LINK, {"from": account})
    print(f"Deployed to {mock_vrf_coordinator.address}")

    print("Deploying Mock Oracle...")
    mock_oracle = MockOracle.deploy(link_token.address, {"from": account})
    print(f"Deployed to {mock_oracle.address}")
    print("Mocks Deployed!")


def get_event_value(_tx, _event_name: str, _key: str):
    return _tx.events[_event_name][_key]
