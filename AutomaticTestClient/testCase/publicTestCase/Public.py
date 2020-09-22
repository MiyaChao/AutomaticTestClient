import demjson
import unittest
from operate.AppiumOperate import appiumOperate
from operate.MySqlOperate import mySqlOperate
from operate.RequestOperate import HttpSession
from operate.SeleniumOperate import seleniumOperate
from method.PublicMethod import publicMethod, drivers
from script.ZZ1597398638108.XM1597398638108 import CustomScript as XM1597398638108
from script.ZZ1597398638108.XM1598933605509 import CustomScript as XM1598933605509
from script.ZZ1597398638108.XM1598949386052 import CustomScript as XM1598949386052
from script.ZZ1597398638108.XM1598951424223 import CustomScript as XM1598951424223
from script.ZZ1597398638108.XM1599033173247 import CustomScript as XM1599033173247


def switchBrowser(browserNo):
    if browserNo == "1":
        drivers.driver = drivers.seleniumDriver
    elif browserNo == "2":
        drivers.driver = drivers.seleniumDriver_2


def getParam(paramDataDict, name):
    if name in paramDataDict:
        return paramDataDict[name]
    else:
        raise Exception("片段参数中不存在参数：" + name + "\n")


def setParam(paramDataDict, name, value):
    paramDataDict[name] = value


def getActualValue(valueAccessMethod, value, paramDataDict, actionJson):
    result = None
    if valueAccessMethod == "getGlobalVariable":
        result = publicMethod.getGlobalVariable(value)
    elif valueAccessMethod == "getParam":
        result = getParam(paramDataDict, value)
    elif valueAccessMethod == "getCustom":
        actualValueType = actionJson["actualValueType"]
        result = publicMethod.convertType(value, actualValueType)
    return result


def getExpectedValue(valueAccessMethod, value, paramDataDict, actionJson):
    result = None
    if valueAccessMethod == "getGlobalVariable":
        result = publicMethod.getGlobalVariable(value)
    elif valueAccessMethod == "getParam":
        result = getParam(paramDataDict, value)
    elif valueAccessMethod == "getCustom":
        actualValueType = actionJson["expectedValueType"]
        result = publicMethod.convertType(value, actualValueType)
    return result


