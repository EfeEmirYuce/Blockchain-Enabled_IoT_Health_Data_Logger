pragma solidity ^0.8.0;

contract HealthLogger {
    struct Log {
        string dataHash;
        uint256 timestamp;
    }
    Log[] public logs;
    event NewLogAdded(string dataHash, uint256 timestamp);

    function addHash(string memory _hash) public {
        logs.push(Log(_hash, block.timestamp));
        emit NewLogAdded(_hash, block.timestamp);
    }

    function getLogCount() public view returns (uint256) {
        return logs.length;
    }
}