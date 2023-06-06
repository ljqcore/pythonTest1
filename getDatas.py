import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import logging
import pymysql

logger = logging.getLogger(__name__)

# https://q.stock.sohu.com/cn/600887/lshq.shtml


def getHTML(stockCode):
    """
    根据stockCode股票编号爬取对应股票的数据

    Args:
        stockCode(int): 股票编号

    Returns:
        str: 爬取后的HTML网页数据内容
    """

    try:
        # 创建 Service 对象并指定 ChromeDriver 所在的路径
        service = Service('/path/to/chromedriver')
        # 隐藏浏览器爬取网页数据
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        # 创建 WebDriver 对象并传入 Service 对象
        driver = webdriver.Chrome(chrome_options=chrome_options, service=service)
        # 通过浏览器驱动打开网页
        url = f'https://q.stock.sohu.com/cn/{stockCode}/lshq.shtml'
        driver.get(url)
        time.sleep(10)  # 等待数据加载完成
        content = driver.page_source.encode('utf-8')
        driver.close()

        # 使用Beautifulsoup整理数据格式
        soup = BeautifulSoup(content, 'html.parser')
        dataList = soup.select("table#BIZ_hq_historySearch tbody tr")
        monthData = []
        for item in dataList[1:]:  # 不要第一行数据
            kv = {}
            if item =='':
                continue
            rows = re.search( r'<td class="e1">(\w+-\w+-\w+)</td><td>(\w*.\w*)</td><td>(\w*.\w*)</td><td>(.\w*.\w*)</td><td>(.\w*.\w*%)</td><td>(\w+.\w+)</td><td>(\w+.\w+)</td><td>(\w+)</td><td>(\w+.\w+)</td><td>(\w*.\w*%)</td>',str(item))
            kv["日期"] = rows.group(1)
            kv["开盘价"] = float(rows.group(2))
            kv["收盘价"] = float(rows.group(3))
            kv["最高价"] = float(rows.group(7))
            kv["最低价"] = float(rows.group(6))
            kv["涨跌额"] = float(rows.group(4))
            kv["成交金额"] = float(rows.group(9))
            kv["成交量"] = float(rows.group(8))
            monthData.append(kv)
        return monthData
    except Exception as e:
        print(e)


def insert_data(stockData):
    """
    向股票历史价格表中传入数据

    Args:
        stockData(dict): 股票数据内容
    """

    # 建立数据库连接
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='123456',
                                 database='stockdata',
                                 charset='utf8')

    try:
        with connection.cursor() as cursor:

            # 插入操作
            for item in stockData:
                sql_ins = "INSERT INTO stock_600887 VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql_ins, (item['日期'], item['开盘价'], item['收盘价'], item['最高价'], item['最低价'], item['涨跌额'], item['成交金额'], item['成交量']))
            connection.commit()
    except pymysql.DatabaseError as error:
        connection.rollback()
        print(error)
    finally:
        # 关闭数据库连接
        cursor.close()
        connection.close()


if __name__ == '__main__':
    Code = '600887'
    data = getHTML(Code)
    print(data)  # 测试
    insert_data(data)
