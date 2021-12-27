from scripts.helpers import get_account, encode_function_data, upgrade_proxy
from brownie import (
    Box,
    BoxV2,
    ProxyAdmin,
    TransparentUpgradeableProxy,
    Contract,
    exceptions,
)
import pytest


def test_should_upgrade_to_box_v2():
    account = get_account()
    box = Box.deploy(
        {"from": account},
    )
    proxy_admin = ProxyAdmin.deploy({"from": account})
    box_encoded_func_call = encode_function_data()
    transparent_proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_func_call,
        {"from": account},
    )
    box_v2 = BoxV2.deploy(
        {"from": account},
    )
    box_proxy = Contract.from_abi("BoxV2", transparent_proxy.address, BoxV2.abi)
    with pytest.raises(exceptions.VirtualMachineError):
        box_proxy.increment({"from": account})
    upgrade_proxy(transparent_proxy, box_v2.address, account, proxy_admin)
    assert box_proxy.value() == 0
    box_proxy.increment({"from": account})
    assert box_proxy.value() == 1
