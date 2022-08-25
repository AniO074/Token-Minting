from brownie import network,AdvancedCollectible
from metadata import sample_metadata 
from scripts.helpfulScripts import get_breed
from pathlib import Path
import os
import requests
import json

def main():
    advanced_Collectible=AdvancedCollectible[len(AdvancedCollectible)-1]
    number_of_tokens=advanced_Collectible.tokenCounter()
    print(number_of_tokens)
    write_metadata(number_of_tokens,advanced_Collectible)

def write_metadata(number_of_tokens,nft_contract):
    for token_id in range(number_of_tokens):
            collectible_meta_data = sample_metadata.metadata
            breed=get_breed(nft_contract.tokenIdtoBreed(token_id))
            meta_data_file_name = ("./metadata/{}".format(network.show_active()) + 
                                    str(token_id) + "-" + breed + ".json")
            if Path(meta_data_file_name).exists():
                print("Token exists{}".format(token_id))
            else:
                collectible_meta_data["name"] = get_breed(nft_contract.tokenIdtoBreed(token_id))
                collectible_meta_data["description"]="A cute {} puppy".format(collectible_meta_data["name"])
                print(collectible_meta_data)
            
            image_to_upload = 'none'
            if os.getenv("UPLOAD_IPFS")=='true':
                image_path = "./img/{}.png".format(breed)
                image_to_upload = upload_to_ipfs(image_path)
                collectible_meta_data["image"]=image_to_upload
                with open(meta_data_file_name,"w") as file:
                    json.dump(collectible_meta_data,file)
                if os.getenv("UPLOAD_IPFS") == 'true':
                    upload_to_ipfs(meta_data_file_name)


def upload_to_ipfs(file_path):
    with Path(file_path).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://localhost:5001"
        response = requests.post(ipfs_url + "/api/v0/add",files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        filename = file_path.split("/")[-1]
        uri = "https://ipfs.io/ipfs/{}?filename={}".format(ipfs_hash,filename)
        print(uri)
        return uri
    return None
