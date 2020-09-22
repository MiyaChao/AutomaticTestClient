from telnetlib import EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from constant.BaseConstant import firefoxDriverPath
from method.PublicMethod import drivers
from operate.MySqlOperate import mySqlOperate


class seleniumOperate:

    @staticmethod
    def queryElement(elementId):
        queryElementSql = "select * from `element` where id = %s"
        queryElementSqlParamList = [elementId]
        queryElementSqlResult = mySqlOperate.search(queryElementSql, queryElementSqlParamList)
        if queryElementSqlResult is None:
            raise Exception("查询元素失败")
        else:
            if not (len(queryElementSqlResult) > 0):
                raise Exception("元素不存在，"+elementId)
            else:
                elementData = queryElementSqlResult[0]
                ByType = None
                locateMode = elementData[2]
                locatePath = elementData[3]
                elementNumber = elementData[12]
                if not isinstance(locateMode, str):
                    raise Exception("locateMode必须为字符串\n")
                if not isinstance(locatePath, str):
                    raise Exception("locatePath必须为字符串\n")
                if locateMode == "id":
                    ByType = By.ID
                elif locateMode == "xpath":
                    ByType = By.XPATH
                elif locateMode == "name":
                    ByType = By.NAME
                elif locateMode == "className":
                    ByType = By.CLASS_NAME
                elif locateMode == "tagName":
                    ByType = By.TAG_NAME
                elif locateMode == "linkText":
                    ByType = By.LINK_TEXT
                elif locateMode == "partialLinkText":
                    ByType = By.PARTIAL_LINK_TEXT
                elif locateMode == "cssSelector":
                    ByType = By.CSS_SELECTOR
                else:
                    raise Exception("元素定位数据错误-locateMode\n")
                if elementNumber == "only one":
                    element = seleniumOperate.public_driver_findElement(drivers.driver, ByType, locatePath)
                    return element
                elif elementNumber == "all":
                    elements = seleniumOperate.public_driver_findElements(drivers.driver, ByType, locatePath)
                    return elements
                else:
                    raise Exception("元素定位数据错误-number\n")

    @staticmethod
    def openBrowser(browserType, browserNo, runMode):
        driverPath = None
        if browserType == "Firefox":
            driverPath = firefoxDriverPath  # 驱动路径
            firefox_option = webdriver.FirefoxOptions()
            if runMode == "noWindow":
                firefox_option.set_headless()  # 设置无界面运行
                firefox_option.add_argument('--disable-gpu')  # 设置无界面运行
            driver = webdriver.Firefox(executable_path=driverPath, service_log_path='../geckodriver_service.log', firefox_options=firefox_option)
        driver.maximize_window()  # 最大化浏览器
        driver.implicitly_wait(30)  # 隐性等待，最长等30秒
        if browserNo == "1":
            drivers.seleniumDriver = driver
        elif browserNo == "2":
            drivers.seleniumDriver_2 = driver
        return driver

    @staticmethod
    def getCurrentUrl(driver):
        return driver.current_url

    @staticmethod
    def getUrl(driver, url):
        driver.get(url)

    @staticmethod
    def quitBrowser(driver):
        driver.quit()

    @staticmethod
    def refresh(driver):
        driver.refresh()

    @staticmethod
    def public_driver_findElement(driver, ByType, value):
        try:
            WebDriverWait(driver, 10, 1).until(EC.presence_of_element_located((ByType, value)))
        except:
            pass
        finally:
            return driver.find_element(ByType, value)

    @staticmethod
    def public_driver_findElements(driver, ByType, value):
        try:
            WebDriverWait(driver, 10, 1).until(EC.presence_of_element_located((ByType, value)))
        except:
            pass
        finally:
            return driver.find_elements(ByType, value)

    @staticmethod
    def public_element_findElement(driver, element, ByType, value):
        try:
            WebDriverWait(driver, 10, 1).until(EC.presence_of_element_located((ByType, value)))
        except:
            pass
        finally:
            return element.find_element(ByType, value)

    @staticmethod
    def public_element_findElements(driver, element, ByType, value):
        try:
            WebDriverWait(driver, 10, 1).until(EC.presence_of_element_located((ByType, value)))
        except:
            pass
        finally:
            return element.find_elements(ByType, value)

    @staticmethod
    def public_element_click(driver, element):
        try:
            WebDriverWait(driver, 10, 1).until(EC.presence_of_element_located(element))
        except:
            pass
        finally:
            return element.click()

    @staticmethod
    def public_element_clear(driver, element):
        try:
            WebDriverWait(driver, 10, 1).until(EC.presence_of_element_located(element))
        except:
            pass
        finally:
            return element.clear()

    @staticmethod
    def public_element_sendKeys(driver, element, inputContent):
        try:
            WebDriverWait(driver, 10, 1).until(EC.presence_of_element_located(element))
        except:
            pass
        finally:
            return element.send_keys(inputContent)

    @staticmethod
    def public_element_getAttribute(driver, element, attributeName):
        try:
            WebDriverWait(driver, 10, 1).until(EC.presence_of_element_located(element))
        except:
            pass
        finally:
            return element.get_attribute(attributeName)


