from brownie import AdvancedCollectible,interface,accounts,config,network

def fund_advanced_collectible(nft_contract):
    dev = accounts.add(config['wallets']['from_key'])
    link_token = interface.LinkTokenInterface(config['networks'][network.show_active()]['linkToken'])
    link_token.transfer(nft_contract,1000000000000000000,{"from":dev})

def get_breed(breed_number):
    switch = {0:'pug',1:'shiba-inu',2:'st-bernard'}
    return switch[breed_number]