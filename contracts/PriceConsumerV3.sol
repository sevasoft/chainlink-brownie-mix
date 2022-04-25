// SPDX-Licence-Identifier: MIT
pragma solidity >=0.8.7 <0.8.12;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

error PriceFeedProxyAlreadyExists(address _proxy);

contract PriceConsumerV3 is Ownable {
    using Counters for Counters.Counter;

    struct PriceFeed {
        string pair;
        address proxy;
    }

    Counters.Counter private _s_priceFeedIdCounter;

    mapping(uint256 => PriceFeed) public s_priceFeeds;
    mapping(address => bool) public s_existing;

    modifier notExisting(address _proxy) {
        if (s_existing[_proxy]) revert PriceFeedProxyAlreadyExists(_proxy);
        _;
    }

    /**
     * Set price feed proxy.
     * @dev https://docs.chain.link/docs/reference-contracts/
     * @param _pair Currency pair. Recommended style: ETH/USD
     * @param _proxy Price feed proxy address.
     */
    function setPriceFeedProxy(string memory _pair, address _proxy)
        public
        onlyOwner
        notExisting(_proxy)
    {
        _s_priceFeedIdCounter.increment();
        uint256 newId = _s_priceFeedIdCounter.current();

        s_priceFeeds[newId] = PriceFeed(_pair, _proxy);
        s_existing[_proxy] = true;
    }

    function totalPriceFeeds() public view returns (uint256) {
        return _s_priceFeedIdCounter.current();
    }

    function pair(uint256 _id)
        public
        view
        returns (string memory)
    {
        return s_priceFeeds[_id].pair;
    }

    /**
     * Get price feed proxy address.
     * @param _id ID of the price feed proxy (e.g. 1). See setPriceFeedProxy
     * @return Proxy address of a provided currency pair.
     */
    function proxy(uint256 _id)
        public
        view
        returns (address)
    {
        return s_priceFeeds[_id].proxy;
    }

    /**
     * Get latest price of a particular aggregator.
     * @param _id ID of the price feed proxy (e.g. 1). See setPriceFeedProxy
     * @return Latest price.
     */
    function price(uint256 _id) public view returns (uint256) {
        address proxy = s_priceFeeds[_id].proxy;
        AggregatorV3Interface priceFeed = AggregatorV3Interface(proxy);

        (
            /*uint80 roundID*/,
            int256 price,
            /*uint startedAt*/,
            /*uint timeStamp*/,
            /*uint80 answeredInRound*/
        ) = priceFeed.latestRoundData();

        return uint256(price);
    }

    /**
     * Get amount of decimals of a particular aggregator.
     * @param _id ID of the price feed proxy (e.g. 1). See setPriceFeedProxy
     * @return Decimals (usually 8 if x/USD or 18 if x/ETH; see docs).
     */
    function decimals(uint256 _id) public view returns (uint8) {
        address proxy = s_priceFeeds[_id].proxy;
        AggregatorV3Interface priceFeed = AggregatorV3Interface(proxy);

        return priceFeed.decimals();
    }
}
