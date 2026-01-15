// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract HealthLogger {
    struct Log {
        string dataHash;
        address user;
        uint256 timestamp;
    }

    Log[] public logs;

    event NewLogAdded(string dataHash, address user, uint256 timestamp);

    function addHash(string memory _hash, address _user) public {
        logs.push(Log(_hash, _user, block.timestamp));
        emit NewLogAdded(_hash, _user, block.timestamp);
    }

    function getLogCount() public view returns (uint256) {
        return logs.length;
    }

    function getLog(uint256 index) public view returns (string memory, address, uint256) {
        require(index < logs.length, "Index out of range");
        Log memory l = logs[index];
        return (l.dataHash, l.user, l.timestamp);
    }
}