from selenium import webdriver
import time,re,os
from bs4 import BeautifulSoup
import pandas as pd
import xlwt
from xlutils.copy import copy
import xlrd

path = os.getcwd().replace('\\','/')+'/'

person = []

url = 'http://zc.fzb.suda.edu.cn/charity_list' #苏大基金会捐款信息公布门户

def open_browser(url):
    driver = webdriver.Chrome()
    driver.get(url)
    return driver


def save(soup,cnt):
    for tr in soup.find_all('tr'):
        '''
        比较傻的分词法
        '''
        try:
            name = str(tr.text).split('抗击新冠肺炎专项基金')[0]
            money = str(tr.text).split('抗击新冠肺炎专项基金')[1].split('元')[0]
            date = str(tr.text).split('元')[1]
            mes = ' '
            if date[0] == '2':
                mes = ' '
            else:
                mes = date[0:-8]
                date = date[-8:]
            person.append([name,money,mes,date])
        except:
            continue    
    workbook = xlrd.open_workbook('捐款.xls', formatting_info=False)
    new_book = copy(workbook)
    sheet = new_book.get_sheet(0)
    for r in range(10):
        for c in range(4):
            sheet.write(r + cnt * 10, c, person[r + cnt * 10][c])     
    new_book.save('捐款.xls')

def scrapy(driver):
    content = driver.page_source.encode('utf-8')
    soup1 = BeautifulSoup(content, 'lxml')
    wbk = xlwt.Workbook()
    wbk.add_sheet('sheet 1')
    wbk.save('捐款.xls')  
    print('第一页')
    save(soup1,0)
    for page in range(2,100000): #最后一页设置的大一点
        button = "//*[@class='ant-pagination-item ant-pagination-item-" + str(page) + "']" #翻页按钮
        driver.find_elements_by_xpath(button)[0].click()
        content = driver.page_source.encode('utf-8')
        soup1 = BeautifulSoup(content, 'lxml')
        save(soup1,page - 1)
        print(page)
        time.sleep(2)
    
if __name__ == '__main__':
    driver = open_browser(url)
    time.sleep(10) #加载页面比较慢，可以睡得长一点
    scrapy(driver)

    



