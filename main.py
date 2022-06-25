import getHomework
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt,Confirm
from rich.text import Text

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
            if pageNum < 1:
                gh.getPage(pageNum)
                chooseNumber = Prompt.ask("请输入需要抓取的作业编号[blue](输入n翻下一页): ")
            else:
                gh.getPage(pageNum)
                chooseNumber = Prompt.ask("请输入需要抓取的作业编号[blue](输入n翻下一页)[yellow](输入u翻上一页): ")
            if chooseNumber == "n":
                pageNum+=1
            if chooseNumber == "u":
                pageNum-=1
        chooseNumber = int(chooseNumber)
        console.print("输入\"1\"下载'作业'类型的图片\n输入\"2\"下载分类的图片")
        type = Prompt.ask("请输入: ",choices=['1','2','3'])
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
            if pageNum<1:
                gh.getPage(pageNum)
                chooseNumber = Prompt.ask("请输入需要抓取的答案编号[blue](输入n翻下一页)：")
            else:
                gh.getPage(pageNum)
                chooseNumber = Prompt.ask("请输入需要抓取的作业编号[blue](输入n翻下一页)[yellow](输入u翻上一页): ")
            if chooseNumber == "n":
                pageNum+=1
            if chooseNumber == "u":
                pageNum-=1
        chooseNumber = int(chooseNumber)
        console.print("输入\"1\"获取'作业'类型的答案\n输入\"2\"获取考试类型的答案")
        type = Prompt.ask("请输入: ", choices=['1', '2'])
        if type == "1":
            answers = gh.getExamAnswer(int(type),chooseNumber)
            answer = ""
            for i in range(1,len(answers)+1):
                if i%5 == 0:
                    answer=answer+answers[i-1]+' '
                    continue
                answer=answer+answers[i-1]
            print()
            print("答案为：%s" % answer)
            chooseNumber="g"
        elif type == 2:
            pass
input("按下回车退出程序")
