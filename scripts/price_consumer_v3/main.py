from scripts.price_consumer_v3.deploy import deploy
from scripts.price_consumer_v3.get_decimals import get_decimals
from scripts.price_consumer_v3.get_price import get_price
from scripts.price_consumer_v3.get_proxy import get_proxy
from scripts.price_consumer_v3.set_proxy import set_price_feed_proxy


def main():
    id_ = "1"

    deploy()
    set_price_feed_proxy(id_)
    get_price(id_)
    get_proxy(id_)
    get_decimals(id_)
