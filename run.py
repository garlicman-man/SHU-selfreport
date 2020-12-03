from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
import traceback
import datetime
import csv

def hover(self,by,value):
    element = self.findElement(by,value)
    ActionChains(self.driver).move_to_element(element).perform()

def visit(browser,url,sleeptime):
    browser.get(url)
    flag = 0
    try:
        browser.find_element_by_id("p1_ChengNuo-inputEl-icon").click()##承诺
        browser.find_element_by_id("fineui_6-inputEl-icon").click()##宝山校区
        #time.sleep(1)
        browser.find_element_by_id("p1_TiWen-inputEl").send_keys("36.5")##体
        browser.find_element_by_id("p1_XiangXDZ-inputEl").send_keys("上海大学宝山校区")##体
        browser.find_element_by_id("p1_ddlXian-inputEl").click()#下拉框区县
        time.sleep(sleeptime)
        browser.find_element_by_xpath("/html/body/ul[3]/li[10]").click()#选择宝山区
        #time.sleep(1)
        browser.find_element_by_id("fineui_11-inputEl-icon").click()##否中高1
        browser.find_element_by_id("fineui_13-inputEl-icon").click()##否中高2
        browser.find_element_by_id("fineui_15-inputEl-icon").click()##否隔离
        browser.find_element_by_id("fineui_21-inputEl-icon").click()##是非框几个
        browser.find_element_by_id("fineui_23-inputEl-icon").click()##
        browser.find_element_by_id("fineui_26-inputEl-icon").click()##
        browser.find_element_by_id("fineui_27-inputEl-icon").click()##
    except:
        flag = 1
        print("报过了")
        
    if flag == 0:##按下确认按钮
        browser.find_elements_by_css_selector(
            ".f-btn.f-noselect.f-state-default.f-corner-all"
            ".f-btn-normal.f-btn-icon-no.f-cmp.f-widget"
            ".f-toolbar-item")[0].click()
        time.sleep(sleeptime)
        flagError = 0
        try:##按下确认填报按钮
            browser.find_elements_by_css_selector(".f-btn.f-noselect.f-state-default.f-corner-all"".f-btn-normal.f-btn-icon-no.f-cmp.f-widget"".f-toolbar-item")[2].click()
        except (Exception, BaseException) as e:
            flagError = 1
        time.sleep(sleeptime)##这上边可能会有已经报过的，不管他，直接换网址冲
        print("报好了")


def get_info(usr,pwd,data_list,MorA,sleeptime):
    #browser = webdriver.Chrome('C:\ProgramData\Anaconda3\chromedriver.exe')
    browser = webdriver.Chrome('chromedriver.exe')
    #browser = webdriver.Firefox(executable_path='G:\\forSubmit\\firefox.exe')
    browser.set_window_size(480,1080)
    #browser.maximize_window()
    #url = "https://selfreport.shu.edu.cn/Default.aspx"
    url = "https://selfreport.shu.edu.cn/XueSFX/HalfdayReport.aspx?day=2020-11-26&t=1"
    #url = "https://selfreport.shu.edu.cn/"
    #url = "https://www.zhihu.com/"
    browser.get(url)
    browser.find_element_by_id("username").send_keys(usr)
    browser.find_element_by_id("password").send_keys(pwd)
    browser.find_element_by_id("submit").click()
    time.sleep(sleeptime)
    # browser.find_element_by_class_name("layui-layer-btn0").click()
    # browser.find_element_by_class_name("f-datalist-item-inner").click()
    # browser.find_element_by_id("p1_ctl00_btnReturn").click()
    # browser.find_element_by_id("lnkReportHistory").click()
    # browser.find_elements_by_class_name("f-datalist-item-inner")[1].click()
    for i in data_list:
        urla = "https://selfreport.shu.edu.cn/XueSFX/HalfdayReport.aspx?day="
        urlb = i
        urlc = "&t=1"
        urld = "&t=2"##拼接url
        
        morning = urla+urlb+urlc
        afternoon = urla+urlb+urld
        if MorA == 1:
            print(i+'morning')
            visit(browser,morning,sleeptime)
            time.sleep(sleeptime)
        if MorA == 2:
            print(i+'afternoon')
            visit(browser,afternoon,sleeptime)
            time.sleep(sleeptime)
    browser.quit()