def uiAction(actionData, paramDataDict, uiActionType):
    if uiActionType == "selenium":
        uiOperate = seleniumOperate
    elif uiActionType == "appium":
        uiOperate = appiumOperate
    print("=======actionData========")
    print(actionData)
    actionKey = actionData["actionKey"]
    actionJson = demjson.decode(actionData["actionJson"])
    if actionKey == "openBrowser":
        print("<b><-----执行openBrowser操作-----></b>")
        browserType = actionJson["browserType"]
        browserNo = actionJson["browserNo"]
        runMode = actionJson["runMode"]
        print("打开" + browserType + "，编号为：" + browserNo + "，模式为" + runMode)
        uiOperate.openBrowser(browserType, browserNo, runMode)
    elif actionKey == "get":
        print("<b><-----执行get操作-----></b>")
        browserNo = actionJson["driverNo"]
        urlAccessMethod = actionJson["urlAccessMethod"]
        urlValue = actionJson["urlValue"]
        url = ""
        if urlAccessMethod == "getParam":
            print("从参数中获取url，参数名：" + urlValue)
            url = getParam(paramDataDict, urlValue)
        elif urlAccessMethod == "getGlobalVariable":
            print("从全局变量中获取url，变量名：" + urlValue)
            url = publicMethod.getGlobalVariable(urlValue)
        elif urlAccessMethod == "getCustom":
            print("自定义url")
            url = urlValue
        if not isinstance(url, str):
            raise Exception("url必须为字符串\n")
        print("url：" + url)
        print("浏览器编号：" + browserNo)
        switchBrowser(browserNo)
        uiOperate.getUrl(drivers.driver, url)
    elif actionKey == "quitBrowser":
        print("<b><-----执行quitBrowser操作-----></b>")
        browserNo = actionJson["browserNo"]
        print("浏览器编号：" + browserNo)
        switchBrowser(browserNo)
        uiOperate.quitBrowser(drivers.driver)
    elif actionKey == "getCurrentUrl":
        print("<b><-----执行getCurrentUrl操作-----></b>")
        browserNo = actionJson["driverNo"]
        print("浏览器编号：" + browserNo)
        resultStorageMethod = actionJson["resultStorageMethod"]
        resultStorageValue = actionJson["resultStorageValue"]
        switchBrowser(browserNo)
        url = uiOperate.getCurrentUrl(drivers.driver)
        if resultStorageMethod == "setGlobalVariable":
            print("存储为全局变量：" + resultStorageValue + "，url：" + url)
            publicMethod.globalVariableDict[resultStorageValue] = url
    elif actionKey == "click":
        print("<b><-----执行click操作-----></b>")
        browserNo = actionJson["driverNo"]
        print("浏览器编号：" + browserNo)
        switchBrowser(browserNo)
        elementAccessMethod = actionJson["elementAccessMethod"]
        element = None
        if elementAccessMethod == "getElement":
            elementId = actionJson["elementId"]
            element = seleniumOperate.queryElement(elementId)
        elif elementAccessMethod == "getGlobalVariable":
            variableName = actionJson["variableName"]
            element = publicMethod.getGlobalVariable(variableName)
        if isinstance(element, list):
            raise Exception("执行click操作的元素信息不能是list类型\n")
        uiOperate.public_element_click(drivers.driver, element)
    elif actionKey == "sendKeys":
        print("<b><-----执行sendKeys操作-----></b>")
        browserNo = actionJson["driverNo"]
        print("浏览器编号：" + browserNo)
        switchBrowser(browserNo)
        elementAccessMethod = actionJson["elementAccessMethod"]
        element = None
        if elementAccessMethod == "getElement":
            elementId = actionJson["elementId"]
            element = seleniumOperate.queryElement(elementId)
        elif elementAccessMethod == "getGlobalVariable":
            variableName = actionJson["variableName"]
            element = publicMethod.getGlobalVariable(variableName)
        if isinstance(element, list):
            raise Exception("执行sendKeys操作的元素信息不能是list类型\n")
        sendKeyValueAccessMethod = actionJson["sendKeyValueAccessMethod"]
        inputContent = ""
        sendKeyValue = actionJson["sendKeyValue"]
        if sendKeyValueAccessMethod == "getParam":
            print("从参数中获取inputContent，参数名：" + sendKeyValue)
            inputContent = getParam(paramDataDict, sendKeyValue)
        elif sendKeyValueAccessMethod == "getGlobalVariable":
            print("从全局变量中获取inputContent，变量名：" + sendKeyValue)
            inputContent = publicMethod.getGlobalVariable(sendKeyValue)
        elif sendKeyValueAccessMethod == "getCustom":
            print("自定义inputContent")
            inputContent = sendKeyValue
        if not isinstance(inputContent, str):
            raise Exception("inputContent必须为字符串\n")
        uiOperate.public_element_sendKeys(drivers.driver, element, inputContent)
    elif actionKey == "clear":
        print("<b><-----执行clear操作-----></b>")
        browserNo = actionJson["driverNo"]
        print("浏览器编号：" + browserNo)
        switchBrowser(browserNo)
        elementAccessMethod = actionJson["elementAccessMethod"]
        element = None
        if elementAccessMethod == "getElement":
            elementId = actionJson["elementId"]
            element = seleniumOperate.queryElement(elementId)
        elif elementAccessMethod == "getGlobalVariable":
            variableName = actionJson["variableName"]
            element = publicMethod.getGlobalVariable(variableName)
        if isinstance(element, list):
            raise Exception("执行clear操作的元素信息不能是list类型\n")
        uiOperate.public_element_clear(drivers.driver, element)
    elif actionKey == "getAttribute":
        print("<b><-----执行getAttribute操作操作-----></b>")
        browserNo = actionJson["driverNo"]
        print("浏览器编号：" + browserNo)
        switchBrowser(browserNo)
        elementAccessMethod = actionJson["elementAccessMethod"]
        element = None
        if elementAccessMethod == "getElement":
            elementId = actionJson["elementId"]
            element = seleniumOperate.queryElement(elementId)
        elif elementAccessMethod == "getGlobalVariable":
            variableName = actionJson["variableName"]
            element = publicMethod.getGlobalVariable(variableName)
        if isinstance(element, list):
            raise Exception("执行getAttribute操作的元素信息不能是list类型\n")
        attributeName = actionJson["attributeName"]
        attributeValue = uiOperate.public_element_getAttribute(drivers.driver, element, attributeName)
        resultStorageMethod = actionJson["resultStorageMethod"]
        resultStorageValue = actionJson["resultStorageValue"]
        if resultStorageMethod == "setGlobalVariable":
            print("存储为全局变量：" + resultStorageValue + "，attributeValue：" + attributeValue)
            publicMethod.globalVariableDict[resultStorageValue] = attributeValue
    elif actionKey == "setElementAsVariable":
        print("<b><-----执行setElementAsVariable操作-----></b>")
        elementAccessMethod = actionJson["elementAccessMethod"]
        element = None
        if elementAccessMethod == "getElement":
            elementId = actionJson["elementId"]
            element = seleniumOperate.queryElement(elementId)
        elif elementAccessMethod == "getGlobalVariable":
            variableName = actionJson["variableName"]
            element = publicMethod.getGlobalVariable(variableName)
        resultStorageMethod = actionJson["resultStorageMethod"]
        resultStorageValue = actionJson["resultStorageValue"]
        if resultStorageMethod == "setGlobalVariable":
            print("存储为全局变量：" + resultStorageValue + "，elementId：" + elementId)
            publicMethod.globalVariableDict[resultStorageValue] = element


