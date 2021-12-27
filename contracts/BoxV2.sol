// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract BoxV2 {
    uint256 public value;
    event ValueChanged(uint256 _value);

    function storeValue(uint256 _value) public {
        value = _value;
        emit ValueChanged(value);
    }

    function increment() public {
        value += 1;
        emit ValueChanged(value);
    }

    function init(uint256 _initialValue) public {
        value = _initialValue;
        emit ValueChanged(value);
    }
}
