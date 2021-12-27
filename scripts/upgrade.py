from scripts.deploy import deploy
from scripts.helpers import get_account, upgrade_proxy
from brownie import BoxV2, TransparentUpgradeableProxy, ProxyAdmin, Contract


def upgrade():
    account = get_account()
    transparent_proxy = TransparentUpgradeableProxy[-1]
    proxy_admin = ProxyAdmin[-1]

    box_v2 = BoxV2.deploy({"from": account})

    upgrade_proxy(
        transparent_proxy, box_v2.address, account, proxy_admin, box_v2.init, 22
    )

    box_proxy = Contract.from_abi(BoxV2._name, transparent_proxy.address, BoxV2.abi)
    print(box_proxy.value())
    box_proxy.increment({"from": account}).wait(1)
    print(box_proxy.value())


def main():
    # deploy()
    upgrade()
