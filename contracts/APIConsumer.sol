// SPDX-License-Identifier: MIT
pragma solidity >=0.8.7 <0.8.12;

import "@chainlink/contracts/src/v0.8/ChainlinkClient.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract APIConsumer is ChainlinkClient, Ownable {
    using Chainlink for Chainlink.Request;
    using Counters for Counters.Counter;

    enum HTTP {
        GET_BYTES32, //     0   =   HTTP GET | JSON PARSE | -        | ETH BYTES 32
        GET_INT256, //      1   =   HTTP GET | JSON PARSE | MULTIPLY | ETH INT 256
        GET_UINT256, //     2   =   HTTP GET | JSON PARSE | MULTIPLY | ETH UINT 256
        GET_BOOL, //        3   =   HTTP GET | JSON PARSE | -        | ETH BOOL
        POST_BYTES32 //     4   =   HTTP POST| JSON PARSE | -        | ETH BYTES 32
    }

    struct LINK {
        address oracle;
        uint256 payment;
        bytes32 jobId;
        address callback;
        bool isMultipliableOutput;
        bytes4 callbackFunctionSignature;
    }

    struct RESPONSE {
        bytes32 inBytes32;
        uint256 inUint256;
        int256 inInt256;
        bool inBool;
    }

    struct API {
        uint256 id;
        string url;
        string path;
        HTTP http;
        LINK link;
        RESPONSE response;
    }

    Counters.Counter private _s_apiIdCounter;

    uint256 private _s_currentApiId;

    mapping(uint256 => API) public s_APIs; // s_ Scroll through

    // Events. Change if you would like to.
    event DataFulfilledInt(int256 _res);
    event DataFulfilledUint(uint256 _res);
    event DataFulfilledBytes32(bytes32 _res);
    event DataFulfilledBool(bool _res);
    event SetNewAPI(uint256 _id, string _url);

    constructor(address _linkToken) {
        setChainlinkToken(_linkToken); // Kovan: 0xa36085F69e2889c224210F603D836748e7dC0088
    }

    function setAPI(
        string memory _url,
        string memory _path,
        HTTP _http,
        address _oracle,
        uint256 _payment,
        bytes32 _jobId
    ) public onlyOwner {
        _s_apiIdCounter.increment();
        uint256 newId = _s_apiIdCounter.current();

        API storage api_ = s_APIs[newId];

        api_.id = newId;
        api_.url = _url;
        api_.path = _path;
        api_.http = _http;
        /* Chainlink */
        api_.link.oracle = _oracle;
        api_.link.payment = _payment;
        api_.link.jobId = _jobId;
        api_.link.callback = address(this);
        api_.link.callbackFunctionSignature = _getSelector(_http);

        api_.link.isMultipliableOutput = _isMultipliableOutput(_http);

        emit SetNewAPI(newId, _url);
    }

    function request(uint256 _apiId) public onlyOwner returns (bytes32 requestId) {
        API memory api = s_APIs[_apiId];
        _s_currentApiId = _apiId;

        Chainlink.Request memory req = buildChainlinkRequest(
            api.link.jobId,
            api.link.callback,
            api.link.callbackFunctionSignature
        );

        req.add("get", api.url);
        req.add("path", api.path);

        req = _multiplyIfRequired(api, req);

        return sendChainlinkRequestTo(api.link.oracle, req, api.link.payment);
    }

    function responseInBytes32(bytes32 _requestId, bytes32 _res)
        public
        recordChainlinkFulfillment(_requestId)
    {
        API storage api_ = s_APIs[_s_currentApiId];
        api_.response.inBytes32 = _res;
        emit DataFulfilledBytes32(_res);
    }

    /**
     * Receive the response in the form of int256.
     * @dev recordChainlinkFulfillment: Ensure that the sender and requestId are valid.
     * @dev validateChainlinkCallback(_requestId) Could be used as well instead of that modifier.
     */
    function responseInInt256(bytes32 _requestId, int256 _res)
        public
        recordChainlinkFulfillment(_requestId)
    {
        API storage api_ = s_APIs[_s_currentApiId];
        api_.response.inInt256 = _res;
        emit DataFulfilledInt(_res);
    }

    function responseInUint256(bytes32 _requestId, uint256 _res)
        public
        recordChainlinkFulfillment(_requestId)
    {
        API storage api_ = s_APIs[_s_currentApiId];
        api_.response.inUint256 = _res;
        emit DataFulfilledUint(_res);
    }

    function responseInBool(bytes32 _requestId, bool _res)
        public
        recordChainlinkFulfillment(_requestId)
    {
        API storage api_ = s_APIs[_s_currentApiId];
        api_.response.inBool = _res;
        emit DataFulfilledBool(_res);
    }

    function withdrawLink() public onlyOwner {
        LinkTokenInterface linkToken = LinkTokenInterface(chainlinkTokenAddress());
        require(
            linkToken.transfer(msg.sender, linkToken.balanceOf(address(this))),
            "Unable to transfer"
        );
    }

    function getApiById(uint256 _id) public view returns (API memory) {
        return s_APIs[_id];
    }

    function _multiplyIfRequired(API memory _api, Chainlink.Request memory _req)
        internal
        pure
        returns (Chainlink.Request memory)
    {
        if (_api.link.isMultipliableOutput && _api.http == HTTP.GET_INT256) {
            _req.addInt("times", 10**18);
        }

        if (_api.link.isMultipliableOutput && _api.http == HTTP.GET_UINT256) {
            _req.addUint("times", 10**18);
        }

        return _req;
    }

    function _getSelector(HTTP _http) internal pure returns (bytes4 selector) {
        if (_http == HTTP.GET_BYTES32) {
            return this.responseInBytes32.selector;
        }
        if (_http == HTTP.GET_INT256) {
            return this.responseInInt256.selector;
        }
        if (_http == HTTP.GET_UINT256) {
            return this.responseInUint256.selector;
        }
        if (_http == HTTP.GET_BOOL) {
            return this.responseInBool.selector;
        }
    }

    function _isMultipliableOutput(HTTP _http) internal pure returns (bool) {
        return _http == HTTP.GET_INT256 || _http == HTTP.GET_UINT256 ? true : false;
    }
}

