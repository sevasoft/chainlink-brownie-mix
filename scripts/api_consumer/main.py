from scripts.api_consumer.deploy import deploy
from scripts.api_consumer.request import request
from scripts.api_consumer.response import response
from scripts.api_consumer.set_api import set_api


def main():
    api_id = "1"

    deploy()
    set_api(api_id)
    request(api_id)
    response(api_id)
