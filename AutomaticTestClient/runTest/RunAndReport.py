import os
import time
import unittest
from BeautifulReport import BeautifulReport
from operate.MySqlOperate import mySqlOperate
from method.PublicMethod import publicMethod, drivers
from testCase.publicTestCase.Public import publicTestCase


def initializationData():
    # 初始化公用变量
    drivers.driver = None
    drivers.seleniumDriver = None
    drivers.seleniumDriver_2 = None
    drivers.driver_2 = None
    drivers.appiumDriver = None
    drivers.appiumDriver_2 = None
    publicMethod.globalVariableDict = {}
    publicMethod.environmentVariableDict = {}
    publicMethod.caseIdList = []
    publicMethod.casesDataDict = {}
    publicMethod.currentSuiteName = None
    publicMethod.currentCaseName = None
    publicMethod.currentFragmentId = None
    publicMethod.currentFragmentName = None
    publicMethod.currentTemplateId = None
    publicMethod.currentTemplateStepName = None
    publicMethod.runCaseResultList = []


def failed(reportId, code):
    if not (code in [0, 1, 2, 3]):
        runAndReport.lock = 1
    i = 0
    while i < 5:
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        failedSql = "UPDATE report SET status = %s, result = %s, updateTime = %s where id = %s"
        failedSqlParamList = [code, code, now, reportId]
        failedSqlResult = mySqlOperate.update(failedSql, failedSqlParamList)
        if failedSqlResult == 1:
            break
        i = i + 1
    if i == 5:
        raise Exception("failedSql执行失败")
    else:
        initializationData()


