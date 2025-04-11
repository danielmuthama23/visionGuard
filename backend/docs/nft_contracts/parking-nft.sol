// docs/nft_contracts/parking-nft.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract ParkingNFT is ERC721, Ownable {
    struct ParkingDetails {
        string licensePlate;
        string vehicleType;
        uint256 entryTime;
        uint256 exitTime;
        string lotId;
    }

    uint256 private _tokenIdCounter;
    mapping(uint256 => ParkingDetails) private _parkingRecords;
    
    event NFTCreated(
        uint256 indexed tokenId,
        address indexed owner,
        string lotId,
        uint256 entryTime
    );

    constructor() ERC721("VisionGuardParking", "VGPT") {}

    function mintParkingNFT(
        address to,
        string memory licensePlate,
        string memory vehicleType,
        string memory lotId
    ) external onlyOwner returns (uint256) {
        _tokenIdCounter++;
        uint256 newTokenId = _tokenIdCounter;
        
        _parkingRecords[newTokenId] = ParkingDetails({
            licensePlate: licensePlate,
            vehicleType: vehicleType,
            entryTime: block.timestamp,
            exitTime: 0,
            lotId: lotId
        });

        _safeMint(to, newTokenId);
        emit NFTCreated(newTokenId, to, lotId, block.timestamp);
        return newTokenId;
    }

    function recordExit(uint256 tokenId) external onlyOwner {
        require(_exists(tokenId), "Token does not exist");
        _parkingRecords[tokenId].exitTime = block.timestamp;
    }

    function getParkingDetails(uint256 tokenId) public view returns (ParkingDetails memory) {
        require(_exists(tokenId), "Token does not exist");
        return _parkingRecords[tokenId];
    }

    function _baseURI() internal pure override returns (string memory) {
        return "https://api.visionguard.io/nft/";
    }
}