import shutil, json, os, requests, time, urllib3, re
from rich.console import Console
from rich.table import Column, Table
from rich.progress import track
import config.user as user

urllib3.disable_warnings()


class GetHomework:
    def __init__(self):
        self._id = []
        self.openid = []
        self.memberid = []
        self.names = []
        self.feedback_photos_url = []
        self.feedback_number = 0
    def initUserInfo(self):
        if user.getOpenID() == "":
            self.str = input("Input your wx_openid: ")
            user.setOpenID(self.str)
        url = "https://a.welife001.com/getUser"
        self.first_headers = {
            "Host": "a.welife001.com",
            "Connection": "keep-alive",
            "Content-Length": "41",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
            "content-type": "application/json",
            "imprint": user.getOpenID(),
            "Referer": "https://servicewechat.com/wx23d8d7ea22039466/1419/page-frame.html",
            "Accept-Encoding": "gzip, deflate, br"}

        first_data = {"openid": user.getOpenID()}

        first_r = json.loads(requests.post(url=url, headers=self.first_headers, data=json.dumps(first_data)).text)
        user.setMemberID(first_r['currentUser']['child_class_list'][0]['member_id'])
        user.setCid(first_r['currentUser']['child_class_list'][0]['cid'])

    def getPage(self, page):
        self._id.clear()
        url = "https://a.welife001.com/info/getParent?type=-1&members=60f01e1aa9b477377b25d732&page=" + str(
            page) + "&size=10&date=-1&hasMore=true"
        self.headers = {
            "Host": "a.welife001.com",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
            "content-type": "application/json",
            "imprint": user.getOpenID(),
            "Referer": "https://servicewechat.com/wx23d8d7ea22039466/1419/page-frame.html",
            "Accept-Encoding": "gzip, deflate, br"
        }
        getParent_r = json.loads(requests.get(url=url, headers=self.headers).text)
        return getParent_r
        
    def getHomeworkURL(self, type, chooseNumber):
        chooseID = self._id[chooseNumber%10 - 1]
        url = "https://a.welife001.com/applet/notify/checkNew2Parent"
        first_headers = {"host": "a.welife001.com",
                         "accept": "*/*",
                         "content-type": "application/json",
                         "referer": "https://servicewechat.com/wx23d8d7ea22039466/1405/page-frame.html",
                         "imprint": user.getOpenID(),
                         "content-length": "223",
                         "accept-language": "zh-cn",
                         "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E217 MicroMessenger/6.8.0(0x16080000) NetType/WIFI Language/en Branch/Br_trunk MiniProgramEnv/Mac",
                         "accept-encoding": "gzip, deflate, br"}

        self.ts = int(round(time.time() * 1000))

        first_data = {
            "extra": 1,
            "cid": user.getCid(),
            "cls_ts": self.ts,
            "daka_day": "",
            "member_id": user.getMemberID(),
            "_id": chooseID,
            "page": 0,
            "size": 10,
            "trial": 0
        }

        first_r = json.loads(requests.post(url=url, headers=first_headers, data=json.dumps(first_data)).text)

        for i in first_r['data']['feedbacks']:
            self.openid.append(i['wx_openid'])
            self.memberid.append(i['member_id'])

        for i in range(0, len(self.openid)):
            headers = {"host": "a.welife001.com",
                        "accept": "*/*",
                        "content-type": "application/json",
                        "referer": "https://servicewechat.com/wx23d8d7ea22039466/1405/page-frame.html",
                        "imprint": self.openid[i],
                        "content-length": "223",
                        "accept-language": "zh-cn",
                        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E217 MicroMessenger/6.8.0(0x16080000) NetType/WIFI Language/en Branch/Br_trunk MiniProgramEnv/Mac",
                        "accept-encoding": "gzip, deflate, br"}

            ts = int(round(time.time() * 1000))

            data = {
                "extra": 1,
                "cid": user.getCid(),
                "cls_ts": ts,
                "daka_day": "",
                "member_id": self.memberid[i],
                "_id": chooseID,
                "page": 0,
                "size": 10,
                "trial": 0}
            if type == 1:
                try:
                    r = json.loads(requests.post(url=url, headers=headers, data=json.dumps(data)).text)
                    self.feedback_photos_url.append(r['data']['accepts'][0]['feedback_photo'] + r['data']['accepts'][0]['feedback_videos'] + r['data']['accepts'][0]['feedback_records'] + r['data']['accepts'][0]['feedback_files'])
                    name = r['data']['membersMap'][self.memberid[i]]['name']
                    self.names.append(name)
                except:
                    # print("error")
                    pass
                self.feedback_number = len(self.feedback_photos_url)
            elif type == 2:
                userFeedbackUrl = []
                try:
                    r = json.loads(requests.post(url=url,headers=headers,data=json.dumps(data)).text)
                    for j in r['data']['accepts'][0]['answer']['subject']:
                        for k in j['input']['file']:
                            if len(k['id']) == 0:
                                pass
                            else:
                                userFeedbackUrl.append(k['id'])
                    name = r['data']['membersMap'][self.memberid[i]]['name']
                    self.names.append(name)
                    self.feedback_photos_url.append(userFeedbackUrl)
                except:
                    pass
                userFeedbackUrl=[]
                self.feedback_number = len(self.feedback_photos_url)
            elif type == 3:
                userFeedbackUrl=[]
                try:
                    r = json.loads(requests.post(url=url,headers=headers,data=json.dumps(data)).text)
                    for j in r['data']['accepts'][0]['attach']['subjects']:
                        for k in j['answers']:
                            if k.find(".") >= 0:
                                userFeedbackUrl.append(k)
                    self.names.append(r['data']['membersMap'][self.memberid[i]]['name'])
                    self.feedback_photos_url.append(userFeedbackUrl)
                except:
                    pass
                userFeedbackUrl=[]
                self.feedback_number = len(self.feedback_photos_url)
    def getExamAnswer(self,type,chooseNumber):
        if type == 1:
            chooseID = self._id[chooseNumber%10 - 1]
            url = "https://a.welife001.com/applet/notify/checkNew2Parent"
            answer = []

            # 请求头
            headers = {"host": "a.welife001.com",
                       "accept": "*/*",
                       "content-type": "application/json",
                       "referer": "https://servicewechat.com/wx23d8d7ea22039466/1400/page-frame.html",
                       "imprint": user.getOpenID(),
                       "content-length": "175",
                       "if-none-match": "W/\"59e0-/Ml25fzb86GbpZkkIN+IdNfnXT4\"",
                       "accept-language": "zh-cn",
                       "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E217 MicroMessenger/6.8.0(0x16080000) NetType/WIFI Language/en Branch/Br_trunk MiniProgramEnv/Mac",
                       "accept-encoding": "gzip, deflate, br"}

            # 输入_id
            # 表单
            data = {
                "extra": 1,
                "cid": user.getCid(),
                "cls_ts": -1,
                "daka_day": "",
                "member_id": user.getMemberID(),
                "_id": chooseID,
                "page": 0,
                "size": 10,
                "trial": 0
            }
            # 字典转json
            data = json.dumps(data)
            r = requests.post(url=url, headers=headers, data=data).text
            r = json.loads(r)
            # ascii：“A”
            c = 65

            rightVal=[]
            right = ''

            # 查找
            for i in r["data"]['notify']["attach"]["subjects"]:
                for j in i["details"]:
                    if j["right"] == "y":
                        rightVal.append(c)
                        c+=1
                    elif j["right"] == "n":
                        c += 1
                    else:
                        answer.append(j["right"])
                for i in rightVal:
                    right += chr(i)
                answer.append(right)
                right = ''
                rightVal=[]
                c=65
            return answer
        elif type == 2:
            chooseID = self._id[chooseNumber % 10 -1]
            url = "https://a.welife001.com/notify/check2Exam"
            answer = []
            ts = int(round(time.time() * 1000))

            headers = {
                "accept": "*/*",
                "content-type": "application/json",
                "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E217 MicroMessenger/6.8.0(0x16080000) NetType/WIFI Language/en Branch/Br_trunk MiniProgramEnv/Mac",
                "content-length": "161",
                "authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJvcGVuaWQiOiJvV1JrVTBZeEVYM3dZTHREcy1OM002UldycTlJIiwidW5pb25pZCI6Im90Z3pwdno5QTBrQzFJSlVYckdnVjl2bWR1TkUiLCJwbGF0Zm9ybSI6Im1pbmkiLCJleHAiOjE2NzQwMjc5ODY1ODUsImlhdCI6MTY2ODg0Mzk4Nn0.RsQpfMW05kSQ9MFHjmtE9__yzz_QZUDM-XQPlMHTOaE",
                "imprint": user.getOpenID(),
                "accept-language": "zh-CN,zh-Hans;q=0.9",
                "referer": "https://servicewechat.com/wx23d8d7ea22039466/1763/page-frame.html",
                "accept-encoding": "gzip, deflate, br"
            }
            data = {
                "_id": chooseID,
                "cid": user.getCid(),
                "daka_day": "",
                "teacher_cate": "",
                "member_id": user.getMemberID(),
                "cls_ts": ts
            }

            data = json.dumps(data)
            r = requests.post(url=url,headers=headers,data=data).text
            r=json.loads(r)

            c=65
            rightVal=[]
            right = ''

            for i in r["notify"]['exam']["subjects"]:
                for j in i["examsubject"]["detailArrays"]:
                    if j["rightval"] == "y":
                        rightVal.append(c)
                        c+=1
                    elif j["rightval"] == "n":
                        c += 1
                    else:
                        answer.append(j["rightval"])
                for i in rightVal:
                    right += chr(i)
                answer.append(right)
                right = ''
                rightVal=[]
                c=65
            return answer
    def downloadHomework(self):
        checkdir = os.path.exists('getHomework')
        if checkdir:
            cwd = os.getcwd()
            shutil.rmtree(cwd + "/getHomework")
            os.mkdir(cwd + "/" + "getHomework")
            for i in self.names:
                os.mkdir(cwd + "/getHomework/" + i)
        else:
            cwd = os.getcwd()
            os.mkdir(cwd + "/" + "getHomework")
            for i in self.names:
                os.mkdir(cwd + "/getHomework/" + i)

        c = 0
        igc = 1

        for i in track(self.feedback_photos_url,description="Downloading..."):
            for j in i:
                file_type = j[j.find("."):]
                if file_type == ".png" or file_type == ".jpg":
                    homework_url = "https://img.banjixiaoguanjia.com/"+j
                elif file_type == ".mp3":
                    homework_url = "https://record.banjixiaoguanjia.com/"+j
                elif file_type == ".mp4":
                    homework_url = "https://video.banjixiaoguanjia.com/"+j
                else:
                    homework_url = "https://file.banjixiaoguanjia.com/"+j
                homework_r = requests.get(homework_url)
                with open(os.getcwd() + "/getHomework/" + self.names[c] + "/" + str(igc) + file_type , 'wb') as f:
                    f.write(homework_r.content)
                igc += 1
            c += 1
            igc = 1
