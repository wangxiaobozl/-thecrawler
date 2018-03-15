import os
import time
import datetime
import sys
from selenium import webdriver
import pymysql.cursors
import proxy
import logging


#代理页面
if __name__ == '__main__':
    url = 'http://www.xicidaili.com/nn/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }


#翻页计数
pageindex_count=0
#代理列表
#profile_list=('110.73.7.61:8123','115.221.125.156:43845','120.92.88.202:10000','61.135.217.7:0')
profile_list=proxy.get_ip_list(url, headers=headers)
#print(len(profile_list*3))
#当前页码
pageindex=1
#总页码
pageNum=273

#爬虫方法
def pqgc(ip_temp,ym):
    print(ip_temp)
    axb=ym
    # 设置代理服务器
    profile = webdriver.FirefoxProfile()
    profile.set_preference('network.proxy.type', 1)
    profile.set_preference('network.proxy.http', ip_temp[0:ip_temp.index(":")])
    profile.set_preference('network.proxy.http_port', 0)  # int(ip_temp[ip_temp.index(":")+1:len(ip_temp)])
    profile.update_preferences()

    # logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    # START_DATETIME = datetime.datetime.now()
    # logging.debug('start at %s', START_DATETIME)
    # 打开火狐浏览器 需要V47版本以上的
    driver = webdriver.Firefox(firefox_profile=profile)  # 打开火狐浏览器
    # driver = webdriver.Firefox()  # 打开火狐浏览器
    logging.debug('type(driver) : %s', type(driver))
    url = "http://app1.sfda.gov.cn/datasearch/face3/base.jsp?tableId=36&tableName=TABLE36&title=%BD%F8%BF%DA%D2%A9%C6%B7&bcId=124356651564146415214424405468"  # 这里打开我的博客网站
    driver.get(url)  # 设置火狐浏览器打开的网址
    logging.debug('request completed')
    time.sleep(20)
    LIST_WEBELEMENT = driver.find_elements_by_id('content')
    if len(LIST_WEBELEMENT)==0:
        print("超时！！！")
        sys.exit()

    #指定页码
    ym_xpath = "//*[@id='content']/div/table[position()=4]/tbody//input[@value]"
    ym_value = driver.find_elements_by_xpath(ym_xpath)
    ym_value[0].clear()
    ym_value[0].send_keys(axb)

    goint_xpath = "//*[@id='content']/div/table[position()=4]/tbody//input[last()]"  # [@src=\"images/dataanniu_07.gif\"]
    goint_value = driver.find_elements_by_xpath(goint_xpath)
    now_handle = driver.current_window_handle
    print(len(goint_value))
    goint_value[1].click()

    #  跳转页面后继续 抓取数据
    time.sleep(15)
    for i in range(0, 30):
        xyy_xpath = ""
        yplist_xpath = ""
        if i == 0:
            xyy_xpath = "//*[@id='content']/div/table[position()=4]/tbody//img[@src=\"images/dataanniu_07.gif\"]"
            yplist_xpath = "//*[@id='content']/div/table[position()=2]/tbody/tr[position()>=1 and ((position()-1) mod 2)=0]/td/p/a[@href]"
        else:
            xyy_xpath = "//*[@id='content']/table[position()=4]/tbody//img[@src=\"images/dataanniu_07.gif\"]"
            yplist_xpath = "//*[@id='content']/table[position()=2]/tbody/tr[position()>=1 and ((position()-1) mod 2)=0]/td/p/a[@href]"
        # 使用xpath进行多路径或多元素定位,用法看官网http://selenium-python.readthedocs.io/locating-elements.html
        elem_dh = driver.find_elements_by_xpath(xyy_xpath)
        # print("我是刚获取的翻页按钮的路径数组:", elem_dh)
        # print("下一页按钮元素：", elem_dh[0])
        # time.sleep(1)
        # 获取当前窗口句柄
        now_handle = driver.current_window_handle  # 获取当前窗口句柄
        # print("我是当前窗口的句柄:", now_handle)  # 打印窗口句柄 是一串数字
        # time.sleep(1)
        # print(" = " * 10 + "第" + str(i+1) + "页" + " = " * 10)
        # 获取页面药品列表
        yplist = driver.find_elements_by_xpath(yplist_xpath)
        for yp_item in yplist:
            yp_name = yp_item.text
            # print(yp_name)
            yp_id = ""
            if i == 0:
                yp_id = yp_item.get_attribute("href").replace(
                    "javascript:commitForECMA(callbackC,'content.jsp?tableId=36&tableName=TABLE36&tableView=%E8%BF%9B%E5%8F%A3%E8%8D%AF%E5%93%81&Id=",
                    '').replace("\",null)", "")
            else:
                yp_id = yp_item.get_attribute("href").replace(
                    "javascript:commitForECMA(callbackC,'content.jsp?tableId=36&tableName=TABLE36&tableView=%E8%BF%9B%E5%8F%A3%E8%8D%AF%E5%93%81&Id=",
                    '').replace("',null)", "")
            print(yp_name + yp_id)
            # file.write(yp_name + "^" + yp_id + '\n')
            sql = "insert into yplist_jk (nameinfo,number) VALUE ('" + yp_name + "','" + yp_id + "')"
            cursor.execute(sql)
            connection.commit()

        # 循环获取界面
        for elem in elem_dh:
            # print("我是翻页按钮上的文本信息:", elem.text)  # 获取元素的文本值
            # print("我是翻页按钮的地址", elem.get_attribute('onclick'))  # 获取元素的href属性值
            if i < pageNum:
                elem.click()  # 点击进入新的界面 _blank弹出
                axb +=1
            print("刚翻页完成了！"+str(axb))
            time.sleep(5)
        if i==29:
            driver.quit()
    return  axb



config = {
          'host':'192.168.1.102',
          'port':3318,
          'user':'wangxb',
          'passwd':'wxb085',
          'db':'test',
          'charset':'utf8',
          'cursorclass':pymysql.cursors.DictCursor,
          }
connection=pymysql.connect(**config)
cursor = connection.cursor()

# try:
#     # 循环替换代理
#     for item in profile_list:
#         print(item)
#         pageindex = pqgc(item, pageindex)
# except :
#     print ("error")
# finally:
#     pqgc(proxy.get_random_ip(profile_list).get("http").replace("http://",""), pageindex)

for i in range(pageindex,pageNum):
    pageindex=pqgc(proxy.get_random_ip(profile_list).get("http").replace("http://", ""), pageindex)











