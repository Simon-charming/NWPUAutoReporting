from selenium import webdriver
from selenium.webdriver.common.by import By
# 导入处理<select>标签的工具
from selenium.webdriver.support.select import Select
# 导入无头参数需要的包，注意应导入对应浏览器的option包
from selenium.webdriver.chrome.options import Options
# 线程池包
import threadpool
# 微信公众号发送消息模块
from wxgzh import SendMessage
# 等待响应包
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# 命令行传入参数包
import argparse
# 系统操作包
import os

from selenium.webdriver.chrome.service import Service


def get_web_driver():
    # 参数
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
    chrome_options.add_argument('window-size=1920x1080')  # 指定浏览器分辨率
    chrome_options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
    chrome_options.add_argument('--headless')  # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
    # 指定路径
    chromedriver = "/usr/bin/chromedriver"
    os.environ["webdriver.chrome.driver"] = chromedriver
    s = Service(chromedriver)
    driver = webdriver.Chrome(service=s, options=chrome_options)
    driver.implicitly_wait(30) # 所有的操作都可以最长等待30s
    return driver


class AutoReporting:
    def __init__(self, stu_dic):
        self.url = "https://yqtb.nwpu.edu.cn/wx/ry/jrsb_xs.jsp"
        self.send = SendMessage(appID=stu_dic['appID'], appSecret=stu_dic['appSecret'],open_id=stu_dic['open_id'])

    def auto_fill(self, stu_dic):
        userName = stu_dic['userName']
        password = stu_dic['password']
        province = stu_dic['province']
        city = stu_dic['city']
        district = stu_dic['district']

        while True:
            web = get_web_driver()
            web.get(self.url)

            # 创建等待对象
            wait = WebDriverWait(web, 15) # 最多等待web 15秒
            # 进入填报的登录页面
            # 输入账号
            userName_element = wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="username"]'))
            )
            userName_element.send_keys(userName)
            # 输入密码
            password_element = wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="password"]'))
            )
            password_element.send_keys(password)
            # 点击登录按钮
            logOn_element = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="fm1"]/div[4]/div/input[5]'))
            )
            logOn_element.click()

            # 进入疫情填报界面
            # 填写地区（不在西安）
            if province:
                inCountry_element = wait.until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="notlocation"]/label[3]'))
                )
                inCountry_element.click()

                province_element = wait.until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="province"]'))
                )
                sel_province = Select(province_element)
                sel_province.select_by_visible_text(province)

                city_element = wait.until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="city"]'))
                )
                sel_city = Select(city_element)
                sel_city.select_by_visible_text(city)

                district_element = wait.until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="district"]'))
                )
                sel_district = Select(district_element)
                sel_district.select_by_visible_text(district)

            # 在学校
            else:
                inSchool_element = wait.until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="notlocation"]/label[1]'))
                )
                inSchool_element.click()

            # 填写地区（在西安）
            if city == '西安市':
                inXian_element = wait.until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="notlocation"]/label[2]'))
                )
                inXian_element.click()

                district_element = wait.until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="district"]'))
                )
                sel_district = Select(district_element)
                sel_district.select_by_visible_text(district)

                detailed_element = wait.until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="xaxxdz"]'))
                )
                detailed_element.send_keys(stu_dic['detailed'])

            # 提交阶段
            # 点击提交按钮
            oneSubmit_element = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="rbxx_div"]/div[27]/div/a'))
            )
            oneSubmit_element.click()
            # 点击确认真实无误按钮
            ensure_element = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="qrxx_div"]/div[2]/div[26]/label'))
            )
            ensure_element.click()
            # 点击提交按钮
            secondSubmit_element = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="save_div"]'))
            )
            secondSubmit_element.click()

            # 发送填报完成的信息
            self.send.send_message("%s已填报完成" % userName)
            print("%s填报完成" % userName)
            break



    # def mul_auto_fill(self):
    #     stu_num = len(self.stu_dic_list)
    #     # 创建线程池
    #     pool = threadpool.ThreadPool(stu_num)
    #     # 创建请求列表
    #     request_list = threadpool.makeRequests(self.auto_fill, self.stu_dic_list)
    #     # 将每个请求加入线程池
    #     for req in request_list:
    #         pool.putRequest(req)
    #     pool.wait()  # 等待线程执行完后再执行主线程


def accept_parser():
    parser = argparse.ArgumentParser(description='疫情填报程序的命令行参数设置')
    parser.add_argument('--userName', '-u', help='学号 属性，必要参数，无默认值', required=True)
    parser.add_argument('--password', '-p', help='密码 属性，必要参数，无默认值', default=2017, required=True)
    parser.add_argument('--province', '-pr', help='省份 属性，非必要参数，必须要填全名（如宁夏回族自治区），不填默认为在学校', default='')
    parser.add_argument('--city', '-c', help='城市 属性，非必要参数，必须要填全名（如合肥市）', default='')
    parser.add_argument('--district', '-d', help='区县 属性，非必要参数，必须要填全名（如长安区）', default='')
    parser.add_argument('--detailed', '-de', help='详细居住地 属性，非必要参数，如住在西安且不在学校需填写现居住地址（##街道##小区#号楼#单元#室）', default='')

    parser.add_argument('--appID', '-ai', help='appid 属性，通过微信测试公众号获取，必要参数，无默认值', required=True)
    parser.add_argument('--appSecret', '-as', help='appSecret 属性，通过微信测试公众号获取，必要参数，无默认值', required=True)
    parser.add_argument('--open_id', '-o', help='学号 属性，必要参数，通过微信测试公众号获取，无默认值', required=True)

    args = parser.parse_args()
    stu_dic = {
        'userName': args.userName, "password": args.password, 'province': args.province, 'city': args.city, 'district': args.district,'detailed': args.detailed,
        'appID': args.appID, 'appSecret': args.appSecret, 'open_id': args.open_id
    }
    return stu_dic


def main():
    stu_dic = accept_parser()
    auto_report = AutoReporting(stu_dic)
    try:
        auto_report.auto_fill(stu_dic)
    except:
        send = SendMessage(appID=stu_dic['appID'], appSecret=stu_dic['appSecret'],open_id=stu_dic['open_id'])
        send.send_message("%s填报失败" % stu_dic['userName'])
        print("%s填报失败" % stu_dic['userName'])


if __name__ == '__main__':
    main()
    print("程序结束")
