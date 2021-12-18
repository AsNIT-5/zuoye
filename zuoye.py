import time
import urllib3
import requests
import random
import os

# 解决警告
urllib3.disable_warnings()


class ZhiJiao:
    def __init__(self, ):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }

    # 获取cookie
    def getCookie_acw_tc(self):
        url = 'https://zjy2.icve.com.cn/portal/login.html'
        self.session.get(url, verify=False)

        return 1

    # 验证码
    def verfiyCode(self):
        url = "https://zjy2.icve.com.cn/api/common/VerifyCode/index" + "?t=" + str(random.random())

        res = self.session.get(url, verify=False)

        img = res.content
        # 下载到本地
        with open('验证码.png', 'wb') as f:
            f.write(img)
        # 识别验证码
        self.code = input("请打开软件所在目录查看“验证码.png”并输入：")
        # 删除图片
        os.remove('验证码.png')

        return 1

    # 登录
    def login(self, userName, passWord):
        url = 'https://zjy2.icve.com.cn/api/common/login/login'

        data = {
            'userName': userName,
            'userPwd': passWord,
            'verifyCode': self.code
        }
        res = self.session.post(url, data=data, verify=False).json()

        if res['code'] == -16:
            print('⚠️  验证码识别错误！')
            return 0
        elif res['code'] == 1:
            self.token = res['token']
            userName = res['displayName']
            print('{}, 欢迎你！🎉🎉🎉'.format(userName))
            return 1
        else:
            print(res)
            print('❌ 登录异常, 出现未知错误, 请联系管理员！')
            time.sleep(3)
            exit()

    # 获取所学课程Info
    def courseInfo(self):
        url = 'https://zjy2.icve.com.cn/api/student/myHomework/getMyHomeworkList'

        res = self.session.post(url, verify=False)

        if res.text == '':
            return ''
        else:
            # 课程信息
            courseLists = res.json()['list']
            for courseList in courseLists:
                for homework in courseList["homeworkList"]:
                    Title = homework["Title"]
                    homeworkid = homework["homeworkId"]
                    courseOpenId = homework["courseOpenId"]
                    print('{}对应的courseOpenId:【{}】,homeworkId:【{}】'.format(Title, courseOpenId, homeworkid))

    def processingData(self, courseOpenId, homeworkId, studentWorkId):
        url = 'https://security.zjy2.icve.com.cn/api/study/homework/history?courseOpenId={}&homeWorkId={}&studentWorkId={}'.format(
            courseOpenId, homeworkId, studentWorkId)
        # 爬取到的所有数据
        reponse = self.session.get(url).json()
        quest = reponse["questions"]
        for num in quest:
            print("题目：", num["Title"])
            for answer in num["answerList"]:
                if answer["IsAnswer"] == "True":
                    print(f"答案为:{answer['Content']}")


if __name__ == "__main__":
    print("\n")
    print("-" * 42)
    print(">    欢迎使用木异阁职教云刷课（获取答案版）     <")
    print(">    QQ：1504257947                      <")
    print(">    微信：HACKER-54946                   <")
    print('-' * 42, "\n")
    zjy = ZhiJiao()
    print('开始登录...⏳')
    # 课程列表
    courseList = zjy.courseInfo()

    while True:
        # 登录
        user = "2111060123"
        password = "Liu123321"
        if zjy.verfiyCode() and zjy.login(user, password):
            print('登录成功 ✅')
            data = zjy.courseInfo()
            print(data)
            courseOpenId = input("请输入courseOpenId后回车：")
            homeworkId = input("请输入homeworkId后回车：")
            studentWorkId = input("请输入studentWorkId后回车：")
            zjy.processingData(courseOpenId, homeworkId, studentWorkId)
            break
        else:
            print('⚠️  2秒后将重新登录, 请等待...')
            time.sleep(2)
