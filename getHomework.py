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
        table = Table()
        table.add_column("[blue]序号", justify="right", width=12)
        table.add_column("[blue]标题", width=40)
        table.add_column("[blue]发布教师名称", width=13)
        for i in range(page*10, len(getParent_r['data'])+page*10):
            text = re.sub("\n", "", getParent_r['data'][i%10]['title'])
            teacherName = getParent_r['data'][i%10]['creator_wx_name']
            self._id.append(getParent_r['data'][i%10]['_id'])
            table.add_row(
                str(i + 1),
                text,
                teacherName
            )
        console = Console()
        console.print(table,justify="center")

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

        for i in first_r['data']['notify']['accepts']:
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
                "cid": "60f01d613d2f2b3a58111c56",
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
                    self.feedback_photos_url.append(r['data']['accepts'][0]['feedback_photo'])
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
            # 查找
            for i in r["data"]["datika"]["subjects"]:
                for j in i["detailArrays"]:
                    if j["rightval"] == "y":
                        answer.append(chr(c))
                        c = 65
                        break
                    else:
                        c += 1
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
                image_url = "https://img.banjixiaoguanjia.com/" + j
                image_r = requests.get(image_url)
                with open(os.getcwd() + "/getHomework/" + self.names[c] + "/" + str(igc) + j[j.find("."):], 'wb') as f:
                    f.write(image_r.content)
                igc += 1
            c += 1
            igc = 1
