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
    time.sleep(sleeptime)
    flag = 0
    try:
        browser.find_element_by_id("p1_ChengNuo-inputEl-icon").click()##承诺
        browser.find_element_by_id("fineui_6-inputEl-icon").click()##宝山校区
        #time.sleep(sleeptime)
        browser.find_element_by_id("p1_TiWen-inputEl").send_keys("36.5")##体
        browser.find_element_by_id("p1_XiangXDZ-inputEl").send_keys("上海大学宝山校区")##体
        browser.find_element_by_id("p1_ddlXian-inputEl").click()
        time.sleep(sleeptime)
        browser.find_element_by_xpath("/html/body/ul[3]/li[10]").click()
        #time.sleep(1)
        browser.find_element_by_id("fineui_11-inputEl-icon").click()##否中高1
        browser.find_element_by_id("fineui_13-inputEl-icon").click()##否中高2
        browser.find_element_by_id("fineui_15-inputEl-icon").click()##否隔离
        browser.find_element_by_id("fineui_21-inputEl-icon").click()##
        browser.find_element_by_id("fineui_23-inputEl-icon").click()##
        browser.find_element_by_id("fineui_26-inputEl-icon").click()##
        browser.find_element_by_id("fineui_27-inputEl-icon").click()##
    except:
        flag = 1
        print("报过了")
        
    if flag == 0:
        browser.find_elements_by_css_selector(
            ".f-btn.f-noselect.f-state-default.f-corner-all"
            ".f-btn-normal.f-btn-icon-no.f-cmp.f-widget"
            ".f-toolbar-item")[0].click()
        time.sleep(sleeptime)
        flagError = 0
        try:
            browser.find_elements_by_css_selector(".f-btn.f-noselect.f-state-default.f-corner-all"".f-btn-normal.f-btn-icon-no.f-cmp.f-widget"".f-toolbar-item")[2].click()
        except (Exception, BaseException) as e:
            flagError = 1
        #time.sleep(sleeptime)
        print("报好了(可能之前报过)")
# https://selfreport.shu.edu.cn/XueSFX/HalfdayReport_View.aspx?day=2020-11-26&t=1

def get_info(usr,pwd,data_list,sleeptime):
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
    # time.sleep(1)

    browser.find_element_by_id("username").send_keys(usr)
    browser.find_element_by_id("password").send_keys(pwd)
    # time.sleep(1)
    browser.find_element_by_id("submit").click()

    time.sleep(1)
    for i in data_list:
        urla = "https://selfreport.shu.edu.cn/XueSFX/HalfdayReport.aspx?day="
        urlb = i
        urlc = "&t=1"
        urld = "&t=2"
        
        morning = urla+urlb+urlc
        afternoon = urla+urlb+urld

        print(i+'morning')
        visit(browser,morning,sleeptime)
        time.sleep(1)

        print(i+'afternoon')
        visit(browser,afternoon,sleeptime)
        time.sleep(sleeptime)
    browser.quit()


if __name__ == '__main__':
    
    reader1 = csv.reader(open('load.csv','r'))
    reader = list(reader1)
    sleeptime = int(reader[1][0])
    start = reader[0][0]
    end = reader[0][1]
    usr = []
    pwd = []
    for row in reader[2:]:
        usr.append(row[0])
        pwd.append(row[1])
    print(usr)
    print(pwd)
    dateend = datetime.datetime.strptime(end,'%Y/%m/%d')
    datestart = datetime.datetime.strptime(start,'%Y/%m/%d')
    # datestart = dateend
    # datestart-= datetime.timedelta(days=1)
    # datestart=datetime.datetime.strptime(start,'%Y-%m-%d')
    data_list = list()
    while datestart<=dateend:
        data_list.append(datestart.strftime('%Y-%m-%d')) 
        datestart+=datetime.timedelta(days=1)
    print(data_list)
    
    for i in range(0,len(usr)):
        get_info(usr[i], pwd[i], data_list,sleeptime)
        print(usr[i])





 
