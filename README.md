# xgj_helper
班级小管家帮助
***
支持获取班级小管家答案、下载作业
# 安装依赖
```
  pip3 install -f requirements.txt
```
# 运行方法
```
  python3 ./main.py
```

# 使用说明
  1. 获取openid：<br>
  通过抓包，找到`getUser`请求表单内`wx-openid`的项，该项的值即为openid

  2. 如果作业类型如图所示：<br>
  ![type-classify](https://raw.githubusercontent.com/SamCui0313/samcui0313.github.io/master/img/type_classify.png)<br>
  ***那么该项作业类型为'分类'作业***

  3. 如果作业类型如图所示：<br>
  ![type-Homework](https://raw.githubusercontent.com/SamCui0313/samcui0313.github.io/master/img/type_Homework.png)<br>
  ***那么该项作业类型为'作业'***

# 注意事项
```
  目前不支持获取在线测试题目答案
```