def public(actionData, paramDataDict):
    print("=======actionData========")
    print(actionData)
    actionJson = demjson.decode(actionData["actionJson"])
    actionKey = actionData["actionKey"]
    if actionKey == "defineVariables":
        print("<b><-----执行defineVariables操作-----></b>")
        value = ""
        variableValueType = actionJson["variableValueType"]
        variableValue = actionJson["variableValue"]
        value = publicMethod.convertType(variableValue, variableValueType)
        variableStorageMethod = actionJson["variableStorageMethod"]
        variableStorageValue = actionJson["variableStorageValue"]
        if variableStorageMethod == "setGlobalVariable":
            try:
                print("定义变量为全局变量，变量名：" + variableStorageValue + "，值：" + str(value))
            except:
                pass
            publicMethod.setGlobalVariable(variableStorageValue, value)
    elif actionKey == "if" or actionKey == "while":
        if actionKey == "if":
            print("<b><-----执行if操作-----></b>")
        elif actionKey == "while":
            print("<b><-----执行while操作-----></b>")
        while 1 == 1:
            actualValueAccessMethod = actionJson["actualValueAccessMethod"]
            actualValue = actionJson["actualValue"]
            actual = getActualValue(actualValueAccessMethod, actualValue, paramDataDict, actionJson)
            expectedValueAccessMethod = actionJson["expectedValueAccessMethod"]
            expectedValue = actionJson["expectedValue"]
            expected = getExpectedValue(expectedValueAccessMethod, expectedValue, paramDataDict, actionJson)
            condition = actionJson["condition"]
            try:
                print("进行逻辑判断，actual：" + str(actual) + "，condition：" + condition + "，expected：" + str(expected))
            except:
                pass
            result = 0
            if condition == "=":
                if actual == expected:
                    result = 1
            elif condition == ">":
                if actual > expected:
                    result = 1
            elif condition == "<":
                if actual < expected:
                    result = 1
            elif condition == "<=":
                if actual <= expected:
                    result = 1
            elif condition == ">=":
                if actual >= expected:
                    result = 1
            elif condition == "in":
                if actual in expected:
                    result = 1
            if result == 1:
                fragmentTemplateStepsSql = "select * from fragment_template_step where id = %s and parentId = %s order by sequence asc"
                fragmentTemplateStepsParams = [publicMethod.currentTemplateId, actionData["id"]]
                fragmentTemplateSteps = mySqlOperate.search(fragmentTemplateStepsSql, fragmentTemplateStepsParams)
                if not (fragmentTemplateSteps is None):
                    templateStepList = []
                    for fragmentTemplateStep in fragmentTemplateSteps:
                        dictionary = {}
                        dictionary["id"] = fragmentTemplateStep[0]
                        dictionary["stepName"] = fragmentTemplateStep[1]
                        dictionary["actionType"] = fragmentTemplateStep[2]
                        dictionary["actionKey"] = fragmentTemplateStep[3]
                        dictionary["actionJson"] = fragmentTemplateStep[4]
                        dictionary["sequence"] = fragmentTemplateStep[5]
                        dictionary["parentId"] = fragmentTemplateStep[6]
                        templateStepList.append(dictionary)
                print("开始执行" + actionData["id"] + "步骤的子级步骤")
                for step in templateStepList:
                    if step["parentId"] == actionData["id"]:
                        stepType = step["actionType"]
                        if stepType == "selenium":
                            uiAction(step, paramDataDict, "selenium")
                        elif stepType == "appium":
                            uiAction(step, paramDataDict, "appium")
                        elif stepType == "public":
                            public(step, paramDataDict)
                        elif stepType == "assert":
                            publicAssert(step, paramDataDict)
                        elif stepType == "request":
                            request(step, paramDataDict)
                        elif stepType == "custom":
                            custom(actionData, paramDataDict)
                        else:
                            raise Exception("actionType错误，actionType：" + stepType + "\n")
            elif result == 0:
                if actionKey == "if":
                    print("条件不符，不执行if步骤下的子步骤")
                elif actionKey == "while":
                    print("条件不符，跳出while循环")
                break
            if actionKey == "if":
                break
    elif actionKey == "for":
        print("<b><-----执行for操作-----></b>")
        dataListAccessMethod = actionJson["dataListAccessMethod"]
        dataListValue = actionJson["dataListValue"]
        dataList = None
        if dataListAccessMethod == "getParam":
            dataList = getParam(paramDataDict, dataListValue)
        elif dataListAccessMethod == "getGlobalVariable":
            dataList = publicMethod.getGlobalVariable(dataListValue)
        elif dataListAccessMethod == "getCustom":
            dataList = dataListValue
        try:
            print("循环列表/字符串为：" + str(dataList))
        except:
            pass
        fragmentTemplateStepsSql = "select * from fragment_template_step where id = %s and parentId = %s order by sequence asc"
        fragmentTemplateStepsParams = [publicMethod.currentTemplateId, actionData["id"]]
        fragmentTemplateSteps = mySqlOperate.search(fragmentTemplateStepsSql, fragmentTemplateStepsParams)
        if not (fragmentTemplateSteps is None):
            templateStepList = []
            for fragmentTemplateStep in fragmentTemplateSteps:
                dictionary = {}
                dictionary["id"] = fragmentTemplateStep[0]
                dictionary["stepName"] = fragmentTemplateStep[1]
                dictionary["actionType"] = fragmentTemplateStep[2]
                dictionary["actionKey"] = fragmentTemplateStep[3]
                dictionary["actionJson"] = fragmentTemplateStep[4]
                dictionary["sequence"] = fragmentTemplateStep[5]
                dictionary["parentId"] = fragmentTemplateStep[6]
                templateStepList.append(dictionary)
        for data in dataList:
            if "dataStorageMethod" in actionJson:
                if "dataStorageValue" in actionJson:
                    dataStorageMethod = actionJson["dataStorageMethod"]
                    dataStorageValue = actionJson["dataStorageValue"]
                    if dataStorageMethod == "setGlobalVariable":
                        print("将data设置为全局变量：" + dataStorageValue)
                        publicMethod.setGlobalVariable(dataStorageValue, data)
                else:
                    raise Exception("resultStorageValue不存在\n")
            else:
                raise Exception("resultStorageMethod不存在\n")
            print("开始执行" + actionData["id"] + "步骤的子级步骤")
            for step in templateStepList:
                if step["parentId"] == actionData["id"]:
                    stepType = step["actionType"]
                    if stepType == "selenium":
                        uiAction(step, paramDataDict, "selenium")
                    elif stepType == "appium":
                        uiAction(step, paramDataDict, "appium")
                    elif stepType == "public":
                        public(step, paramDataDict)
                    elif stepType == "assert":
                        publicAssert(step, paramDataDict)
                    elif stepType == "request":
                        request(step, paramDataDict)
                    else:
                        raise Exception("actionType错误，actionType：" + stepType + "\n")
    elif actionKey == "arithmetic":
        print("<b><-----执行arithmetic操作-----></b>")
        num_1_AccessMethod = actionJson["num_1_AccessMethod"]
        num_1_Value = actionJson["num_1_Value"]
        num1 = None
        if num_1_AccessMethod == "getParam":
            num1 = getParam(paramDataDict, num_1_Value)
        elif num_1_AccessMethod == "getGlobalVariable":
            num1 = publicMethod.getGlobalVariable(num_1_Value)
        elif num_1_AccessMethod == "getCustom":
            num1 = publicMethod.convertType(num_1_Value, "float")
        condition = actionJson["condition"]
        num_2_AccessMethod = actionJson["num_2_AccessMethod"]
        num_2_Value = actionJson["num_2_Value"]
        num2 = None
        if num_2_AccessMethod == "getParam":
            num2 = getParam(paramDataDict, num_2_Value)
        elif num_2_AccessMethod == "getGlobalVariable":
            num2 = publicMethod.getGlobalVariable(num_2_Value)
        elif num_2_AccessMethod == "getCustom":
            num2 = publicMethod.convertType(num_2_Value, "float")
        result = None
        num1 = publicMethod.convertType(num1, "float")
        print("算数1：" + str(num1))
        num2 = publicMethod.convertType(num2, "float")
        print("算数2：" + str(num2))
        if condition == "+":
            print("执行加法运算")
            result = num1 + num2
        elif condition == "-":
            print("执行减法运算")
            result = num1 - num2
        elif condition == "*":
            print("执行乘法运算")
            result = num1 * num2
        elif condition == "/":
            print("执行除法运算")
            result = num1 / num2
        print("运算结果：" + str(result))
        if "resultStorageMethod" in actionJson:
            if "resultStorageValue" in actionJson:
                resultStorageMethod = actionJson["resultStorageMethod"]
                resultStorageValue = actionJson["resultStorageValue"]
                if resultStorageMethod == "setGlobalVariable":
                    print("将运算结果设置为全局变量：" + resultStorageValue)
                    publicMethod.setGlobalVariable(resultStorageValue, result)
            else:
                raise Exception("resultStorageValue不存在\n")
        else:
            raise Exception("resultStorageMethod不存在\n")
    elif actionKey == "list_append":
        print("<b><-----执行list_append操作-----></b>")
        listAccessMethod = actionJson["listAccessMethod"]
        listName = actionJson["listName"]
        list_1 = []
        print("list获取方式：" + listAccessMethod)
        print("list名称：" + listName)
        if listAccessMethod == "getParam":
            list_1 = getParam(paramDataDict, listName)
        elif listAccessMethod == "getGlobalVariable":
            list_1 = publicMethod.getGlobalVariable(listName)
        appendValueAccessMethod = actionJson["appendValueAccessMethod"]
        appendValue = actionJson["appendValue"]
        print("追加值获取方式：" + appendValueAccessMethod)
        value = None
        if appendValueAccessMethod == "getParam":
            value = getParam(paramDataDict, appendValue)
        elif appendValueAccessMethod == "getGlobalVariable":
            value = publicMethod.getGlobalVariable(appendValue)
        elif appendValueAccessMethod == "getCustom":
            appendValueType = actionJson["appendValueType"]
            print("追加值类型：" + appendValueType)
            value = publicMethod.convertType(appendValue, appendValueType)
        try:
            print("追加值：" + str(value))
        except:
            pass
        list_1.append(value)
        if listAccessMethod == "getParam":
            setParam(paramDataDict, listName, list_1)
        elif listAccessMethod == "getGlobalVariable":
            publicMethod.setGlobalVariable(listName, list_1)
    elif actionKey == "dict_update":
        print("<b><-----执行dict_update操作-----></b>")
        dictAccessMethod = actionJson["dictAccessMethod"]
        dictName = actionJson["dictName"]
        print("dict获取方式：" + dictAccessMethod)
        print("dict名称：" + dictName)
        dict_1 = None
        if dictAccessMethod == "getParam":
            dict_1 = getParam(paramDataDict, dictName)
        elif dictAccessMethod == "getGlobalVariable":
            dict_1 = publicMethod.getGlobalVariable(dictName)
        dictKey = actionJson["dictKey"]
        valueAccessMethod = actionJson["valueAccessMethod"]
        dictValue = actionJson["dictValue"]
        print("追加值获取方式：" + valueAccessMethod)
        value = None
        if valueAccessMethod == "getParam":
            value = getParam(paramDataDict, dictValue)
        elif valueAccessMethod == "getGlobalVariable":
            value = publicMethod.getGlobalVariable(dictValue)
        elif valueAccessMethod == "getCustom":
            dictValueType = actionJson["dictValueType"]
            print("追加值类型：" + dictValueType)
            value = publicMethod.convertType(dictValue, dictValueType)
        try:
            print("追加Key：" + str(dictKey) + "，追加Value：" + str(value))
        except:
            pass
        dict_1[dictKey] = value
        if dictAccessMethod == "getParam":
            setParam(paramDataDict, dictName, dict_1)
        elif dictAccessMethod == "getGlobalVariable":
            publicMethod.setGlobalVariable(dictName, dict_1)
    elif actionKey == "getListValue":
        print("<b><-----执行getListValue操作-----></b>")
        listAccessMethod = actionJson["listAccessMethod"]
        listName = actionJson["listName"]
        list_1 = []
        print("list获取方式：" + listAccessMethod)
        print("list名称：" + listName)
        if listAccessMethod == "getParam":
            list_1 = getParam(paramDataDict, listName)
        elif listAccessMethod == "getGlobalVariable":
            list_1 = publicMethod.getGlobalVariable(listName)
        sequence = actionJson["sequence"]
        print("取第" + str(sequence) + "个的值")
        result = list_1[int(sequence)]
        try:
            print("result：" + str(result))
        except:
            pass
        if "resultStorageMethod" in actionJson:
            if "resultStorageValue" in actionJson:
                resultStorageMethod = actionJson["resultStorageMethod"]
                resultStorageValue = actionJson["resultStorageValue"]
                if resultStorageMethod == "setGlobalVariable":
                    print("将结果设置为全局变量：" + resultStorageValue)
                    publicMethod.setGlobalVariable(resultStorageValue, result)
            else:
                raise Exception("resultStorageValue不存在\n")
        else:
            raise Exception("resultStorageMethod不存在\n")
    elif actionKey == "getDictValue":
        print("<b><-----执行getDictValue操作-----></b>")
        dictAccessMethod = actionJson["dictAccessMethod"]
        dictName = actionJson["dictName"]
        print("dict获取方式：" + dictAccessMethod)
        print("dict名称：" + dictName)
        dict_1 = None
        if dictAccessMethod == "getParam":
            dict_1 = getParam(paramDataDict, dictName)
        elif dictAccessMethod == "getGlobalVariable":
            dict_1 = publicMethod.getGlobalVariable(dictName)
        dictKey = actionJson["key"]
        print("取关键字为'" + str(dictKey) + "'的值")
        result = dict_1[dictKey]
        try:
            print("result：" + str(result))
        except:
            pass
        if "resultStorageMethod" in actionJson:
            if "resultStorageValue" in actionJson:
                resultStorageMethod = actionJson["resultStorageMethod"]
                resultStorageValue = actionJson["resultStorageValue"]
                if resultStorageMethod == "setGlobalVariable":
                    print("将结果设置为全局变量：" + resultStorageValue)
                    publicMethod.setGlobalVariable(resultStorageValue, result)
            else:
                raise Exception("resultStorageValue不存在\n")
        else:
            raise Exception("resultStorageMethod不存在\n")


