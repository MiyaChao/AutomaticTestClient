# -*- coding: utf-8 -*-
"""
@Time ： 2020/9/11 17:51
@Auth ： 邓锐坤
@File ：Application.py
@IDE ：PyCharm

"""
import os
import threading
import time
from tkinter import *
from tkinter import messagebox

import psutil

from operate.MySqlOperate import mySqlOperate
from constant.BaseConstant import *

projectIdList = []
projectPidDict = {}
pidProjectDict = {}
projectRestarted = {}
projectStartButtonDict = {}
projectStopButtonDict = {}
projectStatusLabelDict = {}
projectThreadDict = {}
thread_check_dict = {"thread_check": True}


def check():
    while 1 == 1:
        if thread_check_dict["thread_check"] is False:
            return 0
        for projectId in projectIdList:
            if projectId in projectRestarted:
                if projectRestarted[projectId] == 1:
                    searchPidSql = "select * from `project_pid` where userId = %s and projectId = %s and modeId = %s"
                    searchPidSqlParamList = [userId, projectId, modeId]
                    searchPidSqlResult = mySqlOperate.search(searchPidSql, searchPidSqlParamList)
                    if searchPidSqlResult is None:
                        raise Exception("查询pid信息失败")
                    else:
                        if not (searchPidSqlResult[0][4] is None):
                            projectPidDict[projectId] = searchPidSqlResult[0][4]
                            pidProjectDict[searchPidSqlResult[0][4]] = projectId
                            projectRestarted[projectId] = 0
                if projectId in projectPidDict:
                    pl = psutil.pids()
                    result = False
                    for pid in pl:
                        if pid == projectPidDict[projectId]:
                            result = True
                            break
                        else:
                            result = False
                    if result is False:
                        del projectPidDict[projectId]
                        projectStatusLabelDict[projectId]["text"] = "未启动"
                        projectStatusLabelDict[projectId]["fg"] = "red"

thread_check = threading.Thread(target=check)
thread_check.start()


def runCommand(command):
    try:
        os.system(command)
    except:
        print("命令执行失败，" + command)


def startProject(projectData):
    # projectStartButtonDict[projectData["projectId"]].grid_forget()
    # projectStopButtonDict[projectData["projectId"]].grid(row=projectData["row"], column=4, sticky=W)
    stopProject(projectData)

    command = "python ourTest_client.py "
    command = command + userId + " "
    command = command + projectData["projectId"] + " "
    command = command + modeId + " "
    thread = threading.Thread(target=runCommand, args=(command,))
    thread.start()
    projectThreadDict[projectData["projectId"]] = thread
    projectRestarted[projectData["projectId"]] = 1

    projectStatusLabelDict[projectData["projectId"]]["text"] = "已启动"
    projectStatusLabelDict[projectData["projectId"]]["fg"] = "green"


def stopProject(projectData):
    # projectStopButtonDict[projectData["projectId"]].grid_forget()
    # projectStartButtonDict[projectData["projectId"]].grid(row=projectData["row"], column=4, sticky=W)
    try:
        if projectData["projectId"] in projectThreadDict:
            searchPidSql = "select * from `project_pid` where userId = %s and projectId = %s and modeId = %s"
            searchPidSqlParamList = [userId, projectData["projectId"], modeId]
            searchPidSqlResult = mySqlOperate.search(searchPidSql, searchPidSqlParamList)
            if searchPidSqlResult is None:
                raise Exception("查询pid信息失败")
            else:
                if not (searchPidSqlResult[0][4] is None):
                    command = 'taskkill -f -pid %s' % searchPidSqlResult[0][4]
                    try:
                        os.system(command)
                    except:
                        print("进程不存在，" + command)
                    setPidSql = "update `project_pid` set pid = %s where id = %s"
                    setPidSqlParamList = [None, searchPidSqlResult[0][0]]
                    setPidSqlResult = mySqlOperate.update(setPidSql, setPidSqlParamList)
                    if setPidSqlResult == 0:
                        raise Exception("保存pid信息失败1")
    except OSError as e:
        print(e)

    projectStatusLabelDict[projectData["projectId"]]["text"] = "未启动"
    projectStatusLabelDict[projectData["projectId"]]["fg"] = "red"


def callbackClose():
    result = messagebox.askyesno('Choose', '是否退出程序？')
    if result is True:
        thread_check_dict["thread_check"] = False
        for projectId in projectIdList:
            projectData = {"projectId": projectId}
            stopProject(projectData)
        sys.exit(0)
    else:
        pass


class application:
    def __init__(self):
        self.win = Tk()
        self.win.title("ourTest")
        self.win.geometry("600x200")
        self.createWidgets()
        self.win.protocol("WM_DELETE_WINDOW", callbackClose)
        self.win.mainloop()

    def createWidgets(self):
        menubar = Menu(self.win)
        menu_1 = Menu(menubar, tearoff=0)
        for each in ['当前用户', '退出登录']:
            menu_1.add_command(label=each)
        menu_2 = Menu(menubar, tearoff=0)
        for each in ['关于我们']:
            menu_2.add_command(label=each)
        menubar.add_cascade(label="用户", menu=menu_1)
        menubar.add_cascade(label="关于", menu=menu_2)
        self.win['menu'] = menubar

        projectSql = "select * from `project` where groupId = %s and status = %s"
        projectSqlParamList = ["ZZ1597398638108", 1]
        projectSqlResult = mySqlOperate.search(projectSql, projectSqlParamList)
        if projectSqlResult is None:
            raise Exception("查询项目信息失败")
        else:
            row = 1
            for projectData in projectSqlResult:
                projectId = projectData[0]
                projectName = projectData[1]
                projectIdList.append(projectId)
                projectData = {"projectId": projectId, "projectName": projectName, "row": row}
                idLabel = Label(self.win, text="项目ID", anchor=NW, width=20)
                nameLabel = Label(self.win, text="项目名称", anchor=NW, width=20)
                statusLabel = Label(self.win, text="状态", anchor=NW, width=20)
                operateLabel = Label(self.win, text="操作", anchor=NW, width=20)
                idLabel.grid(row=0, column=0, sticky=W)
                nameLabel.grid(row=0, column=2, sticky=W)
                statusLabel.grid(row=0, column=3, sticky=W)
                operateLabel.grid(row=0, column=4, sticky=W, columnspan=2)
                projectIdLabel = Label(self.win, text=projectId, anchor=NW, width=20)
                projectNameLabel = Label(self.win, text=projectName, anchor=NW, width=20)
                projectStatusLabel = Label(self.win, text="未启动", anchor=NW, width=20, fg="red")
                projectStatusLabelDict[projectId] = projectStatusLabel
                projectStartOperateLabel = Button(self.win, text="启动", anchor=NW, command=lambda arg=projectData: startProject(arg), fg="green")
                projectStartButtonDict[projectId] = projectStartOperateLabel
                projectStopOperateLabel = Button(self.win, text="结束", anchor=NW, command=lambda arg=projectData: stopProject(arg), fg="red")
                projectStopButtonDict[projectId] = projectStopOperateLabel
                projectIdLabel.grid(row=row, column=0, sticky=W)
                projectNameLabel.grid(row=row, column=2, sticky=W)
                projectStatusLabel.grid(row=row, column=3, sticky=W)
                projectStartOperateLabel.grid(row=row, column=4, sticky=W)
                projectStopOperateLabel.grid(row=row, column=5, sticky=W)
                row = row + 1
