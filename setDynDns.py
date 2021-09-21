import requests as req
import os
from pathlib import Path

def updateGoogleDomains(info, currentIpv4):
    for dict in info:
        keys = ["username", "password", "hostname"]
        for key in keys:
            goodFormat = True
            if dict.get(key) == None:
                goodFormat = False
                print(f"Bad format for last record in googleDomainsInfo.txt.")
                break

        if goodFormat:                
            url = "https://"+dict["username"]+":"+dict["password"]+"@domains.google.com/nic/update"
            param = {"hostname": dict["hostname"], "myip": currentIpv4}
            answer = req.get(url, param)
            print(f"Answer for {dict.get('hostname')}:\t"+answer.text)


if __name__ == "__main__":
    #Getting current public IPv4
    currentIpv4 = req.get('https://api.ipify.org').text
    print(f'Current IPv4:\t\t{currentIpv4}')
    
    #Getting last known IPv4
    path = Path(__file__).parent.joinpath('lastIp.txt')
    lastIpv4 = ""
    if (os.path.isfile(path)):
        with open(path, "r") as reader:
            lastIpv4 = reader.read()
        print(f"Last known IPv4:\t{lastIpv4}")
    else:
        print("No previous IP known.")
    

    if currentIpv4 != lastIpv4:
        #Updating the new adress
        print("Updating the new adress.")
        with open(path, "w") as writer:
            writer.write(currentIpv4)
        print(f"Last known IP updated:\t{currentIpv4}")

        path = Path(__file__).parent.joinpath('googleDomainsInfo.txt')
        print("Getting authentification informations for domains.google.com.")
        if (os.path.isfile(path)):
            info = list()
            with open(path, "r") as reader:
                for number, line in enumerate(reader):
                    id = number%4
                    if id == 1:
                        info.append(dict())
                        info[-1].update({"username": line.strip()})
                        
                    elif id == 2:
                        info[-1].update({"password": line.strip()})
                        
                    elif id == 3:
                        info[-1].update({"hostname": line.strip()})
            
            print("Sending the new adresses to Google.")
            updateGoogleDomains(info, currentIpv4)


        else:
            print("No information found in googleDomainsInfo.txt.")   

    else:
        print("The IP adress did not change.")

    
    