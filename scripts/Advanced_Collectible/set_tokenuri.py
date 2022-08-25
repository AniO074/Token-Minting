from brownie import config,network,accounts,AdvancedCollectible
from scripts.helpfulScripts import get_breed

dog_metadata_dic = {
    "pug": "ipfs://Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-pug.json",
    "shiba-inu": "ipfs://QmdryoExpgEQQQgJPoruwGJyZmz6SqV4FRTX1i73CT3iXn?filename=1-shiba-inu.json",
    "st-bernard": "ipfs://QmbBnUjyHHN7Ytq9xDsYF9sucZdDJLRkWz7vnZfrjMXMxs?filename=2-st-bernard.json",
}

OPENSEA_FORMAT = "https://testnets.opensea.io/assets/{}/{}"

def main():
    advanced_collectible = AdvancedCollectible[len(AdvancedCollectible)-1]
    number_of_tokens_deployed = advanced_collectible.tokenCounter()
    print("Number of tokens you've deployed:{}".format(number_of_tokens_deployed))

    for token_id in range(number_of_tokens_deployed):
        if not advanced_collectible.tokenURI(token_id).startswith("https://"):
            print("Setting tokenURI  of {}".format(token_id))
            breed=get_breed(advanced_collectible.tokenIdtoBreed(token_id))
            set_tokenURI(token_id,advanced_collectible,dog_metadata_dic[breed])
        else:
            print("Skipping {},we've already set tokenURI".format(token_id))


def set_tokenURI(token_id,nft_contract,tokenURI):
    dev = accounts.add(config["wallets"]["from_key"])
    nft_contract.setTokenURI(token_id,tokenURI,{"from":dev})
    print(
        "Awesome! you can now view your nft at {}".format(
            OPENSEA_FORMAT.format(nft_contract.address,token_id)
        )
    )
    print("Please give upto 20 minutes,and hit 'refresh metadata'")
