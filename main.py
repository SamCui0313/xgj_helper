import getHomework
import re
import sys,io
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt,Confirm
from rich.text import Text
from rich.table import Table

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

gh = getHomework.GetHomework()
console = Console()
gh.initUserInfo()

panel = Panel(Text("输入\"1\"抓取作业\n输入\"2\"抓取答案\n输入\"3\"更改openid\n输入\"q\"退出程序",style="bold yellow",justify="center"),border_style="red",title="helper",subtitle="SamCui")
workNum = 0
pageNum = 0
chooseNumber = "g"

while not workNum == "q":
    console.print(panel, justify="center")
    workNum = Prompt.ask("请输入: ",choices=["1","2","3","q"])
    if workNum == "1":
        while not chooseNumber.isdigit():        
            getParent_r = gh.getPage(pageNum)
            table = Table()
            table.add_column("[blue]序号", justify="right", width=12)
            table.add_column("[blue]标题", width=40)
            table.add_column("[blue]发布教师名称", width=13)
            for i in range(pageNum*10, len(getParent_r['data'])+pageNum*10):
                text = re.sub("\n", "", getParent_r['data'][i%10]['title'])
                teacherName = getParent_r['data'][i%10]['creator_wx_name']
                gh._id.append(getParent_r['data'][i%10]['_id'])
                table.add_row(
                    str(i + 1),
                    text,
                    teacherName
                )
            console = Console()
            console.print(table,justify="center")
            if pageNum < 1:
                chooseNumber = Prompt.ask("请输入需要抓取的作业编号[blue](输入n翻下一页): ")
            else:
                chooseNumber = Prompt.ask("请输入需要抓取的作业编号[blue](输入n翻下一页)[yellow](输入u翻上一页): ")
            if chooseNumber == "n":
                pageNum+=1
            if chooseNumber == "u":
                pageNum-=1
        chooseNumber = int(chooseNumber)
        console.print("输入\"1\"下载'作业'类型的图片\n输入\"2\"下载分类的图片")
        type = Prompt.ask("请输入: ",choices=['1','2'])
        gh.getHomeworkURL(int(type),chooseNumber)
        isDownloading = Confirm.ask("本作业共有" + str(gh.feedback_number) + "人提交,是否开始下载？")
        if isDownloading:
            gh.downloadHomework()
            console.print("下载成功!!!")
            chooseNumber = "g"
            gh = getHomework.GetHomework()
        else:
            chooseNumber="g"
            gh = getHomework.GetHomework()
            continue
    if workNum == "2":
        while not chooseNumber.isdigit():
            getParent_r = gh.getPage(pageNum)
            table = Table()
            table.add_column("[blue]序号", justify="right", width=12)
            table.add_column("[blue]标题", width=40)
            table.add_column("[blue]发布教师名称", width=13)
            for i in range(pageNum*10, len(getParent_r['data'])+pageNum*10):
                text = re.sub("\n", "", getParent_r['data'][i%10]['title'])
                teacherName = getParent_r['data'][i%10]['creator_wx_name']
                gh._id.append(getParent_r['data'][i%10]['_id'])
                table.add_row(
                    str(i + 1),
                    text,
                    teacherName
                )
            console = Console()
            console.print(table,justify="center")
            if pageNum<1:
                chooseNumber = Prompt.ask("请输入需要抓取的答案编号[blue](输入n翻下一页)：")
            else:
                chooseNumber = Prompt.ask("请输入需要抓取的答案编号[blue](输入n翻下一页)[yellow](输入u翻上一页): ")
            if chooseNumber == "n":
                pageNum+=1
            if chooseNumber == "u":
                pageNum-=1
        chooseNumber = int(chooseNumber)
        console.print("输入\"1\"获取'作业'类型的答案")
        type = Prompt.ask("请输入: ", choices=['1'])
        if type == "1":
            answers = gh.getExamAnswer(int(type),chooseNumber)
            answer = ""
            leaveNum = len(answers)
            i=1
            c=0
            while i <= leaveNum:
                if answers[c] == 'A' or answers[c] == 'B' or answers[c] == 'C' or answers[c] == 'D':
                    if i%5 == 0:
                        answer=answer+answers[c]+' '
                        c+=1
                        i+=1
                        continue
                else:
                    answer=answer+' '+answers[c]+' ' if not answer[len(answer)-1] == ' ' else answer+answers[c]+' '
                    c+=1
                    leaveNum -= i
                    i=1
                    continue
                answer=answer+answers[c]
                c+=1
                i+=1
            print()
            print(u"答案为：%s" % answer)
            chooseNumber="g"
input("按下回车退出程序")
