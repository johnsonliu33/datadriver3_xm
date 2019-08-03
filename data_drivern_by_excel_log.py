# encoding=utf-8
from selenium import webdriver
import unittest, time
import logging, traceback
import ddt
from xm.ExcelUtil import ParseExcel
from selenium.common.exceptions import NoSuchElementException

"""
ddt单元测试，不用for循环，以元组方式获取数据
"""


# 初始化日志对象
logging.basicConfig(
    # 日志级别
    level = logging.INFO,
    # 日志格式
    # 时间、代码所在文件名、代码行号、日志级别名字、日志信息
    format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    # 打印日志的时间
    datefmt = '%a, %Y-%m-%d %H:%M:%S',
    # 日志文件存放的目录（目录必须存在）及日志文件名
    filename = 'e:/dataDriveRreport.log',
    # 打开日志文件的方式
    filemode = 'w'
)

excelPath = 'data.xlsx'
sheetName = "搜索数据表"
# 创建ParseExcel类的实例对象
excel = ParseExcel(excelPath, sheetName)

@ddt.ddt
class TestDemo(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    @ddt.data(*excel.getDatasFromSheet())
    def test_dataDrivenByFile(self, data):
        testData, expectData = tuple(data)
        url = "http://www.baidu.com"
        # 访问百度首页
        self.driver.get(url)
        # 将浏览器窗口最大化
        self.driver.maximize_window()
        print (testData, expectData)
        # 设置隐式等待时间为10秒
        self.driver.implicitly_wait(10)

        try:
            # 获取当前的时间戳，用于后面计算查询耗时用
            start = time.time()
            # 获取当前时间的字符串，表示测试开始时间
            startTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # 找到搜索输入框，并输入测试数据
            self.driver.find_element_by_id("kw").send_keys(testData)
            # 找到搜索按钮，并点击
            self.driver.find_element_by_id("su").click()
            time.sleep(3)
            # 断言期望结果是否出现在页面源代码中
            self.assertTrue(expectData in self.driver.page_source)
            print ("搜索%s，期望%s" %(testData, expectData))
        except NoSuchElementException as e:
            logging.error("查找的页面元素不存在，异常堆栈信息："\
                          + str(traceback.format_exc()))
        except AssertionError as e:
            print("断言失败了")
            logging.info("搜索“%s”，期望“%s”，失败" %(testData, expectData))
        except Exception as e:
            logging.error("未知错误，错误信息：" + str(traceback.format_exc()))
        else:
            logging.info("搜索“%s”，期望“%s”通过" %(testData, expectData))

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()
