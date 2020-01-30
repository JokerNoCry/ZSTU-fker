from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time,os
import sendmail

USERNAME = "************"  # 你的学号
PASSWORD = "************"    # 你的密码
NAME = "your name"   
MAIL_ADDR = "root@qfrost.com"  # 你的邮箱
KC_LIST = ["世界电子竞技", "桥牌"]  # 你要抢的课的列表

task = [    # username, password, name, mail_addr, kc_list
    (USERNAME, PASSWORD, NAME, MAIL_ADDR, KC_LIST),   # 依照此格式再往下写可以实现多任务
]

LOGIN_URL = "http://10.11.247.52/jwglxt/xtgl/login_slogin.html?language=zh_CN"

class QkSuccess(Exception):   #继承自基类Exception
    def __str__(self):
        return "抢课成功"

class example:
    def __init__(self, username, password, name, mail_addr, kc_list):
        self.username = username
        self.password = password
        self.name = name
        self.kc_list = kc_list
        self.mail = mail_addr
        self.browser = webdriver.Firefox()

    def login(self):
        self.browser.get(LOGIN_URL)
        username_input = self.browser.find_element_by_id("yhm")    
        password_input = self.browser.find_element_by_id("mm")     
        login_button = self.browser.find_element_by_id("dl")       

        username_input.click()
        username_input.send_keys(self.username)
        password_input.click()
        password_input.send_keys(self.password)
        time.sleep(0.5)
        login_button.click()

    def qk(self, panel, kcmc):
        global task

        panel.click()
        time.sleep(0.3)
        xk_button = panel.find_element_by_xpath('.//td[@class="an"]/button[contains(text(), "选课")]')
        xk_button.click()
        time.sleep(0.2)
        result = panel.find_element_by_xpath('.//h3').text[-2:]

        with open(self.name + ".txt",'a+') as fp:
            fp.write(str(kcmc) + str(result) + "\n")
            if "已选" in result:
                print("抢课成功:",kcmc)
                print("抢课成功:",kcmc,file=fp)
                shili.sendmail(kcmc)
                if len(task) == 1:
                    exit(0)
                else:
                    del task[0]
                    raise QkSuccess()

    def xk(self):
        # search_button = self.browser.find_element_by_name("query")
        # search_button.click()
        tsxxk_button = self.browser.find_element_by_link_text("通识选修课")
        tsxxk_button.click()
        time.sleep(0.9)
        more_button = self.browser.find_element_by_link_text("点此查看更多")
        try:
            while True:
                more_button.click()
        except Exception as e:
            print(e)
            pass

        get_list = self.browser.find_elements_by_class_name("panel-info")
        print("匹配到 %d 个课程，开始检索" % len(get_list))
        for item in get_list:
            # print(item.text)
            for kcmc in self.kc_list:
                if kcmc in item.text:
                    print("开始抢", item.text)
                    self.qk(item, kcmc)
        
    def init_xk(self):
        jmp_xk_button = self.browser.find_element_by_link_text("选课")
        jmp_xk_button.click()
        time.sleep(0.5)
        jmp_zzxk_button = self.browser.find_element_by_link_text("自主选课")
        jmp_zzxk_button.click() 
        time.sleep(1)
        print(self.browser.window_handles)
        self.browser.switch_to.window(self.browser.window_handles[-1])

        set_yl_button = self.browser.find_element_by_link_text("有")
        set_yl_button.click()

    def sendmail(self, kcmc):       
        receivers = [self.mail]
        subject = '抢课成功通知' 
        content = "To " + self.name + "\n抢课成功： " + kcmc  
        sender_name = self.name 
        receivers_name = [self.mail]   

        mail = sendmail.Mail(self.mail, receivers)
        mail.send(subject, content, sender_name, receivers_name)




if __name__ == "__main__":

    while True:
        if len(task[0]) != 5:
            print("Task Error!")
            print(task[0])
            del task[0]
            continue

        username = task[0][0]
        password = task[0][1]
        name = task[0][2]
        mail_addr = task[0][3]
        kc_list = task[0][4]
        try:
            shili = example(username, password, name, mail_addr, kc_list)
            shili.login()
            time.sleep(1)
            shili.init_xk()
            while True:
                shili.xk()
                time.sleep(1)
        except Exception as e:
            print(e)
            shili.browser.quit()
            del shili
            try:
                with open(name + ".txt",'a+') as fp:
                    fp.write( str(time.asctime( time.localtime(time.time()) )) + str(e) + '\n')
            except Exception as ex:
                print("文件无法打开！")
                print(ex)



















# 注意事项：
# 1. 需先退课，才能抢课，因此有一定的风险，所以建议提供多几个想上的课，以提高成功率
# 2. 请确认所抢的课没有课程冲突
# 3. 抢不到不收费
# 4. 不接换课单

# 请提供以下信息：
# 姓名
# 账号
# 密码
# 所要抢的课
