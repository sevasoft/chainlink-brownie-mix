from brownie import APIConsumer, network


def response(_api_id: str = "") -> None:
    api_consumer = APIConsumer[-1]

    print(
        "Reading data from API Consumer contract {} on netwrok {}".format(
            api_consumer.address, network.show_active()
        )
    )

    api = api_consumer.getApiById(int(_api_id))

    if api["http"] == 0:
        data = api["response"]["inBytes32"]
    elif api["http"] == 1:
        data = api["response"]["inInt256"]
    elif api["http"] == 2:
        data = api["response"]["inUint256"]
    elif api["http"] == 3:
        data = api["response"]["inBool"]
    else:
        data = None

    ## Uncomment when brownie'll support python3.10
    # match api["http"]:
    #    case 0: data = api["response"]["inBytes32"]
    #    case 1: data = api["response"]["inInt256"]
    #    case 2: data = api["response"]["inUint256"]
    #    case 3: data = api["response"]["inBool"]
    #    case _: data = None

    if data is None:
        print("You may have to wait a minute and then call this again, unless on a local chain!")

    print(data)


def main():
    response(input("Provide API ID: "))
