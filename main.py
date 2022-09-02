# 启动代理
from browsermobproxy import Server
# 爬虫包
import requests
# 基础包
import time
from selenium import webdriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# 导入处理<select>标签的工具
from selenium.webdriver.support.select import Select
# 导入无头参数需要的包，注意应导入对应浏览器的option包
from selenium.webdriver.edge.options import Options
# 系统操作
import sys
import os
# 多线程
from threading import Thread
# 线程池包
import threading
import threadpool

import time

from mobile_tool import send_notice

url = "https://yqtb.nwpu.edu.cn/wx/ry/jrsb_xs.jsp"


# 重启程序
def restart_program():
    print("网络超时，正在尝试重连……")
    python = sys.executable
    os.execl(python, python, *sys.argv)
    exit()


# 创建超时线程
class TimeThread(Thread):
    def run(self):
        time.sleep(60)
        restart_program()


def auto_fill(stu_dic):
    DELAY_TIME = 1

    userName = stu_dic['userName']
    password = stu_dic['password']
    province = stu_dic['province']
    city = stu_dic['city']
    district = stu_dic['district']

    while True:
        try:
            # 无头参数
            opt = Options()
            opt.add_argument('--headless')

            web = webdriver.Edge(options=opt)
            web.get(url)
            time.sleep(DELAY_TIME)

            # 创建超时线程对象
            overtime = TimeThread()
            overtime.start()

            # 进入填报页面
            web.find_element(By.XPATH, '//*[@id="username"]').send_keys(userName)
            web.find_element(By.XPATH, '//*[@id="password"]').send_keys(password)
            web.find_element(By.XPATH, '//*[@id="fm1"]/div[4]/div/input[5]').click()
            time.sleep(DELAY_TIME + 2)

            # 信息填写部分
            # 填写地区
            if province and city and district:
                sel_el_province = web.find_element(By.XPATH, '//*[@id="province"]')
                sel_province = Select(sel_el_province)
                sel_province.select_by_visible_text(province)

                sel_el_city = web.find_element(By.XPATH, '//*[@id="city"]')
                sel_city = Select(sel_el_city)
                sel_city.select_by_visible_text(city)

                sel_el_district = web.find_element(By.XPATH, '//*[@id="district"]')
                sel_district = Select(sel_el_district)
                sel_district.select_by_visible_text(district)

            # 点击提交按钮
            web.find_element(By.XPATH, '//*[@id="rbxx_div"]/div[27]/div/a').click()
            time.sleep(DELAY_TIME)
            # 点击确认真实无误按钮
            web.find_element(By.XPATH, '//*[@id="qrxx_div"]/div[2]/div[26]/label').click()
            time.sleep(DELAY_TIME)
            # 点击提交按钮
            web.find_element(By.XPATH, '//*[@id="save_div"]').click()
            time.sleep(DELAY_TIME + 1)
            print("%s填报完成" % userName)
            break

        except:
            DELAY_TIME += 1
            web.quit()


def mul_auto_fill(stu_dic_list):
    stu_num = len(stu_dic_list)

    # 创建线程池
    pool = threadpool.ThreadPool(stu_num)
    # 创建请求列表
    request_list = threadpool.makeRequests(auto_fill, stu_dic_list)
    # 将每个请求加入线程池
    for req in request_list:
        pool.putRequest(req)
    pool.wait()  # 等待线程执行完后再执行主线程


if __name__ == '__main__':
    stu_dic_list = [
        {'userName': "2021302779", "password": "q11658059@", 'province': '安徽省', 'city': '合肥市', 'district': '庐江县'},
        {'userName': "2021302730", "password": "hexiaoyu\\20030222", 'province': '宁夏回族自治区', 'city': '中卫市', 'district': '中宁县'}
    ]

    mul_auto_fill(stu_dic_list)
    try:
        os.system("appium -a 0.0.0.0 -p 4723")
        time.sleep(5)
        # 向qq发送完成的消息
        send_notice("疫情填报已全部完成")
    except:
        print("未发送qq消息")
    print("已全部填完")
    os.system("shutdown -s -t 20")
    exit()
