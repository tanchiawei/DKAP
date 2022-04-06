// SPDX-License-Identifier: GPL-3.0
pragma solidity >= 0.7 .0 < 0.9 .0;

contract PubKey {
    //dynamic array

    struct pubKey {
        address permittedAddress;
        string pubValue;
        bool flag; 
    }
    mapping(uint => pubKey) permitted;
    uint permittedLength;
    event VoteCast(address test, address test2);
        //create a variable called name
    string private name;

    
    //declare an event
    event PairEvent(string STATUS);
    event PairError(string STATUS, bytes ADDRESS);
    constructor() {}

    function destroy() public {
        address payable admin;
        admin = payable(msg.sender);
        selfdestruct(admin);
    }
    function delete_public_key() public returns(string memory){
            for (uint i = 0; i < permittedLength; i++) {
                if (permitted[i].permittedAddress == msg.sender) {
                    permitted[i].pubValue = "";
                    emit PairEvent("DELETE");
                    return "Success";
                }
            }
            return "There seems to be a problem";
        
    }

    function getPubKey() view public returns(pubKey[] memory) {

        pubKey[] memory ret = new pubKey[](permittedLength);
        for (uint i = 0; i < permittedLength; i++) {
            ret[i] = permitted[i];
        }
        return ret;
    }

    function setPubKey(string memory inPubKey) public returns(string memory) {
        for (uint i = 0; i < permittedLength; i++) {

            if (permitted[i].permittedAddress == msg.sender) {
                permitted[i].pubValue = inPubKey;
                emit PairEvent("NEW");
                
                return "Success";
                        
            }

        }
        emit PairEvent("Not Authorized");
        return "Not Authorized";

    }
    function adminSetPermittedAddresses(address inPermittedAddress) public {
        bool skip_remaining = false;
        bool address_exist = false;
        if (msg.sender == 0x9e659CF30F66956E2Dedf4027b81e39Ff1F0a7a9) {
            if (permittedLength == 0){
                    permitted[permittedLength].flag = true;
                    permitted[permittedLength].pubValue = "";
                    permitted[permittedLength].permittedAddress = inPermittedAddress;
                    permittedLength++;
            }else{
                for (uint i = 0; i < permittedLength; i++) {
                    if(permitted[i].permittedAddress == inPermittedAddress){
                        address_exist = true;
                        //Address already exist
                    }
                }
                if (address_exist == false){
                for (uint i = 0; i < permittedLength; i++) {
                        if (permitted[i].permittedAddress == 0x0000000000000000000000000000000000000000){
                            permitted[i].flag = true;
                            permitted[i].pubValue = "";
                            permitted[i].permittedAddress = inPermittedAddress;
                            skip_remaining = true;
                            //permittedLength++;
                        }
                }
                if (skip_remaining == false){
                            permitted[permittedLength].flag = true;
                            permitted[permittedLength].pubValue = "";
                            permitted[permittedLength].permittedAddress = inPermittedAddress;
                            permittedLength++;
                }
            }   

            }
            
            
        }
    }

    function adminRemovePermittedAdress(address inRemoveAddress) public {
        if (msg.sender == 0x9e659CF30F66956E2Dedf4027b81e39Ff1F0a7a9) {
            for (uint i = 0; i < permittedLength; i++) {
                if (permitted[i].permittedAddress == inRemoveAddress) {
                    permitted[i].pubValue = "";
                    permitted[i].flag = false;
                    permitted[i].permittedAddress = address(0);
                    emit PairEvent("DELETE");
                }
            }
        }


    }
}