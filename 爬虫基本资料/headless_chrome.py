from selenium import webdriver

'''
    topic:此为将Chrome设置为无头浏览器模式的2种方法
'''


def method1(url):
    # 创建chrome参数对象
    opt = webdriver.ChromeOptions()
    # 把chrome设置成无界面模式，不论windows还是linux都可以，自动适配对应参数
    opt.set_headless()
    # 创建chrome无界面对象
    driver = webdriver.Chrome(options=opt)
    driver.get(url)
    # 打印内容
    print(driver.page_source)


def method2(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument('--proxy-server=http://ip:port')  # 此为通过chrome设置代理ip
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(url)
    print(driver.page_source)


if __name__ == '__main__':
    url = 'https://www.baidu.com'
    method1(url)
    # method2(url)