class runAndReport:
    # 任务等待了多少次（每隔sleepTime秒加1）
    waitNum = 0
    # 每隔多少秒检测一次是否有待执行任务
    sleepTime = 5
    # 任务准备工作锁，为1时任务准备工作的后续操作将不再进行
    lock = 0

    def checkTask(self, reportPath):
        while 1 == 1:
            # 检测是否有正在执行的任务
            runningTasksSql = ""
            runningTasksSqlParamList = []
            if publicMethod.modeId == "1":
                runningTasksSql = "select * from `report` where projectId = %s and status = %s and modeId = %s order by createTime asc"
                runningTasksSqlParamList = [publicMethod.projectId, 1, publicMethod.modeId]
            else:
                runningTasksSql = "select * from `report` where projectId = %s and status = %s  and modeId = %s  and userId = %s order by createTime asc"
                runningTasksSqlParamList = [publicMethod.projectId, 1, publicMethod.modeId, publicMethod.userId]
            runningTasks = mySqlOperate.search(runningTasksSql, runningTasksSqlParamList)
            if runningTasks is None:
                print("runningTaskSql执行失败")
                continue
            # 没有正在执行的任务则检测是否有需要执行的任务
            if len(runningTasks) > 0:
                self.waitNum = self.waitNum + 1
                if (self.waitNum * self.sleepTime) > 60:
                    print("任务执行超时")
                    failed(runningTasks[0][0], 3)
                    self.waitNum = 0
            else:
                # 检测是否有需要执行的任务
                toDoTasksSql = ""
                toDoTasksSqlParamList = []
                if publicMethod.modeId == "1":
                    toDoTasksSql = "select * from `report` where projectId = %s and status = %s and modeId = %s order by createTime asc"
                    toDoTasksSqlParamList = [publicMethod.projectId, 0, publicMethod.modeId]
                else:
                    toDoTasksSql = "select * from `report` where projectId = %s and status = %s  and modeId = %s  and userId = %s order by createTime asc"
                    toDoTasksSqlParamList = [publicMethod.projectId, 0, publicMethod.modeId, publicMethod.userId]
                toDoTasks = mySqlOperate.search(toDoTasksSql, toDoTasksSqlParamList)
                if toDoTasks is None:
                    print("toDoTaskSql执行失败")
                    continue
                # 没有需要执行的任务则等待sleepTime秒后继续检测
                if len(toDoTasks) > 0:
                    # 有需要执行的任务，执行任务
                    now = time.strftime("%Y-%m-%d %H:%M:%S")
                    toDoTaskData = toDoTasks[0]
                    # 0 id
                    reportId = toDoTaskData[0]
                    startTaskSql = "UPDATE report SET status = %s, updateTime = %s where id = %s"
                    startTaskSqlParamList = [1, now, reportId]
                    startTaskSqlResult = mySqlOperate.update(startTaskSql, startTaskSqlParamList)
                    if startTaskSqlResult == 0:
                        print("startTaskSql执行失败")
                        continue
                    self.runTask(toDoTaskData, reportPath)
            time.sleep(self.sleepTime)

    @staticmethod
    def runTask(toDoTaskData, reportPath):
        testSuite = unittest.TestSuite()
        reportId = toDoTaskData[0]
        taskType = toDoTaskData[2]
        taskId = toDoTaskData[3]
        try:
            print("开始执行任务，type：" + str(taskType) + "，id：" + taskId)
            # 加载环境变量
            environmentId = toDoTaskData[12]
            getEnvironmentVariablesSql = "select * from environment_variables where environmentId = %s and  status = %s"
            getEnvironmentVariablesSqlParamList = [environmentId, 1]
            environmentVariables = mySqlOperate.search(getEnvironmentVariablesSql, getEnvironmentVariablesSqlParamList)
            if not (environmentVariables is None):
                for environmentVariable in environmentVariables:
                    try:
                        environmentVariableName = environmentVariable[2]
                        environmentVariableType = environmentVariable[7]
                        environmentVariableValue = environmentVariable[3]
                        value = publicMethod.convertType(environmentVariableValue, environmentVariableType)
                        publicMethod.environmentVariableDict[environmentVariableName] = value
                    except Exception as e:
                        print("加载环境变量失败2")
                        failed(reportId, 4)
                        print(e)
            else:
                print("加载环境变量失败1")
                failed(reportId, 4)
            if runAndReport.lock == 0:
                # 加载测试用例
                if taskType == 1:
                    caseId = taskId
                    publicMethod.caseIdList.append(caseId)
                    publicMethod.casesDataDict[caseId] = {}
                    publicMethod.casesDataDict[caseId]["caseName"] = toDoTaskData[1]
                    publicMethod.casesDataDict[caseId]["caseData"] = []
                elif taskType == 2:
                    publicMethod.currentSuiteName = toDoTaskData[1]
                    suiteStepsSql = "select * from suite_step where suiteId = %s and status = %s"
                    suiteStepsSqlParamList = [taskId, 1]
                    suiteSteps = mySqlOperate.search(suiteStepsSql, suiteStepsSqlParamList)
                    if not (suiteSteps is None):
                        for suiteStep in suiteSteps:
                            if runAndReport.lock == 0:
                                caseId = suiteStep[2]
                                publicMethod.caseIdList.append(caseId)
                                publicMethod.casesDataDict[caseId] = {}
                                caseSql = "select * from `case` where id = %s"
                                caseSqlParamList = [caseId]
                                case = mySqlOperate.search(caseSql, caseSqlParamList)
                                if not (case is None):
                                    case = case[0]
                                    publicMethod.casesDataDict[caseId]["caseName"] = case[1]
                                    publicMethod.casesDataDict[caseId]["caseData"] = []
                                else:
                                    print("获取测试用例失败")
                                    failed(reportId, 5)
                    else:
                        print("获取集合步骤失败")
                        failed(reportId, 6)
                if runAndReport.lock == 0:
                    # 加载测试用例步骤，即测试片段
                    for caseId in publicMethod.caseIdList:
                        caseStepsSql = "select * from `case_step` where caseId = %s and status = %s order by sequence asc"
                        caseStepsSqlParamList = [caseId, 1]
                        caseSteps = mySqlOperate.search(caseStepsSql, caseStepsSqlParamList)
                        caseStepDict = {}
                        if not (caseSteps is None):
                            for caseStep in caseSteps:
                                testSuite.addTest(publicTestCase('test_public'))
                                if runAndReport.lock == 0:
                                    caseStepDict = {}
                                    fragmentId = caseStep[2]
                                    fragmentSql = "select * from `fragment` where id = %s"
                                    fragmentSqlParamList = [fragmentId]
                                    fragment = mySqlOperate.search(fragmentSql, fragmentSqlParamList)
                                    if not (fragment is None):
                                        fragment = fragment[0]
                                        fragmentId = fragment[0]
                                        fragmentName = fragment[1]
                                        fragmentTemplateId = fragment[2]
                                        caseStepDict["fragmentId"] = fragmentId
                                        caseStepDict["fragmentName"] = fragmentName
                                        caseStepDict["fragmentTemplateId"] = fragmentTemplateId
                                        # 加载测试片段参数
                                        fragmentParamsSql = "select * from fragment_param where fragmentId = %s and status = %s"
                                        fragmentParamsSqlParamList = [fragmentId, 1]
                                        fragmentParams = mySqlOperate.search(fragmentParamsSql, fragmentParamsSqlParamList)
                                        if not (fragmentParams is None):
                                            paramDict = {}
                                            for fragmentParam in fragmentParams:
                                                paramName = fragmentParam[1]
                                                paramType = fragmentParam[2]
                                                paramValue = fragmentParam[3]
                                                value = publicMethod.convertType(paramValue, paramType)
                                                print(paramName)
                                                paramDict[paramName] = value
                                            caseStepDict["fragmentParamDict"] = paramDict
                                        else:
                                            print("获取片段参数失败")
                                            failed(reportId, 9)
                                        if runAndReport.lock == 0:
                                            fragmentTemplateStepsSql = "select * from fragment_template_step where templateId = %s and parentId is %s and status = %s order by sequence asc"
                                            fragmentTemplateStepsParams = [fragmentTemplateId, None, 1]
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
                                                    templateStepList.append(dictionary)
                                                caseStepDict["templateStepList"] = templateStepList
                                            else:
                                                print("获取片段模板步骤失败")
                                                failed(reportId, 10)
                                    else:
                                        print("获取用例片段失败")
                                        failed(reportId, 8)
                                    if runAndReport.lock == 0:
                                        publicMethod.casesDataDict[caseId]["caseData"].append(caseStepDict)
                        else:
                            print("获取用例步骤失败")
                            failed(reportId, 7)
                print(publicMethod.casesDataDict)
                print(publicMethod.environmentVariableDict)

                if runAndReport.lock == 0:
                    """执行所有测试用例，并把结果写入报告"""
                    result = BeautifulReport(testSuite)
                    now = time.strftime("%Y%m%d%H%M%S")
                    if not os.path.exists(reportPath):
                        os.makedirs(os.path.abspath(reportPath))
                    filename = now + '_' + toDoTaskData[1] + '.html'
                    result.report(filename=filename, description=toDoTaskData[1], log_path=reportPath)
                    now = time.strftime("%Y-%m-%d %H:%M:%S")
                    reportPath = str(os.path.abspath(reportPath)) + "\\" + filename
                    reportPath = reportPath.replace("\\", "/", -1)
                    if runAndReport.lock == 0:
                        suiteLastResult = 1
                        taskResult = 1
                        i = 0
                        for caseId in publicMethod.caseIdList:
                            result = publicMethod.runCaseResultList[i]
                            if taskType == 2:
                                if result == 0:
                                    suiteLastResult = 0
                            if result == 0:
                                taskResult = 0
                            now = time.strftime("%Y-%m-%d %H:%M:%S")
                            updateCaseSql = "update `case` SET lastResult = %s, updateTime = %s where id = %s"
                            updateCaseSqlParamList = [result, now, caseId]
                            updateCaseSqlResult = mySqlOperate.update(updateCaseSql, updateCaseSqlParamList)
                            i = i + 1
                        if taskType == 2:
                            now = time.strftime("%Y-%m-%d %H:%M:%S")
                            updateSuiteSql = "update `suite` SET lastResult = %s, updateTime = %s where id = %s"
                            updateSuiteSqlParamList = [suiteLastResult, now, taskId]
                            updateSuiteSqlResult = mySqlOperate.update(updateSuiteSql, updateSuiteSqlParamList)
                        updateReportSql = "update report set status = %s, result = %s, reportPath = %s, updateTime = %s where id = %s"
                        updateReportSqlParamList = [2, taskResult, reportPath, now, reportId]
                        updateReportSqlResult = mySqlOperate.update(updateReportSql, updateReportSqlParamList)
                    if runAndReport.lock == 0:
                        initializationData()
        except Exception as e:
            print("发生未知错误")
            failed(reportId, 11)
            print(e)