def publicAssert(actionData, paramDataDict):
    print("=======actionData========")
    print(actionData)
    actionJson = demjson.decode(actionData["actionJson"])
    print("<b><-----执行assert操作-----></b>")
    actualValueAccessMethod = actionJson["actualValueAccessMethod"]
    actualValue = actionJson["actualValue"]
    actual = None
    if actualValueAccessMethod == "getGlobalVariable":
        actual = publicMethod.getGlobalVariable(actualValue)
    expectedValueAccessMethod = actionJson["expectedValueAccessMethod"]
    expectedValue = actionJson["expectedValue"]
    expect = None
    if expectedValueAccessMethod == "getCustom":
        expectedValueType = actionJson["expectedValueType"]
        expect = publicMethod.convertType(expectedValue, expectedValueType)
    elif expectedValueAccessMethod == "getParam":
        expect = getParam(paramDataDict, expectedValue)
    elif expectedValueAccessMethod == "getGlobalVariable":
        expect = publicMethod.getGlobalVariable(expectedValue)
    print("实际值：" + str(actual))
    print("期望值：" + str(expect))
    assert actual == expect, actionData["stepName"]


def request(actionData, paramDataDict):
    print("=======actionData========")
    print(actionData)
    actionJson = demjson.decode(actionData["actionJson"])
    print("<b><-----执行request操作-----></b>")
    domainNameAccessMethod = None
    if "domainNameAccessMethod" in actionJson:
        domainNameAccessMethod = actionJson["domainNameAccessMethod"]
    else:
        raise Exception("domainNameAccessMethod不存在\n")
    domain = ""
    if "domainNameValue" in actionJson:
        if domainNameAccessMethod == "getCustom":
            domain = actionJson["domainNameValue"]
        elif domainNameAccessMethod == "getEnvironmentVariable":
            domain = publicMethod.getEnvironmentVariable(actionJson["domainNameValue"])
        elif domainNameAccessMethod == "getGlobalVariable":
            domain = publicMethod.getGlobalVariable(actionJson["domainNameValue"])
    else:
        raise Exception("domainNameValue不存在\n")
    urlValue = ""
    if "urlValue" in actionJson:
        urlValue = actionJson["urlValue"]
    else:
        raise Exception("urlValue不存在\n")
    url = domain + urlValue
    method = None
    if "actionKey" in actionData:
        method = actionData["actionKey"]
    else:
        raise Exception("actionKey不存在\n")
    http = HttpSession()
    headers = None
    if "headersValueAccessMethod" in actionJson:
        if "headersValue" in actionJson:
            headersValueAccessMethod = actionJson["headersValueAccessMethod"]
            if headersValueAccessMethod == "getGlobalVariable":
                headers = publicMethod.getGlobalVariable(actionJson["headersValue"])
            elif headersValueAccessMethod == "getEnvironmentVariable":
                headers = publicMethod.getEnvironmentVariable(actionJson["headersValue"])
            elif headersValueAccessMethod == "getParam":
                headers = getParam(paramDataDict, actionJson["headersValue"])
            elif headersValueAccessMethod == "getCustom":
                headers = demjson.decode(actionJson["headersValue"])
            if not (headers is None):
                if not isinstance(headers, dict):
                    raise Exception("headers必须为字典\n")
    cookies = None
    if "cookiesValueAccessMethod" in actionJson:
        if "cookiesValue" in actionJson:
            cookiesValueAccessMethod = actionJson["cookiesValueAccessMethod"]
            if cookiesValueAccessMethod == "getGlobalVariable":
                cookies = publicMethod.getGlobalVariable(actionJson["cookiesValue"])
            elif cookiesValueAccessMethod == "getEnvironmentVariable":
                cookies = publicMethod.getEnvironmentVariable(actionJson["cookiesValue"])
            elif cookiesValueAccessMethod == "getParam":
                cookies = getParam(paramDataDict, actionJson["cookiesValue"])
            elif cookiesValueAccessMethod == "getCustom":
                cookies = demjson.decode(actionJson["cookiesValue"])
            if not (cookies is None):
                if not isinstance(cookies, dict):
                    raise Exception("cookies必须为字典\n")
    data = None
    if "dataValueAccessMethod" in actionJson:
        if "dataValue" in actionJson:
            dataValueAccessMethod = actionJson["dataValueAccessMethod"]
            if dataValueAccessMethod == "getGlobalVariable":
                data = publicMethod.getGlobalVariable(actionJson["dataValue"])
            elif dataValueAccessMethod == "getEnvironmentVariable":
                data = publicMethod.getEnvironmentVariable(actionJson["dataValue"])
            elif dataValueAccessMethod == "getParam":
                data = getParam(paramDataDict, actionJson["dataValue"])
            elif dataValueAccessMethod == "getCustom":
                data = demjson.decode(actionJson["dataValue"])
            if not (data is None):
                if not isinstance(data, dict):
                    raise Exception("data必须为字典\n")
    json = None
    if "jsonValueAccessMethod" in actionJson:
        if "jsonValue" in actionJson:
            jsonValueAccessMethod = actionJson["jsonValueAccessMethod"]
            if jsonValueAccessMethod == "getGlobalVariable":
                json = publicMethod.getGlobalVariable(actionJson["jsonValue"])
            elif jsonValueAccessMethod == "getEnvironmentVariable":
                json = publicMethod.getEnvironmentVariable(actionJson["jsonValue"])
            elif jsonValueAccessMethod == "getParam":
                json = getParam(paramDataDict, actionJson["jsonValue"])
            elif jsonValueAccessMethod == "getCustom":
                json = demjson.decode(actionJson["jsonValue"])
            if not (json is None):
                if not isinstance(json, dict):
                    raise Exception("json必须为字典\n")
    files = None
    if "fileValueAccessMethod" in actionJson:
        if "fileValue" in actionJson:
            if dataValueAccessMethod == "getParam":
                files = getParam(paramDataDict, actionJson["fileValue"])
    result = http.request(method=method, url=url, data=data, json=json, headers=headers, cookies=cookies, files=files)
    if "resultStorageMethod" in actionJson:
        if "resultStorageValue" in actionJson:
            resultStorageMethod = actionJson["resultStorageMethod"]
            resultStorageValue = actionJson["resultStorageValue"]
            if resultStorageMethod == "setGlobalVariable":
                try:
                    print("将结果设置为全局变量：" + resultStorageValue)
                    publicMethod.setGlobalVariable(resultStorageValue, result.json())
                except:
                    pass
    try:
        print("返回结果为：" + str(result.json()))
    except:
        pass
    if "resultCookiesStorageMethod" in actionJson:
        if "resultCookiesStorageValue" in actionJson:
            resultCookiesStorageMethod = actionJson["resultCookiesStorageMethod"]
            resultCookiesStorageValue = actionJson["resultCookiesStorageValue"]
            if resultCookiesStorageMethod == "setGlobalVariable":
                try:
                    print("将结果Cookies设置为全局变量：" + resultCookiesStorageValue)
                    publicMethod.setGlobalVariable(resultCookiesStorageValue, result.cookies)
                except:
                    pass
    try:
        print("返回结果Cookies为：" + str(result.cookies.items()))
    except:
        pass


