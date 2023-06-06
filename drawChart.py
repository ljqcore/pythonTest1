import csv
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import mpl_finance
import pandas
import pymysql


def findall_db_data(start_date, end_date):
    """
    接受时间起止参数从数据库中查询并返回数据

    Args:
        start_date(str): 查询股票数据的起始日期
        end_date(str):查询股票数据的终止日期

    Returns:
        list[dict]: 查询限定时间内的股票数据字典
    """

    # 建立数据库连接
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='123456',
                                 database='stockdata',
                                 charset='utf8')

    data = []
    try:
        # 创建游标对象
        with connection.cursor() as cursor:
            sql_sel = "SELECT * FROM stock_600887 WHERE `datatime` BETWEEN '{}' AND '{}'".format(start_date, end_date)
            cursor.execute(sql_sel)
            result_set = cursor.fetchall()  # 提取结果
            print(result_set)

            for row in result_set:
                fields = {'日期': str(row[0]), '开盘价': float(row[1]), '收盘价': float(row[2]), '最高价': float(row[3]),
                          '最低价': float(row[4]), '涨跌额': float(row[5]), '成交金额': float(row[6]),  '成交量': float(row[7])}
                data.append(fields)

    except pymysql.DatabaseError as error:
        print('数据查询失败' + error)
    finally:
        # 关闭连接
        cursor.close()
        connection.close()

    # 返回字典列表
    return data


def fetchData(stockCode, start_date, end_date):
    """
    接受股票编号参数查询数据并写入文件中

    Args:
        stockCode(int): 股票编号
        start_date(str): 数据开始时间
        end_date(str): 数据结束时间

    Returns:
        file: 写入数据后的csv文件对象
    """

    data = findall_db_data(start_date, end_date)
    print('查询到的数据data=' + str(data))

    # 列名
    colsName = ['日期', '开盘价', '收盘价', '最高价', '最低价', '成交量']
    # 临时数据文件名
    dataFile = str(stockCode) + 'temp.csv'
    # 写入数据到临时数据文件
    with open(dataFile, 'w', newline='', encoding='utf-8') as wf:
        writer = csv.writer(wf)
        writer.writerow(colsName)
        for quotes in data:
            row = [quotes['日期'], quotes['开盘价'], quotes['收盘价'],
                   quotes['最高价'], quotes['最低价'], quotes['成交量']]
            writer.writerow(row)

    return dataFile


def drawLine(start, end):
    """
    股票历史成交量折线图

    Args:
        start(str): 数据开始时间
        end(str): 数据结束时间
    """

    plt.rcParams['font.family'] = ['SimHei']
    start_date = start
    end_date = end
    datas = findall_db_data(start_date, end_date)
    dates_map = map(lambda it: it['日期'], datas)
    dates = list(dates_map)
    dates.sort()
    volumes_map = map(lambda it: it['成交量'], datas)
    volumes = list(volumes_map)

    # 设置x轴刻度间隔为12天
    x_ticks = [dates[i] for i in range(len(dates)) if i % 12 == 0]
    x_labels = [str(x_ticks[i]) for i in range(len(x_ticks))]
    # fig修改整个图像的属性，ax是Axes子图对象，绘制数据的独立区域
    fig, ax = plt.subplots()
    # 调整子图参数SubplotParams
    fig.subplots_adjust(bottom=0.2)
    plt.plot(dates, volumes)
    plt.title("此股票历史过去三个月的成交量")
    plt.ylabel("成交量")
    plt.xlabel("交易日期")

    # 设置x轴刻度和标签向右对齐
    plt.xticks(x_ticks, x_labels, rotation=20, horizontalalignment='right')
    # 将图片保存下来
    plt.savefig('img/plot1.png')
    plt.show()


