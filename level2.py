# encoding=utf8
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import csv
from selenium import webdriver
from goose3 import Goose
from goose3.text import StopWordsChinese  # 中文库
import shutil, os

def nChrome():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    return driver

def openChrome():
    try:
        option = webdriver.ChromeOptions()
        option.add_argument('disable-infobars')
        driver = webdriver.Chrome(chrome_options=option)
        # driver.maximize_window()  # 最大化浏览器
        return driver
    except:
        print("有错误发生，驱动程序缺失或浏览器版本不匹配，或环境变量未配置")
        time.sleep(5)
        exit()

def Open_w(w_num):
    base_url = "http://finance.eastmoney.com/a/cdfsd_{page}.html"
    num = 1  # 文章计数
    page = 1  # 页数计数
    entry = 1  # 条目计数
    articles = []  # csv内容存入
    for i in range(1, w_num+1):
        url = base_url.format(page=i)
        try:
            driver.get(url)
            # lxml解析器 速度快 文档纠错能力强 需要安装C语言库
            time.sleep(1)  # 缓冲
            titles = BeautifulSoup(driver.page_source, 'lxml').find_all('div', {'class': 'text'})
            if titles:
                print("||||||------------第{0}页爬取内容已获得------------||||||".format(page))
                for title in titles:  # 注意，xpath失败由于类型错误
                    id = num
                    new_title = title.find('a').get_text().replace(' ', '').strip('\n')
                    new_summ = title.find('p', {'class': 'info'}).get_text().replace(' ', '').strip('\n')
                    new_time = title.find('p', {'class': 'time'}).get_text().replace(' ', '').strip('\n')
                    url = title.find('a')['href']
                    # sub_ord(title, url)  # 提速开进程4
                    if num == 1:
                        make_path()
                    Identification(new_title, url)
                    articles.append([id, new_title, new_summ, new_time, url])
                    num = num + 1
                    entry = entry + 1
                entry = 1
                print("||||||------------第{0}页爬取完毕！！！------------||||||".format(page))
                page = page + 1
            else:
                print("请检查网页结构是否发生变化")
                time.sleep(5)
                exit()
        except:
            print("请更换ip或增加代理池，预防黑名单")
            time.sleep(5)
            exit()
    save_data(articles)

# 识别模式
def Identification(title, url):
    g = Goose({'stopwords_class': StopWordsChinese})
    article = g.extract(url=url)
    try:
        filename = ".\\Content\\" + title + ".txt"
        with open(filename, 'w') as f:
            f.write(article.cleaned_text[0:])
    except IOError:
        print("文件发生异常，请检查文件！！！")
        f.close()
        time.sleep(5)
        exit()

def make_path():
    if "Content" in os.listdir():
        if input("当前目录下存储文件夹Content已存在，是否需要删除？Y/N:   ") in ['Y', 'y']:
            shutil.rmtree("Content")
            os.mkdir("Content")
    else:
        os.mkdir("Content")

# 普通模式, 速度太慢！！！
# def sub_ord(sub_title, url):
#     driver.get(url)
#     titles = BeautifulSoup(driver.page_source, 'lxml').find_all('div', {'class': 'Body'})
#     if titles:
#         for title in titles:
#             new_summ = title.get_text().replace(' ', '').strip('\n')
#             print(new_summ)
#     else:
#         print("请检查网页结构是否发生变化")
#         time.sleep(5)
#         exit()
#     try:
#         filename = sub_title + ".txt"
#         with open(filename, 'w') as f:
#             f.write(new_summ)
#     except IOError:
#         print("文件发生异常，请检查文件！！！")
#         f.close()
#         time.sleep(5)
#         exit()
#     driver.close()

# def Content(driver):
#         try:
#             links = driver.find_elements_by_xpath("//*[@id='newsListContent']/li[" + str(i) + "]/div[2]/p[1]/a")
#             for link in links:
#                 urls.append(link.get_attribute('href'))
#         except:
#             print("写法出现错误")

def save_data(articles):
    try:
        with open('save.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['文章id', '文章标题', '文章摘要', '发表时间', '文章链接'])
            try:
                for row in articles:
                    writer.writerow(row)
                print("保存完毕！！！随时停止")
            except ValueError:
                print("文件写入发生异常，请检查数据！！！")
                time.sleep(5)
                exit()
    except IOError:
        print("文件发生异常，请检查文件！！！")
        f.close()
        time.sleep(5)
        exit()

if __name__ == '__main__':
    # w_num = int(input("请输入爬取页面数量: "))
    w_num = 2
    driver = nChrome()
    while 1:
        result = EC.alert_is_present()(driver)
        if result:
            print("alert 存在弹窗，处理后再试验")
        else:
            print("alert 未弹出！")
            break
    Open_w(w_num)
    # content = driver.page_source.encode('utf-8')
    confirm = input("数据已成功爬取并存储，是否查看？Y（查看文件）|N（关闭进程）：")
    if confirm == 'Y' or confirm == 'y':
        import os
        os.system("start save.csv")
        driver.close()
    else:
        driver.close()