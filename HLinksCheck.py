#!/usr/bin/python
# -*- coding:utf-8 -*-
'''need to install selenium, using chromedriver and install chrome to use the headless mode'''

import re
from urllib import parse
from tld import get_fld
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

'''
    获取输入url的netloc
    输入参数：  urlProvided                         需要检测的url
    输出参数：  parse.urlparse(urlProvided).netloc  url的netloc
'''


def get_netloc(urlProvided):
    return parse.urlparse(urlProvided).netloc


'''
   检测url网页中是否有暗链
   输入参数：   urlProvided    需要检测的url
   返回参数：   hide_list      url中含有的暗链list
'''


def checkLink(urlProvided):
    node_list = []
    url_list = []
    hide_list = []

    try:
        options = Options()
    # 使用chrome浏览器的无头（headless）模式
        options.add_argument("--headless")
        options.add_argument(
            'user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"')

    # 需要自己配置chrome_driver路径,可放在当前目录下
        chrome_driver = r'./chromedriver'
        driver = webdriver.Chrome(
            executable_path=chrome_driver, chrome_options=options)
        domain = urlProvided
        driver.get(domain)

    # 获得并返回所有a标签
        all_node = driver.find_elements_by_tag_name("a")
        # print(all_node)
        for a in all_node:
            # 检测点是否有herf和src
            url = a.get_attribute("href") or a.get_attribute('src')
            if url is None:
                continue

        # 检测是否有http/https
            http_match = re.search(r"^(http).*", url)

        # 从该点获取url
            if http_match:
                node_list.append(a)
                url_list.append(url)

        netloc = get_netloc(domain)
        domain2 = get_fld(domain)  # 获得二级域名
    #  检测提取出来url是否和检测网页的url有相同的hostname和二级域名
        i = 0
        while i < len(url_list):
            if domain2 == get_fld(url_list[i]) or netloc == get_netloc(url_list[i]):
                node_list.pop(i)
                url_list.pop(i)
                i -= 1
            i += 1

        for i in node_list:
            # is_displayed函数的定义可参考webDriver官网的解释:https://www.w3.org/TR/webdriver/#element-displayedness
            if not i.is_displayed():
                hide_list.append(i)
            else:
                # 检测字体大小
                value = i.value_of_css_property("font-size")
                # 将其转化为int类型
                value = int(re.sub(r"[a-zA-Z]", "", value))
                if value < 2:
                    hide_list.append(i)

                # 检测可见性
                value = i.value_of_css_property('visibility')
                if value == "hidden":
                    hide_list.append(i)

                # 检测颜色    rgba(255, 255, 255, 1)} 白色
                color = i.value_of_css_property('color')
                if color == "rgba(255, 255, 255, 1)":
                    hide_list.append(i)

                # 检测清晰度, 如果低于0.2，我们认为他是一个暗链
                value = i.value_of_css_property('opacity')
                opacity = float(value)
                if opacity <= 0.2:
                    hide_list.append(i)

                # 检测是否display为none
                value = i.value_of_css_property('display')
                if value == 'none':
                    hide_list.append(i)

        # 如果marquee的高度小于5或不显示，我们假设它是一个暗链
        marquee = driver.find_elements_by_tag_name("marquee")
        for i in marquee:
            value = i.value_of_css_property('height')
            height = float(re.sub("[a-zA-Z]", "", str(value)))
            if not i.is_displayed():
                hide_list.append(i.find_element_by_tag_name("a"))
            elif height < 5:
                hide_list.append(i.find_element_by_tag_name('a'))

        # 提取meta中的url
        meta = driver.find_elements_by_tag_name("meta")
        for i in meta:
            if i.get_attribute("url"):
                hide_list.append(i)

        # 检测iframe中的url
        iframe = driver.find_elements_by_tag_name("iframe")
        for i in iframe:
            hide_list.append(i)

    except Exception as e:
        print(e)
        pass
    finally:
        test_list = []
        for i in hide_list:
            if i.get_attribute('href'):
                test_list.append(i.get_attribute("href"))
            elif i.get_attribute("src"):
                test_list.append(i.get_attribute("src"))
            elif i.get_attribute('url'):
                test_list.append(i.get_attribute('url'))
        hide_list = test_list
        driver.quit()
        return hide_list


if __name__ == '__main__':
    # 读取文件url.txt
    with open('url.txt', 'r') as f1:
        urlList = f1.readlines()
    f1.close()
    url_index = 0
    for urlProvided in urlList:
        urlProvided = urlProvided.rstrip('\n')
        hide_list = checkLink(urlProvided)

        target_num = len(hide_list)
        if target_num > 0:
            print("\nThe url: " + urlProvided + ' contains HiddenLinks:')
            print(hide_list)
            # 输出到txt中
            result_txt = 'url' + str(url_index) + 'result.txt'
            if not os.path.exists(result_txt):
                with open(result_txt, "w")as fobj1:
                    fobj1.write("The url: " + urlProvided +
                                " contains hidden links!\n\n")
                    fobj1.write("The hidden links are as follow: " + "\n\n")
                    for i in range(target_num):
                        fobj1.write(hide_list[i]+"\n")
                fobj1.close()
        else:
            print("The url: " + urlProvided + 'doesn\'t contain HiddenLinks\n')
        url_index += 1
