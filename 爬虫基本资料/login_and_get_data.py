#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import re
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains  # 模拟鼠标事件类


def parse_html(html):
    # 使用正则表达式来提取页面信息
    # 注意此处 .*? 与 (.*?) 的用法
    pattern = r'<div class="l-grid-row-cell-inner" style="width:112px;height:22px;min-height:22px; ">(.*?)</div>.*?<div class="l-grid-row-cell-inner" style="width:112px;height:22px;min-height:22px; ">(.*?)</div>.*?<div class="l-grid-row-cell-inner" style="width:92px;height:22px;min-height:22px; ">(.*?)</div>.*?<div class="l-grid-row-cell-inner" style="width:92px;height:22px;min-height:22px; ">(.*?)</div>.*?<div class="l-grid-row-cell-inner" style="width:112px;height:22px;min-height:22px; ">(.*?)</div>.*?<div class="l-grid-row-cell-inner" style="width:122px;height:22px;min-height:22px; ">(.*?)</div>.*?<div class="l-grid-row-cell-inner" style="width:122px;height:22px;min-height:22px; ">(.*?)</div>'
    data_list = re.findall(pattern, html)
    print(len(data_list))
    for data in data_list:
        print(data)
    # with open('test_gbk.csv', 'w', encoding='gkb')
    with open('test_utf8.csv', 'w', encoding='utf-8') as csvfile, open('test2.txt', 'w', encoding='utf-8') as f1:
        writer = csv.writer(csvfile)
        writer.writerow(['id', 'name', 'global_area', 'local_area', 'data', 'start_time', 'end_time'])
        for data in data_list:
            writer.writerow(data)
            # f1.write(str(data) + '\n')

def main():
    # 设置为无头浏览器
    # opt = webdriver.ChromeOptions()
    # opt.set_headless()
    ## opt.add_argument('--proxy-server=http://ip:port')  # 此为通过chrome设置代理ip
    # driver = webdriver.Chrome(options=opt)

    # 此为有界面浏览器
    driver = webdriver.Chrome()
    driver.maximize_window()  # 窗口最大化
    url = '需要登录的网站url'
    driver.get(url)  # 进入网站登录页面
    driver.implicitly_wait(30)  # 智能等待元素加载完成
    
    # 需要特别说明的是：隐性等待对整个driver的周期都起作用，所以只要设置一次即可，我曾看到有人把隐性等待当成了sleep在用，走哪儿都来一下…
    
    driver.find_element_by_xpath('//*[@id="dl"]/input[1]').send_keys('你的用户名')  # 输入用户名
    driver.find_element_by_id('password').click()
    name = driver.find_element_by_id('password')

    # 因为有js存在，不能直接输入密码，所以需要使用鼠标类模拟，再执行js代码来输入密码
    actions = ActionChains(driver).move_to_element(name)  
    driver.execute_script('document.getElementById("password").value="你的密码"')
    driver.find_element_by_xpath('//*[@id="dl"]/input[4]').submit()  # 提交表单
    driver.find_element_by_xpath('//*[@id="apDiv33"]/a').click()  # 点击页面元素
    driver.switch_to.window(driver.window_handles[-1])  # 切换不同的tab页，切换到当前句柄
    driver.find_element_by_xpath('//*[@id="accordion1"]/div[2]/a[2]').click()  # 点击需要的信息
    
    # 切换iframe到数据页
    # 注意：此处如果不查找表格中的一个元素的话，直接写入文件中，会导致表格中的元素都隐藏，写不进去
    driver.switch_to.frame(driver.find_element_by_id('97'))

    # 解决方法：通过查找其中任意一个元素，来展开网页，然后再写入文件，则可以将包含所有的元素的页面都写入文件中
    driver.find_element_by_xpath('//*[@id="maingrid|2|r1001|c103"]/div')

    # print(driver.find_element_by_xpath('//*[@id="maingrid|2|r1001|c103"]/div').text)
    print('----------------------')
    # 通过xpath获取网页数据
    # select = driver.find_element_by_id('maingrid')
    # td_list = select.find_elements_by_tag_name('td')

    # for td in td_list:
    #     if not td.text:
    #         pass
    #     else:
    #         print(td.text)


    # 获取当前页面
    html = driver.page_source
    # with open('test1.txt', 'w', encoding='utf-8') as f:
    #     f.write(html)
    parse_html(html)

if __name__ == '__main__':
    main()  
