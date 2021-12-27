from brownie import ProxyAdmin, TransparentUpgradeableProxy, Box, BoxV2, Contract
from scripts.helpers import encode_function_data, get_account, upgrade_proxy


def deploy():
    account = get_account()

    # deploy logic contracts
    box = Box.deploy({"from": account})

    # deploy admin proxy
    proxy_admin = ProxyAdmin.deploy({"from": account})

    # deploy transaprent proxy
    encoded_init_function = encode_function_data(box.init, 12)
    TransparentUpgradeableProxy.deploy(
        box.address, proxy_admin.address, encoded_init_function, {"from": account}
    )


def main():
    deploy()