def custom(actionData, paramDataDict):
    print("=======actionData========")
    print(actionData)
    actionJson = demjson.decode(actionData["actionJson"])
    print("<b><-----执行custom方法-----></b>")
    methodName = actionJson["methodName"]
    if publicMethod.projectId == "XM1597398638108":
        result = XM1597398638108.run(methodName, paramDataDict)
    elif publicMethod.projectId == "XM1598933605509":
        result = XM1598933605509.run(methodName, paramDataDict)
    elif publicMethod.projectId == "XM1598949386052":
        result = XM1598949386052.run(methodName, paramDataDict)
    elif publicMethod.projectId == "XM1598951424223":
        result = XM1598951424223.run(methodName, paramDataDict)
    elif publicMethod.projectId == "XM1599033173247":
        result = XM1599033173247.run(methodName, paramDataDict)
    if "resultStorageMethod" in actionJson:
        if "resultStorageValue" in actionJson:
            resultStorageMethod = actionJson["resultStorageMethod"]
            resultStorageValue = actionJson["resultStorageValue"]
            if resultStorageMethod == "setGlobalVariable":
                print("将结果设置为全局变量：" + resultStorageValue)
                publicMethod.setGlobalVariable(resultStorageValue, result)
            try:
                print("返回结果为：" + str(result))
            except:
                pass
        else:
            raise Exception("resultStorageValue不存在\n")
    else:
        raise Exception("resultStorageMethod不存在\n")


