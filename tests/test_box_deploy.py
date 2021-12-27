from brownie import Box, TransparentUpgradeableProxy, ProxyAdmin, Contract, exceptions
from scripts.helpers import get_account, encode_function_data
import pytest


def test_should_deploy_box_v1():
    account = get_account()

    # deploy logic contracts
    box_v1 = Box.deploy({"from": account})

    # deploy admin proxy
    proxy_admin = ProxyAdmin.deploy({"from": account})
    encoded_init_function = encode_function_data()
    transparent_proxy = TransparentUpgradeableProxy.deploy(
        box_v1.address, proxy_admin.address, encoded_init_function, {"from": account}
    )

    box_proxy = Contract.from_abi(Box._name, transparent_proxy.address, Box.abi)
    box_proxy.storeValue(5, {"from": account}).wait(1)
    assert box_proxy.value() == 5
    with pytest.raises(AttributeError):
        box_v1.increment().wait(1)
