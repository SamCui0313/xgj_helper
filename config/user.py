import os, configparser

configPath = os.getcwd() + "/config/config.ini"
conf = configparser.ConfigParser()
if not os.path.exists(os.getcwd() + "/config/config.ini"):
    conf.add_section("User")
    conf.set("User","wx_openid","")
    conf.set("User","member_id","")
    conf.set("User","cid","")
    conf.write(open(configPath,"w+"))
def setOpenID(openID):
    conf.set("User", "wx_openid", openID)
    conf.write(open(configPath, 'w+'))

def setMemberID(memberID):
    conf.set("User", "member_id", memberID)
    conf.write(open(configPath, 'w+'))

def setCid(cid):
    conf.set("User","cid",cid)
    conf.write(open(configPath,"w+"))

def getOpenID():
    conf.read(configPath)
    id = conf.get("User", "wx_openid")
    return id


def getMemberID():
    conf.read(configPath)
    idd = conf.get("User", "member_id")
    return idd

def getCid():
    conf.read(configPath)
    iddd=conf.get("User","cid")
    return iddd
def clearConfig():
    conf.set("User","wx_openid","")
    conf.set("User","wx_openid","")
    conf.write(open(configPath,"w+"))

