import requests,colorama,xmltodict,json,os,ast
import lxml.html as html

colorama.init(autoreset=True)

def input_colorama(color,message) :
    print(color+message, end = '')
    return input()


   
def EveryThingToID64(something):
    headers = {'User-Agent':"Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36","content-type": "application/json","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9","Accept-language":"en-US,en;q=0.5"}
    r = requests.get("https://steamid.xyz/"+something,headers = headers).text
    tree = html.fromstring(r)
    ID64 = tree.xpath('//*[@id="guide"]/input[4]')
    return ID64[0].value

def GetGamesInDict(profile):
    p = EveryThingToID64(profile)
    headers = {'User-Agent':"Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36","content-type": "application/json","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9","Accept-language":"en-US,en;q=0.5"}
    r = requests.get(f"https://steamcommunity.com/profiles/{p}/games/?tab=all&xml=1",headers = headers).text
    d = xmltodict.parse(r)
    return d

def SaveData(p,data):
    f = open("Profiles/"+p,"w+",encoding="utf-8")
    f.write(str(data))
    f.close()

def LoadProfiles():
    profiles = os.listdir("Profiles")
    return profiles

def LoadProfileData(profilename):
    f = open("Profiles/"+profilename,"r",encoding="utf8")
    data = f.read()
    data = ast.literal_eval(data)
    f.close()
    return data
    
def ParseGames(p):
    info = GetGamesInDict(p)
    ProfileName = info["gamesList"]["steamID"]
    GamesCount = len(info["gamesList"]["games"]["game"])
    print(colorama.Fore.RED+"====================")
    print(colorama.Fore.GREEN + "Profile Name: "+ ProfileName)
    print(colorama.Fore.GREEN+"Games on Profile: "+str(GamesCount))
    DwG = {}
    for game in info["gamesList"]["games"]["game"]:
        try:
            DwG[game["name"]] = game["hoursOnRecord"]
        except:
            pass
    return DwG

def Compare():
    NoChanges = True
    for p in LoadProfiles():
        OldData = LoadProfileData(p)
        NewData = ParseGames(p)
        TotalTime = 0
        for game in NewData:
            try:
                HourDiff = float(NewData[game])-float(OldData[game])
                
                TotalTime+= float(NewData[game])
                if float(HourDiff)>0.0:
                    print(colorama.Fore.CYAN+game+"    +"+str(round(HourDiff,2)))
                    NoChanges = False
            except:
                pass
        if NoChanges:
            print(colorama.Fore.CYAN+"Nothing New")
        print(colorama.Fore.YELLOW+"Total Time Played: "+str(round(TotalTime,2) ))
        SaveData(p,NewData)
Compare()
print(colorama.Fore.RED+"====================")
p = input_colorama(colorama.Fore.YELLOW,"Profile ID: ")
DwG = ParseGames(p)
SaveData(p,DwG)
