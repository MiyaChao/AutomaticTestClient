import os
import random
import sys
import threading
import time
from constant.BaseConstant import *
from method.PublicMethod import publicMethod
from operate.MySqlOperate import mySqlOperate
from runTest.RunAndReport import runAndReport
from constant import BaseConstant


class runTestCaseThread(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        run = runAndReport()
        run.checkTask(reportPath)


if __name__ == '__main__':
    pid = os.getpid()
    publicMethod.userId = sys.argv[1]
    publicMethod.projectId = sys.argv[2]
    publicMethod.modeId = sys.argv[3]
    reportPath = "./report/" + BaseConstant.groupId + "/" + publicMethod.projectId
    reportImgPath = "../AutomaticTestImgReports/" + BaseConstant.groupId + "/" + publicMethod.projectId

    searchUserSql = "select * from `user` where id = %s"
    searchUserSqlParamList = [publicMethod.userId]
    searchUserSqlResult = mySqlOperate.search(searchUserSql, searchUserSqlParamList)
    if searchUserSqlResult is None:
        raise Exception("查询用户信息失败")
    else:
        if len(searchUserSqlResult) > 0:
            userType = searchUserSqlResult[0][11]
            if not (userType == int(publicMethod.modeId)):
                if userType == 0:
                    raise Exception("该用户没有启动团队模式任务的权限")
                elif userType == 1:
                    raise Exception("该用户没有启动个人模式任务的权限")
        else:
            raise Exception("用户信息错误，此用户不存在")

    searchPidSql = "select * from `project_pid` where userId = %s and projectId = %s and modeId = %s"
    searchPidSqlParamList = [publicMethod.userId, publicMethod.projectId, publicMethod.modeId]
    searchPidSqlResult = mySqlOperate.search(searchPidSql, searchPidSqlParamList)
    if searchPidSqlResult is None:
        raise Exception("查询pid信息失败")
    else:
        if len(searchPidSqlResult) > 0:
            setPidSql = "update `project_pid` set pid = %s where id = %s"
            setPidSqlParamList = [pid, searchPidSqlResult[0][0]]
            setPidSqlResult = mySqlOperate.update(setPidSql, setPidSqlParamList)
            if setPidSqlResult == 0:
                raise Exception("保存pid信息失败1")
        else:
            now = time.time() * 1000
            pidId = 'PID' + str(int(now) + random.randint(1, 1000))
            now = time.strftime("%Y-%m-%d %H:%M:%S")
            addPidSql = "insert into `project_pid` (id, projectId, userId, modeId, pid, createTime, updateTime) value (%s, %s, %s, %s, %s, %s, %s)"
            addPidSqlParamList = [pidId, publicMethod.projectId, publicMethod.userId, publicMethod.modeId, pid, now, now]
            addPidSqlResult = mySqlOperate.update(addPidSql, addPidSqlParamList)
            if addPidSqlResult == 0:
                raise Exception("保存pid信息失败2")

    thread = runTestCaseThread(1, publicMethod.projectId)
    thread.start()
