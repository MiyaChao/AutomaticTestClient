import time
from telnetlib import EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from constant.BaseConstant import *
from appium import webdriver
from method.PublicMethod import drivers

# appium所有操作强制等待的时间（秒）
timeSleep = 2


class appiumOperate:

    @staticmethod
    def getCapabilities(phoneNo):
        capabilities = {}
        capabilities["automationName"] = "UiAutomator1"
        if phoneNo == "1":
            # 手机操作系统
            capabilities["platformName"] = platformName
            # 操作系统版本
            capabilities["platformVersion"] = platformVersion
            # 手机名字，一般与udid一样
            capabilities["deviceName"] = deviceName
            # 连接手机的唯一标识
            capabilities["udid"] = udid
            #
            capabilities["chromeOptions"] = {
                "androidProcess": "com.tencent.mm:tools"
            }
        if phoneNo == "2":
            # 手机操作系统
            capabilities["platformName"] = platformName_2
            # 操作系统版本
            capabilities["platformVersion"] = platformVersion_2
            # 手机名字，一般与udid一样
            capabilities["deviceName"] = deviceName_2
            # 连接手机的唯一标识
            capabilities["udid"] = udid_2
        # app包名
        capabilities["appPackage"] = appPackage
        # 要启动的Android Activity名
        capabilities["appActivity"] = appActivity
        # 是否跳过appiumServer安装
        capabilities["skipServerInstallation"] = True
        # 是否跳过appiumDevice安装
        capabilities["skipDeviceInitialization"] = True
        # 不要在会话前重置应用状态
        capabilities["noReset"] = True
        # Android是否删除应用，IOS是否删除整个模拟器目录
        capabilities["fullReset"] = False
        # 是否启动Unicode输入法
        capabilities["unicodeKeyboard"] = True
        # 结束时是否切换回默认输入法
        capabilities["resetKeyboard"] = True
        capabilities["chromedriverExcutable"] = chromeDriverPath

        return capabilities

    @staticmethod
    def linkPhone():
        driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', appiumOperate.getCapabilities("1"))
        driver.implicitly_wait(30)
        drivers.appiumDriver = driver
        time.sleep(2)

    @staticmethod
    def linkPhone_2():
        driver = webdriver.Remote('http://127.0.0.1:4725/wd/hub', appiumOperate.getCapabilities("2"))
        driver.implicitly_wait(30)
        drivers.appiumDriver_2 = driver
        time.sleep(2)

    @staticmethod
    def gotoWebView(driver):
        driver.switch_to.context("WEBVIEW_com.tencent.mm:tools")

    @staticmethod
    def gotoAppView(driver):
        driver.switch_to.context("NATIVE_APP")

    @staticmethod
    def public_driver_findElement(driver, ByType, value):
        try:
            WebDriverWait(driver, 10, 1).until(EC.presence_of_element_located((ByType, value)))
        except:
            pass
        finally:
            time.sleep(timeSleep)
            return driver.find_element(ByType, value)

    @staticmethod
    def public_driver_findElements(driver, ByType, value):
        try:
            WebDriverWait(driver, 10, 1).until(EC.presence_of_element_located((ByType, value)))
        except:
            pass
        finally:
            time.sleep(timeSleep)
            return driver.find_elements(ByType, value)

    @staticmethod
    def public_element_findElement(driver, element, ByType, value):
        try:
            WebDriverWait(driver, 10, 1).until(EC.presence_of_element_located((ByType, value)))
        except:
            pass
        finally:
            time.sleep(timeSleep)
            return element.find_element(ByType, value)

    @staticmethod
    def public_element_findElements(driver, element, ByType, value):
        try:
            WebDriverWait(driver, 10, 1).until(EC.presence_of_element_located((ByType, value)))
        except:
            pass
        finally:
            time.sleep(timeSleep)
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
