from brownie import AdvancedCollectible,network,accounts,config
from scripts.helpfulScripts import get_breed
import time

def main():
    account1 = accounts.add(config['wallets']['from_key'])
    advanced_collectible = AdvancedCollectible[len(AdvancedCollectible)-1]
    transaction = advanced_collectible.CreateCollectible("none",{'from':account1})
    transaction.wait(2)
    time.sleep(35)
    requestId = transaction.events['requestedCollectible']['requestId']
    token_id = advanced_collectible.requestIdtoTokenId(requestId)
    breed = get_breed(advanced_collectible.tokenIdtoBreed(token_id))
    print('Dog breed of tokenId {} is  {}'.format(token_id,breed))