class publicTestCase(unittest.TestCase):
    # 当前测试片段执行结果
    fragmentResult = 0
    # 记录执行到了第几个测试用例
    caseNum = 0
    # 记录执行到了测试用例的第几个测试片段
    fragmentNum = 0
    # 记录执行到了测试用例的有几个测试片段
    caseStepNum = 0
    # 记录执行当前正在执行的测试用例的执行结果
    currentCaseResult = 1

    def setUp(self):
        # 该class内每个用例开始前执行
        publicMethod.setUp()

    def tearDown(self):
        # 该class内每个用例结束后执行
        publicMethod.tearDown()
        # 检测该用例是否还有测试片段未执行
        if publicTestCase.caseStepNum > publicTestCase.fragmentNum:
            # 记录执行当前正在执行的测试用例的执行结果
            if publicTestCase.fragmentResult == 0:
                publicTestCase.currentCaseResult = 0
        publicTestCase.fragmentNum = publicTestCase.fragmentNum + 1
        # 检测该用例是否还有测试片段未执行（caseStepNum等于fragmentNum则代表，该用例所有步骤都已经执行完毕）
        if publicTestCase.caseStepNum == publicTestCase.fragmentNum:
            # caseNum + 1，执行下一个测试用例
            publicTestCase.caseNum = publicTestCase.caseNum + 1
            # 将当前测试用例的执行结果记录起来
            publicMethod.runCaseResultList.append(publicTestCase.currentCaseResult)
            # 重置当前执行到第几个测试片段记录
            publicTestCase.fragmentNum = 0
            publicTestCase.currentCaseResult = 1
        # 重置当前执行到当前测试片段执行结果
        publicTestCase.fragmentResult = 0
        # 判断还有没有测试用例要执行（caseNum等于caseIdList的长度，用例已经全部执行完毕）
        if publicTestCase.caseNum == len(publicMethod.caseIdList):
            # 用例已经全部执行完毕，重置caseNum和fragmentNum
            publicTestCase.caseNum = 0
            publicTestCase.fragmentNum = 0
            publicTestCase.currentCaseResult = 1

    @staticmethod
    def test_public():
        """公用测试用例"""
        # 打印当前用例数据到报告中
        print(publicMethod.casesDataDict)
        # 打印当前环境变量数据到报告中
        print("=======environmentVariableDict========")
        print(publicMethod.environmentVariableDict)
        # 读取执行任务时需要用到的数据
        caseId = publicMethod.caseIdList[publicTestCase.caseNum]
        caseName = publicMethod.casesDataDict[caseId]["caseName"]
        publicTestCase.caseStepNum = len(publicMethod.casesDataDict[caseId]["caseData"])
        fragmentId = publicMethod.casesDataDict[caseId]["caseData"][publicTestCase.fragmentNum]["fragmentId"]
        fragmentName = publicMethod.casesDataDict[caseId]["caseData"][publicTestCase.fragmentNum]["fragmentName"]
        fragmentParamDict = publicMethod.casesDataDict[caseId]["caseData"][publicTestCase.fragmentNum]["fragmentParamDict"]
        templateId = publicMethod.casesDataDict[caseId]["caseData"][publicTestCase.fragmentNum]["fragmentTemplateId"]
        templateStepList = publicMethod.casesDataDict[caseId]["caseData"][publicTestCase.fragmentNum]["templateStepList"]
        # 设置当前执行的任务信息（生成测试报告时需要使用）
        publicMethod.currentCaseName = caseName
        publicMethod.currentFragmentId = fragmentId
        publicMethod.currentFragmentName = fragmentName
        publicMethod.currentTemplateId = templateId
        # 打印当前片段参数数据到报告中
        print("=======paramDataDict========")
        print(fragmentParamDict)
        # 遍历当前片段步骤一步一步执行
        for templateStep in templateStepList:
            actionType = templateStep["actionType"]
            if actionType == "selenium":
                uiAction(templateStep, fragmentParamDict, "selenium")
            elif actionType == "appium":
                uiAction(templateStep, fragmentParamDict, "appium")
            elif actionType == "public":
                public(templateStep, fragmentParamDict)
            elif actionType == "assert":
                publicAssert(templateStep, fragmentParamDict)
            elif actionType == "request":
                request(templateStep, fragmentParamDict)
            elif actionType == "custom":
                custom(templateStep, fragmentParamDict)
            else:
                raise Exception("actionType错误，actionType：" + actionType + "\n")
        # 执行到这代表前面没有报错，测试结果正常
        publicTestCase.fragmentResult = 1
