//SPDX-License-Identifier:MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";

contract AdvancedCollectible is VRFConsumerBase,ERC721
{
    //RandomNumber -> Keyhash(Unique Oracle),VrfCoordinator(Randomnumber Verifier),Link token(fee to make request)
    //
        bytes32 internal keyhash;
        uint256 internal fee;
        uint256 public tokenCounter;
        uint256 public RandomNumberReturned = 0;
        enum Breed{PUG,SHIBA_INU,ST_BERNARD}
        mapping (bytes32 => address) public requestIdtoSender;
        mapping (bytes32 => string) public requestIdtoTokenURI;
        mapping (uint256 => Breed) public tokenIdtoBreed;
        mapping (bytes32 => uint256) public requestIdtoTokenId;
        mapping (uint256 => string) public tokenIdtoTokenURI;
        mapping (bytes32 => uint256) public requestIdtoRandomNumber;
        event  requestedCollectible(bytes32 indexed requestId);
        event returnedCollectible(bytes32 indexed requestId, uint256 randomNumber);



        constructor(address _vrfcoordinator,address _linktoken,bytes32 _keyhash)
        VRFConsumerBase(_vrfcoordinator,_linktoken) 
        ERC721("Doggie","Dog")
        {
                tokenCounter = 0;
                fee = 0.1 * 10 ** 18;
                keyhash = _keyhash;
        }

        function CreateCollectible(string memory TokenURI) public returns(bytes32)
        {
            bytes32 requestId = requestRandomness(keyhash,fee);
            requestIdtoSender[requestId] = msg.sender;
            requestIdtoTokenURI[requestId] = TokenURI;
            emit requestedCollectible(requestId);
        } 

        function fulfillRandomness(bytes32 requestId,uint256 randomNumber) internal override
        {
          /*   Breed breed = Breed(randomNumber % 3);
             uint256 newTokenId = tokenCounter;
             tokenIdtoBreed[newTokenId]=breed;
             //emit breedAssigned(newTokenId,breed);
             address owner = requestIdtoSender[requestId];
             _safeMint(owner,newTokenId);  
             tokenCounter = tokenCounter + 1;      
           */
           //RandomNumberReturned = randomNumber;
           emit returnedCollectible(requestId,randomNumber);
           RandomNumberReturned = randomNumber;
           address dogOwner = requestIdtoSender[requestId];
           string memory TokenUri = requestIdtoTokenURI[requestId];
            uint256 newTokenId = tokenCounter;
            requestIdtoRandomNumber[requestId]=randomNumber;
            tokenIdtoTokenURI[newTokenId]=TokenUri;
            _safeMint(dogOwner,newTokenId);
            tokenURI(newTokenId);  //Implicitly calls the BaseURI and maps the TokenURI with TokenID in the ABI
            Breed breed = Breed(randomNumber % 3);
            tokenIdtoBreed[newTokenId] = breed;
            requestIdtoTokenId[requestId] = newTokenId;
            tokenCounter = tokenCounter + 1;
        }

        function _baseURI() internal view override returns(string memory)
        {
                return tokenIdtoTokenURI[tokenCounter];
        }

        function setTokenURI(uint256 tokenId,string memory _tokenURI) public 
        {
            require(
                _isApprovedOrOwner(_msgSender(),tokenId),
                "ERC721:transfer caller is not owner nor approved"
            );
            tokenURI(tokenId);
        }
}