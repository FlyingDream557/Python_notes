#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import re
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options


def login(driver, url):
    driver.get(url)
    driver.implicitly_wait(30)  # 智能等待元素加载完成
    # 需要特别说明的是：隐性等待对整个driver的周期都起作用，所以只要设置一次即可，我曾看到有人把隐性等待当成了sleep在用，走哪儿都来一下…
    
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="dl"]/input[1]').send_keys('152307')
    driver.find_element_by_id('password').click()
    name = driver.find_element_by_id('password')
    actions = ActionChains(driver).move_to_element(name)
    driver.execute_script('document.getElementById("password").value="aiNI19930827"')
    time.sleep(1.5)
    driver.find_element_by_xpath('//*[@id="dl"]/input[4]').submit()
    driver.find_element_by_xpath('//*[@id="apDiv33"]/a').click() 
    # 句柄已经切换过来，但是焦点没有切过去。 需要将焦点切过来，才能对当前页进行操作
    driver.switch_to.window(driver.window_handles[-1])  # 切换不同的tab页
    driver.find_element_by_xpath('//*[@id="accordion1"]/div[2]/a[2]').click()

    # 切换iframe到数据页
    # 注意：此处如果不查找表格中的一个元素的话，直接写入文件中，会导致表格中的元素都隐藏，写不进去
    driver.switch_to.frame(driver.find_element_by_id('97'))
    # 解决方法：通过查找其中一个，展开网页，然后再写入文件，则可以将所有的元素都写入文件
    driver.find_element_by_xpath('//*[@id="maingrid|2|r1001|c103"]/div')


def parse_html1(html):
    # 使用正则表达式提取信息
    pattern = r'<div class="l-grid-row-cell-inner" style="width:112px;height:22px;min-height:22px; ">(.*?)</div>.*?<div class="l-grid-row-cell-inner" style="width:112px;height:22px;min-height:22px; ">(.*?)</div>.*?<div class="l-grid-row-cell-inner" style="width:92px;height:22px;min-height:22px; ">(.*?)</div>.*?<div class="l-grid-row-cell-inner" style="width:92px;height:22px;min-height:22px; ">(.*?)</div>.*?<div class="l-grid-row-cell-inner" style="width:112px;height:22px;min-height:22px; ">(.*?)</div>.*?<div class="l-grid-row-cell-inner" style="width:122px;height:22px;min-height:22px; ">(.*?)</div>.*?<div class="l-grid-row-cell-inner" style="width:122px;height:22px;min-height:22px; ">(.*?)</div>'
    data_list = re.findall(pattern, html)
    print(len(data_list))
    for data in data_list:
        print(data)
    with open('test.csv', 'a', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for data in data_list:
            writer.writerow(data)


def parse_html2(html):
    # 使用BeautifulSoup提取信息
    soup = BeautifulSoup(html, 'lxml')
    # table有2个，取后面那个
    table = soup.find_all('table', {'class': 'l-grid-body-table'})[-1]

    data_list = []
    for tr in table.find_all('tr'):
        data = []
        for td in tr.find_all('div', {'class': 'l-grid-row-cell-inner'}):
            data.append(td.get_text())

        print(data)
        data_list.append(data)

    with open('test.csv', 'a', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for data in data_list:
            writer.writerow(data)

def parse_html(html):
    ''' 
        使用 xpath 来提取网页信息
        XPath 是一门在 XML 文档中查找信息(节点)的语言。
        XPath 可用来在 XML 文档中对元素和属性进行遍历。
    '''
    html = etree.HTML(html)
    tr_list = html.xpath('//*[@id="maingridgrid"]/div[4]/div[2]/div/table/tbody/tr')
    data_list = []          
    for tr in tr_list:      
        data = []           
        for td in tr.xpath('./td/div[@class="l-grid-row-cell-inner"]'):
            data.append(td.text) 
        print(data)
        data_list.append(data)
    # print(data_list)

    with open('test.csv', 'a', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for data in data_list:
            writer.writerow(data)
            

def main():
    # 设置为无头浏览器
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # define headless

    driver = webdriver.Chrome(chrome_options=chrome_options)
    # driver.maximize_window()
    url = '需要登录的网址' 
    login(driver, url)

    with open('test.csv', 'a', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['字段1', '字段2', '字段3', '字段4', '字段5', '字段6', '字段7'])


    # 得到一共有几页
    nums = int(driver.find_element_by_xpath('//*[@id="maingrid"]/div[5]/div/div[6]/span/span').text)
    print('========================================', nums)

    for i in range(nums):
        # 循环得到所有页面
        html = driver.page_source
        parse_html(html)

        # 得到下一页的位置并点击，点击后页面会自动更新，只需要重新获取driver.page_source即可
        driver.find_element_by_xpath('//*[@id="maingrid"]/div[5]/div/div[8]/div[2]/span').click()
        # 注意：此处一定要强制等待5s，或者更久，不然可能新的页面没加载出来。得到的还是原来的页面
        time.sleep(5)    
  
    driver.quit()  # 关闭浏览器，并退出驱动程序


if __name__ == '__main__':
    main()  
