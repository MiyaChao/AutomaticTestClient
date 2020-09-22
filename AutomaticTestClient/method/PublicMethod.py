import demjson


class drivers:
    driver = None
    seleniumDriver = None
    seleniumDriver_2 = None
    driver_2 = None
    appiumDriver = None
    appiumDriver_2 = None


class publicMethod:
    # 启动客户端的用户ID
    userId = None
    # 启动客户端的项目ID
    projectId = None
    # 启动客户端的模式
    modeId = None
    # 执行任务的用例id列表
    caseIdList = []
    # 执行任务的用例数据字典
    casesDataDict = {}
    # 当前正在执行的集合名称
    currentSuiteName = None
    # 当前正在执行的用例名称
    currentCaseName = None
    # 当前正在执行的片段ID
    currentFragmentId = None
    # 当前正在执行的片段名称
    currentFragmentName = None
    # 当前正在执行的片段模板ID
    currentTemplateId = None
    # 当前正在执行的片段步骤名称
    currentTemplateStepName = None
    # 当前正在执行的用例执行结果列表
    runCaseResultList = []
    # 全局变量字典
    globalVariableDict = {}
    # 环境变量字典
    environmentVariableDict = {}

    # 执行用例前执行，检测是否有需要设置的全局变量或cookie，有就进行设置
    @staticmethod
    def setUp():
        pass

    # 执行用例后执行，检测是否有需要设置的全局变量或cookie，有就进行设置
    @staticmethod
    def tearDown():
        pass

    # 检测字符串中是否只有数字
    @staticmethod
    def isNumber(string):
        numberList = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        for char in string:
            if char in numberList:
                continue
            else:
                return 0
        return 1

    # 设置全局变量
    @staticmethod
    def setGlobalVariable(name, value):
        publicMethod.globalVariableDict[name] = value

    # 获取某个全局变量
    @staticmethod
    def getGlobalVariable(name):
        if name in publicMethod.globalVariableDict:
            return publicMethod.globalVariableDict[name]
        else:
            raise Exception("全局变量中不存在变量："+name+"\n")

    # 获取全部全局变量
    @staticmethod
    def getGlobalVariableDict():
        return publicMethod.globalVariableDict

    # 获取环境变量
    @staticmethod
    def getEnvironmentVariable(name):
        if name in publicMethod.environmentVariableDict:
            return publicMethod.environmentVariableDict[name]
        else:
            raise Exception("环境变量中不存在变量：" + name + "\n")

    # 转换数据类型
    @staticmethod
    def convertType(value, valueType):
        result = None
        if valueType == "string":
            result = value
        elif valueType == "int":
            try:
                result = int(value)
            except:
                raise Exception("转换类型失败，内容\""+value+"\"不可转换为int类型\n")
        elif valueType == "float":
            try:
                result = float(value)
            except:
                raise Exception("转换类型失败，内容\""+value+"\"不可转换为float类型\n")
        elif valueType == "list":
            try:
                result = eval(value)
            except:
                raise Exception("转换类型失败，内容\""+value+"\"不可转换为list类型\n")
        elif valueType == "dict":
            try:
                result = demjson.decode(value)
            except:
                raise Exception("转换类型失败，内容\""+value+"\"不可转换为dict类型\n")
        elif valueType == "file":
            try:
                if not (isinstance(value, dict)):
                    value = demjson.decode(value)
                fileKey = value["fileKey"]
                value = value["value"]
                valueFragment = value.split(".", -1)
                fileType = ""
                if valueFragment[len(valueFragment) - 1] in ["jpg", "png"]:
                    fileType = "image/jpeg"
                elif valueFragment[len(valueFragment) - 1] in ["xlsx", "xls", "txt"]:
                    fileType = "application/vnd.ms-excel"
                pathFragment = value.split("\\", -1)
                file_data = {fileKey: (pathFragment[len(pathFragment) - 1], open(value, 'rb'), fileType)}
                result = file_data
            except:
                print("转换类型失败，内容不可转换为文件类型")
        return result
