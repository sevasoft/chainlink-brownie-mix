from brownie import network
from brownie.network.web3 import Web3

from helper_brownie import get_account, get_mock

CHAINLINK = {
    "development": {
        "api_consumer": {
            "link_token": get_mock("chainlink", "api_consumer", "", "link_token"),
            "1": {
                "name": "Latest CPI in Belgium",
                "descirption": "Get the latest CPI in Belgium in the form of uint256. Data is taken from the Belgian statistical office",
                "url": "https://bestat.statbel.fgov.be/bestat/api/views/876acb9d-4eae-408e-93d9-88eae4ad1eaf/result/JSON",
                "path": "facts,6,Cosumtieprijsindex",
                "http": 2,  # uint256
                "oracle": get_mock("chainlink", "api_consumer", "1", "oracle"),
                "payment": 100000000000000000,  # 0.1 LINK
                "job_id": "d5270d1c311941d0b08bead21fea7747",
            },
        },
        "price_consumer_v3": {
            "1": {
                "pair": "ETH/USDT",
                "proxy": get_mock("chainlink", "price_consumer_v3", "1", "proxy"),
                "hearbeat": 60,  # minutes
                "decimals": 18,  # amount
            }
        },
    },
    "kovan": {
        "api_consumer": {
            "link_token": "0xa36085F69e2889c224210F603D836748e7dC0088",
            "1": {
                "name": "Latest CPI in Belgium",
                "descirption": "Get the latest CPI in Belgium in the form of uint256. Data is taken from the Belgian statistical office",
                "url": "https://bestat.statbel.fgov.be/bestat/api/views/876acb9d-4eae-408e-93d9-88eae4ad1eaf/result/JSON",
                "path": "facts,6,Cosumtieprijsindex",
                "http": 2,  # uint256
                "oracle": "0xc57B33452b4F7BB189bB5AfaE9cc4aBa1f7a4FD8",
                "payment": 100000000000000000,  # 0.1 LINK
                "job_id": "d5270d1c311941d0b08bead21fea7747",
            },
        },
        "price_consumer_v3": {
            "1": {
                "pair": "ETH/USDT",
                "proxy": "0x10900f50d1bC46b4Ed796C50A4Cc63791CaF7501",
                "hearbeat": 60,  # minutes
                "decimals": 18,
            }
        },
    },
}

API_CONSUMER = CHAINLINK[f"{network.show_active()}"]["api_consumer"]
PRICE_CONSUMER_V3 = CHAINLINK[f"{network.show_active()}"]["price_consumer_v3"]


def fund_with_link(_to, _from=None, _amount=Web3.toWei(0.2, "ether")):
    account = _from if _from else get_account()
    link_token = API_CONSUMER["link_token"]
    ### Keep this line to show how it could be done without deploying a mock
    # tx = interface.LinkTokenInterface(link_token.address).transfer(
    #     contract_address, amount, {"from": account}
    # )
    tx = link_token.transfer(_to, _amount, {"from": account})
    print("Funded {}".format(_to))
    return tx
