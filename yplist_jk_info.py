import os
import time
import datetime
import sys
from selenium import webdriver
import pymysql.cursors
import proxy
import logging
#无浏览器爬取数据
#分组号
input_group=0
bky_list=[]
bky_id=""

#代理页面
if __name__ == '__main__':
    url = 'http://www.xicidaili.com/nn/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
#代理列表
profile_list=proxy.get_ip_list(url, headers=headers)


#数据库配置
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


#递归爬取方法
def getinfo(yp_group):
    connection = pymysql.connect(**config)
    cursor = connection.cursor()
    sql_yplist = "select * from yplist_jk a where a.state is null order by a.id LIMIT 50"
    cursor.execute(sql_yplist)
    connection.commit()
    i = cursor.rowcount
    print(i)
    ip_dl=proxy.get_random_ip(profile_list).get("http").replace("http://", "")
    print(ip_dl)
    # 设置代理服务器
    profile = webdriver.FirefoxProfile()
    profile.set_preference('network.proxy.type', 1)
    profile.set_preference('network.proxy.http', ip_dl[0:ip_dl.index(":")])
    profile.set_preference('network.proxy.http_port', 0)  # int(ip_temp[ip_temp.index(":")+1:len(ip_temp)])
    profile.update_preferences()
    driver = webdriver.Remote("http://172.16.9.152:4446/wd/hub",desired_capabilities=webdriver.DesiredCapabilities.HTMLUNIT, browser_profile=profile)
    #固定地址
    url = "http://app1.sfda.gov.cn/datasearch/face3/content.jsp?tableId=36&tableName=TABLE36&tableView=进口药品&Id="  # 这里打开我的博客网站
    if i>0:
        result = cursor.fetchall()
        for yp in result:
            try:
                print(yp.get("number") + yp.get("nameinfo") + str(yp.get("id")))
                item_info = {}
                driver.get(url + yp.get("number"))  # 设置火狐浏览器打开的网址
                logging.debug('request completed')
                #time.sleep(1)
                LIST_WEBELEMENT = driver.find_elements_by_xpath("//table")
                if len(LIST_WEBELEMENT) == 0:
                    print("超时！！！")
                    driver.quit()
                    getinfo(yp_group)
                    # sys.exit()
                    # driver.quit()
                yp_info = driver.find_elements_by_xpath("//table[1]//tr")
                # print(len(yp_info))
                if len(yp_info) !=36:
                    i -= 1
                    # if  yp.get("number") not in bky_list:
                    #     bky_list.append(yp.get("number"))
                    updatestate(yp.get("number"))
                    continue
                for item in yp_info:
                    if len(item.find_elements_by_xpath("td")) == 1:#首行跳出
                        continue
                    td_list = item.find_elements_by_xpath("td")
                    if len(td_list[0].text) != 0:
                        item_info.setdefault(td_list[0].text, td_list[1].text)
                    # for ii in item_info:
                    #     print(ii,item_info[ii]).
                sql="INSERT into yplist_jk_info (`yp_id`,\
                      `yp_number`,\
                      `注册证号`,\
                      `原注册证号`,\
                      `注册证号备注`,\
                      `分包装批准文号`,\
                      `公司名称（中文）`,\
                      `公司名称（英文）`,\
                      `地址（中文）`,\
                      `地址（英文）`,\
                      `国家/地区（中文）`,\
                      `国家/地区（英文）`,\
                      `产品名称（中文）`,\
                      `产品名称（英文）`,\
                      `商品名（中文）`,\
                      `商品名（英文）`,\
                      `剂型（中文）`,\
                      `规格（中文）`,\
                      `包装规格（中文）`,\
                      `生产厂商（中文）`,\
                      `生产厂商（英文）`,\
                      `厂商地址（中文）`,\
                      `厂商地址（英文）`,\
                      `厂商国家/地区（中文）`,\
                      `厂商国家/地区（英文）`,\
                      `发证日期`,\
                      `有效期截止日`,\
                      `分包装企业名称`,\
                      `分包装企业地址`,\
                      `分包装文号批准日期`,\
                      `分包装文号有效期截止日`,\
                      `产品类别`,\
                      `药品本位码`,\
                      `药品本位码备注`,\
                      `相关数据库查询`,\
                      `注`) values (" + str(yp.get("id")) + ",'" + yp.get("number") + "','"+ item_info.get( "注册证号").replace("'","''") + "','"+ item_info.get( "原注册证号").replace("'","''")+ "','" \
                    +item_info.get( "注册证号备注").replace("'","''")+ "','"  +item_info.get( "分包装批准文号").replace("'","''") + "','" +item_info.get( "公司名称（中文）").replace("'","''") + "','" +item_info.get( "公司名称（英文）").replace("'","''")+ "','"\
                    +item_info.get( "地址（中文）").replace("'","''")+ "','"  +item_info.get( "地址（英文）").replace("'","''")+ "','"  +item_info.get( "国家/地区（中文）").replace("'","''")+ "','"  +item_info.get( "国家/地区（英文）").replace("'","''")+ "','"\
                    +item_info.get( "产品名称（中文）").replace("'","''") + "','" +item_info.get( "产品名称（英文）").replace("'","''")+ "','"  +item_info.get( "商品名（中文）").replace("'","''")+ "','"  +item_info.get( "商品名（英文）").replace("'","''")+ "','"\
                    +item_info.get( "剂型（中文）").replace("'","''") + "','" +item_info.get( "规格（中文）").replace("'","''")+ "','"  +item_info.get( "包装规格（中文）").replace("'","''") + "','" +item_info.get( "生产厂商（中文）").replace("'","''")+ "','"\
                    +item_info.get( "生产厂商（英文）").replace("'","''")+ "','"  +item_info.get( "厂商地址（中文）").replace("'","''") + "','" +item_info.get( "厂商地址（英文）").replace("'","''")+ "','"  +item_info.get( "厂商国家/地区（中文）").replace("'","''")+ "','" \
                    +item_info.get( "厂商国家/地区（英文）").replace("'","''") + "','" +item_info.get( "发证日期").replace("'","''") + "','" +item_info.get( "有效期截止日").replace("'","''") + "','" +item_info.get( "分包装企业名称").replace("'","''")+ "','" \
                    +item_info.get( "分包装企业地址").replace("'","''")+ "','"  +item_info.get( "分包装文号批准日期").replace("'","''")+ "','"  +item_info.get( "分包装文号有效期截止日").replace("'","''")+ "','"  +item_info.get( "产品类别").replace("'","''")+ "','" \
                    +item_info.get("药品本位码").replace("'", "''")+ "','" +item_info.get( "药品本位码备注").replace("'","''") + "','" +item_info.get( "相关数据库查询").replace("'","''").replace("\r","").replace("\n","") + "','" +item_info.get( "注").replace("'","''").replace("\r","").replace("\n","")  +"')"
                cursor.execute(sql)
                connection.commit()
                updatestate(yp.get("number"))
                i -= 1
                if i == 0:
                    driver.quit()
                    print("循环结束！")
                    getinfo(yp_group)
            except:
                print("循环调用出错！")
                continue
            # finally:
            #     connection.close()
    else:
        driver.quit()
#更新状态
def updatestate(number):
    try:
        connection = pymysql.connect(**config)
        cursor = connection.cursor()
        sql="update yplist_jk set state=1 where number ="+number
        cursor.execute(sql)
        connection.commit()
    except:
        print("更新出错！")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

#执行爬取
input_group=input('输入分组:')
getinfo(input_group)
cursor.close()
connection.close()