def drawBar(data_list, p_list, y):
    """
    绘制柱状图

    Args:
        data_list(list): 日期数据列表
        p_list(list): 数据内容列表
        y(str): y轴标签
    """

    # 设置为中文
    plt.rcParams['font.family'] = ['SimHei']
    plt.bar(data_list, p_list)
    plt.title("该股票历史成交量")
    plt.ylabel(y)
    plt.xlabel("交易日期")
    # 设置x轴刻度间隔为15天
    x_ticks = [data_list[i] for i in range(len(data_list)) if i % 12 == 0]
    x_labels = [str(x_ticks[i]) for i in range(len(x_ticks))]
    plt.xticks(x_ticks, x_labels, rotation=10, horizontalalignment='right')


def drawOHLC(start, end):
    """
    绘制OHLC图

    Args:
        start(str): 数据开始时间
        end(str): 数据结束时间
    """

    plt.rcParams['font.family'] = ['SimHei']
    start_date = start
    end_date = end
    datas = findall_db_data(start_date, end_date)
    # 日期数据
    dates_map = map(lambda it: it['日期'], datas)
    dates = list(dates_map)
    # 读出数据后根据日期将数据进行排序
    dates.sort()
    # 开盘价
    open_map = map(lambda it: it['开盘价'], datas)
    open = list(open_map)
    # 收盘价
    close_map = map(lambda it: it['收盘价'], datas)
    close = list(close_map)
    # 最高价
    high_map = map(lambda it: it['最高价'], datas)
    high = list(high_map)
    # 最低价
    low_map = map(lambda it: it['最低价'], datas)
    low = list(low_map)

    # 4行1列第一个位置
    plt.subplot(411)
    # 画出柱状图
    drawBar(dates, open, "开盘价")

    plt.subplot(412)
    drawBar(dates, close, "收盘价")

    plt.subplot(413)
    drawBar(dates, high, "最高价")

    plt.subplot(414)
    drawBar(dates, low, "最低价")

    plt.tight_layout()  # 调整布局
    # 将图片保存下来
    plt.savefig('img/plot2.png')
    plt.show()


def drawK(file):
    """
    接受文件数据画一个K线图

    Args:
        file(): 读取的数据文件对象
    """

    # 设置为中文
    plt.rcParams['font.family'] = ['SimHei']
    quotes = pandas.read_csv(file,
                             index_col=0,
                             parse_dates=True,
                             infer_datetime_format=True)
    # 读出数据后根据日期将数据进行排序
    quotes = quotes.sort_index()
    # 绘制一个子图，并设置子图大小
    fig, ax = plt.subplots()
    # 调整子图参数SubplotParams
    fig.subplots_adjust(bottom=0.2)

    print("读出的数据内容：")
    print(quotes)
    # 转换数据格式的时候不能改变“开盘价”“最高价”之间的顺序
    mpl_finance.candlestick_ohlc(ax, zip(mdates.date2num(quotes.index.to_pydatetime()),
                                         quotes['开盘价'], quotes['最高价'], quotes['最低价'], quotes['收盘价'], ),
                                 width=1, colorup='r', colordown='g', alpha=0.6)

    ax.xaxis_date()
    ax.autoscale_view()
    plt.title("此股票历史过去一个月的数据")
    plt.xlabel('日期')
    plt.ylabel('价格（元）')
    plt.plot(quotes.index, quotes['开盘价'], 'r-', label='开盘价')
    plt.plot(quotes.index, quotes['最高价'], 'b-', label='最高价')
    plt.plot(quotes.index, quotes['最低价'], 'y-', label='最低价')
    plt.plot(quotes.index, quotes['收盘价'], 'g-', label='收盘价')
    plt.legend(loc='best', fontsize=16)  # 添加图例，best自适应
    # 获取当前 Axes 对象的 X 轴刻度标签，并将它们的旋转角度设置为 20 度，水平对齐方式设置为右对齐
    plt.setp(plt.gca().get_xticklabels(), rotation=20, horizontalalignment='right')
    # 将图片保存下来
    plt.savefig('img/plot3.png')
    plt.show()


if __name__ == '__main__':
    datafile = fetchData(600887, '2023-04-01', '2023-04-27')
    drawK(datafile)
    drawLine('2023-01-01', '2023-04-27')
    drawOHLC('2023-01-01', '2023-04-27')

