Transparent Proxy Upgradable Pattern

The Proxy delegates the call to the setted implementation contract
ProxyAdmin acts as an admin contract to manage the TransparentUpgradeableProxy
To eliminate function clashes, non-admins can reach only logic contract's functions
and admins can call only Proxy's functionality.