if __name__ == '__main__':

    reader1 = csv.reader(open('load.csv','r'))
    reader = list(reader1)
    # start = reader[0][0]
    # end = reader[0][1]
    sleeptime = int(reader[1][0])
    usr = []
    pwd = []
    for row in reader[2:]:
        usr.append(row[0])
        pwd.append(row[1])


    while(True):
        sched_time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        today = datetime.datetime.now().strftime('%Y-%m-%d')##今日日期

        hour = datetime.datetime.now().strftime('%H')##当前小时
        sched_time2 = datetime.datetime.strptime(sched_time,'%Y-%m-%d-%H-%M-%S')

        finaldelta = 0
        a1 = "-07-02-01"#目标时间早报
        a2 = today + a1#今日的早报时间
        test2=datetime.datetime.strptime(a2, "%Y-%m-%d-%H-%M-%S")#转格式为日期型
        diff=test2-sched_time2#计算当前时间与早报时间差值
        # print(diff.total_seconds())
        delta = diff.total_seconds()

        a3 = "-20-02-01"#晚报时间 同上
        a4 = today + a3
        test3=datetime.datetime.strptime(a4, "%Y-%m-%d-%H-%M-%S")
        diff=test3-sched_time2
        # print(diff.total_seconds())
        deltb = diff.total_seconds()##与晚报时间差额
        hour = int(hour)
        print(hour)
        # print(delta)
        # print(deltb)
        if hour >= 0 and hour <=8:
            finaldelta = delta
        elif hour >8 and hour <= 20:
            finaldelta = deltb
        elif hour>20 and hour <=24:
            finaldelta = delta + 86400
        # if delta>0 and deltb>0:##如果当前时间与指定早报时间或晚报时间差额小于3200 直接选择小的差额 可能为负
        #     finaldelta = min(delta,deltb)
        # elif delta<=-3200 and deltb>-3200:#如果一个为负小于-3200 取另一个
        #     finaldelta = deltb
        # elif deltb<=-3200 and delta>-3200:
        #     finaldelta = delta
        # else:
        #     finaldelta = min(delta,deltb)
        #     finaldelta += 86400
        # print(finaldelta)
        #print("cha")
        print(finaldelta)
        if finaldelta > 60:#如果仍然差了一分钟以上，开始沉睡
            print("开始长时间休息,",'休息',finaldelta,'秒')
            while finaldelta != 0:
                if finaldelta % 10 == 0:
                    print("剩余:",finaldelta,"秒")
                finaldelta = finaldelta - 1
                time.sleep(1)
        else:
            print("时间临近")
            #time.sleep(10)
            print("开始运行")
            hour = datetime.datetime.now().strftime('%H')##当前小时
            loopflag = 0
            if hour == '07':##确定我现在要早报还是晚报
                loopflag = 1
            if hour == '20':  
                loopflag = 2
            if loopflag != 0:
                print("success")
                print(loopflag)
                    # end = '2020-11-01'
                end = datetime.datetime.now().strftime('%Y-%m-%d')
                dateend = datetime.datetime.strptime(end,'%Y-%m-%d')
                datestart = dateend
                #datestart-= datetime.timedelta(days=1)

                # datestart=datetime.datetime.strptime(start,'%Y-%m-%d')
                data_list = list()##将要打的加入list
                while datestart<=dateend:
                    data_list.append(datestart.strftime('%Y-%m-%d')) 
                    datestart+=datetime.timedelta(days=1)
                print(data_list)
                
                for i in range(0,len(usr)):
                    get_info(usr[i], pwd[i], data_list,loopflag,sleeptime)##loopflag为区分早上和下午 为1与2
                    print(usr[i])
            print("开始待机3600s 超过当前小时后重新计算时间差")
            finaldelta = 3600
            while finaldelta != 0:
                if finaldelta % 10 == 0:
                    print("剩余:",finaldelta,"秒")
                finaldelta = finaldelta - 1
                time.sleep(1)