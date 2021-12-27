from brownie import network, accounts, config
import eth_utils

NON_FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["hardhat", "development", "ganache"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = NON_FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS + [
    "mainnet-fork",
    "binance-fork",
    "matic-fork",
]


def get_account(number=None):
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    if number:
        return accounts[number]
    if network.show_active() in config["networks"]:
        account = accounts.add(config["wallets"]["from_key"])
        return account
    return None


def encode_function_data(initializer=None, *args):
    """Encodes the function call so we can work with an initializer.
    Args:
        initializer ([brownie.network.contract.ContractTx], optional):
        The initializer function we want to call. Example: `box.store`.
        Defaults to None.
        args (Any, optional):
        The arguments to pass to the initializer function
    Returns:
        [bytes]: Return the encoded bytes.
    """
    if len(args) == 0 or not initializer:
        return eth_utils.to_bytes(hexstr="0x")
    else:
        return initializer.encode_input(*args)


def upgrade_proxy(
    transparent_proxy,
    new_implementation_addr,
    account,
    proxy_admin=None,
    init_func=None,
    *args,
):
    """
    Upgrade a proxy with new implementation,
    depending on whether a proxy_admin is passed (good practice)
    and optional function with parameters to be encoded and called
    inside the logic contract after upgrading
    """
    transaction = None
    if init_func:
        encoded_func_data = encode_function_data(init_func, *args)
        if proxy_admin:
            transaction = proxy_admin.upgradeAndCall(
                transparent_proxy,
                new_implementation_addr,
                encoded_func_data,
                {"from": account},
            )
        else:
            transaction = transparent_proxy.upgradeAndCall(
                new_implementation_addr, encoded_func_data, {"from": account}
            )
    else:
        if proxy_admin:
            transaction = proxy_admin.upgrade(
                transparent_proxy, new_implementation_addr, {"from": account}
            )
        else:
            transaction = transparent_proxy.upgradeTo(
                new_implementation_addr, {"from": account}
            )
    transaction.wait(1)
    return transaction
