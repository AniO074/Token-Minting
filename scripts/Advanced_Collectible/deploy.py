from brownie import AdvancedCollectible,network,accounts,config
from scripts.helpfulScripts import fund_advanced_collectible


def main():
    dev = accounts.add(config['wallets']['from_key'])
    advancedCollectible = AdvancedCollectible.deploy(
        config["networks"][network.show_active()]['vrfCoordinator'],
        config["networks"][network.show_active()]['linkToken'],
        config["networks"][network.show_active()]['keyhash'],
        {"from":dev}
    )
    fund_advanced_collectible(advancedCollectible)
    return advancedCollectible
