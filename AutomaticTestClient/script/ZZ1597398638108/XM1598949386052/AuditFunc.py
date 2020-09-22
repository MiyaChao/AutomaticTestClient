from script.ZZ1597398638108.XM1598949386052 import *
from script.ZZ1597398638108.XM1598949386052.conf import *
from method.PublicMethod import *
import functools
import time
import pandas as pd
import time
import numpy as np
import openpyxl
# from operate.RequestOperate import HttpSession

def assert_fun(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print('call %s():' % func.__name__)
        # print('args = {}'.format(*args))
        r = func(*args, **kwargs)
        # print(r.status_code)
        assert r.status_code == 200

        return r

    return wrapper


class AuditApi:
    # def __init__(self):
    #     # self.host = publicMethod.getEnvironmentVariable("host")
    #     self.host='http://flow.dasu123.inet'

    # 登录
    @assert_fun
    def login_sys(self, account, password):
        payload = {
            'account': account,
            'password': password,
        }
        url = f'{host}/admin/login/login'

        r = s.request('POST',url, data=payload)
        # r.cookies
        return r

    # 退出登录
    @assert_fun
    def login_out(self):
        url = f'{host}/admin/login/logout'
        r = s.request('POST',url)
        return r

    # 添加申请
    @assert_fun
    def create(self, atype, payload):
        url = f'{host}/{terminal}/{atype}/create'
        r = s.request('POST', url, data=payload)
        return r

    @assert_fun
    def update(self, atype,id,payload):
        payload['id'] = id
        url = f'{host}/{terminal}/{atype}/update'
        r = s.request('POST', url, data=payload)
        return r

    # 审核
    @assert_fun
    def do_action(self,
                  atype,
                  payload,
                  ):

        url = f'{host}/{terminal}/{atype}/doAction'
        r = s.request('POST', url, data=payload)
        return r

    # 详细信息 - 获取按钮类型：审核通过 不通过 拒绝
    @assert_fun
    def detail(self,atype, id):
        payload = {'id': id}
        url = f'{host}/{terminal}/{atype}/detail'
        r = s.request('GET', url, data=payload)

        return r

    # 获取待审核列表
    @assert_fun
    def get_verify_list(self):
        url = f'{host}/{terminal}/myFlow/getVerifyList'
        r = s.request('GET', url)
        return r

# 获取已发起列表
    @assert_fun
    def get_own_list(self):
        url = f'{host}/{terminal}/myFlow/getOwnList?page=1&pageSize=10'
        r = s.request('GET', url)
        return r

    @assert_fun
    def call_back(self, id):

        url = f'{host}/{terminal}/myFlow/callBackEntry'
        r = s.request('POST', url, data={'id': id})
        # print(r.json()['message'])
        return r

# 获取流程配置列表
    @assert_fun
    def get_flowlist(self):
        r = s.request('GET',f'{host}/flow/flow/getList?page=1&pageSize=1000')
        # flowlist = r.json()['data']
        # return flowlist
        return r

# 流程配置
    @assert_fun
    def get_work_flow(self,id):
        r = s.request('GET', f'{host}/flow/FlowConfigUser/detail?id={id}')

        return r

    # 上传文件
    @assert_fun
    def upload(self, fileData):
        # fileData = publicMethod.convertType(r'D:\Users\monda\Desktop\测试附件\1.jpg', 'file','src')
        # print(fileData)
        # payload = {'src':file_data}
        r = s.request('POST',f'{host}/utils/upload/upload',files=fileData)

        return r

    #  获取业务部门
    @assert_fun
    def get_department(self):
        r = s.request('GET', f'{host}/flow/structure/getTwoAndOneLevelStructure')
        return r

class BussinessComm(AuditApi):
    # def set_atype(self, value):
    #     self.atype = publicMethod.setGlobalVariable('atype',value)
    #     return self.atype

    # 获取已发起列表最新一条记录的id
    def get_own_record_id(self):
        r = self.get_own_list()
        # print(r.json())
        id = r.json()['data'][0]['id']
        return id

    # 在“待审核”列表中找到对应id的记录，并返回该记录的审核流程
    def get_verify_state(self, id):
        alist = self.get_verify_list().json()['data']
        for item in alist:
            if item['id'] == id:
                return item['stateName']
        raise Exception('待审核列表中未找到该记录！')

    # 在“已发起”列表中找到对应id的记录，并返回该记录的审核流程
    def get_own_state(self, id):

        alist = self.get_own_list().json()['data']
        for item in alist:
            if item['id'] == id:
                return item['stateName'],item['stateStatus']
        raise Exception('已发起列表中未找到该记录！')

    # def get_transactions(self,detail,act):
    #     if act == 'success':
    #         transitions = detail['data']['success']
    #     elif act == 'back':
    #         transitions = detail['data']['back']
    #     elif act == 'cancel':
    #         transitions = detail['data']['cancel']
    #     return act

    # 审核操作： 审核通过  审核不通过  拒绝
    def audit_act(self,atype,detail,act,payload):
        # detail = self.detail(atype,id).json()
        # print(detail)
        if act == 'success':
            print(detail)
            transitions = detail['data']['success']
        elif act == 'back':
            transitions = detail['data']['back']
        elif act == 'cancel':
            transitions = detail['data']['cancel']
        else:
            raise Exception(f"传入act参数不正确:{act}")
        print(f'transitions:{transitions}')

        if transitions:
            for i in range(len(transitions)):
                payload[f'transitions[{i}]'] = transitions[i]
            r = self.do_action(atype, payload)
            return r
        else:   # transitions为空，可能是因为不是当前流程审核人
            raise Exception(f'transitions不正确：{transitions}')

    # 审核通过流程，验证审核流程
    def audit_all_pass(self,atype,id):
        workFlow = self.get_flow(atype)     # 获取流程配置
        workSteps = workFlow['steps']
        stateList = []
        while True:
            detail = self.detail(atype,id).json()

            stateId = detail['data']['stateId']
            for item in workSteps:                  # 找到对应的流程名称
                if stateId == item['stateId']:
                    stateName = item['label']
                    print(stateName)
                    stateList.append(stateName)

            if stateName in ['结束', '完成', '已完成', '已结案']:
                return stateList

            payload = {'id': id, 'reason': '同意'}
            r = self.audit_act(atype, detail, "success", payload)
            assert r.json()['code'] == '000', r.json()
            time.sleep(1)

    def upload_file(self):
        myFile={
            "value":"D:\\Users\\monda\\Desktop\\测试附件\\1.jpg",
            "fileKey":"src"
        }
        fileData = publicMethod.convertType(myFile, 'file')

        fileName = fileData['src'][0]

        r = self.upload(fileData)

        filePath = r.json()['data']['httpPath']
        return fileName,filePath

# 返回流程配置
    # 根据atype 去文件中找对应的flowid,请求接口，返回流程配置
    def get_flow(self, atype):
        wordFlow = self.read_config()
        for item in wordFlow:
            if item['atype'] == atype:
                flowId = item['id']

                r = self.get_work_flow(flowId)
                workFlow = r.json()['data']
                return workFlow
        raise Exception('未找到对应的flowid')




    # def audit_pass_1(self,atype, tt=[]):
    #     steps = self.get_flow()
    #     aList = self.get_list()
    #     id = aList.json()['data'][0]['id']
    #
    #     while True:
    #         detail = self.detail(id).json()['data']
    #
    #         stateId = detail['stateId']
    #         success = detail['success']
    #
    #         step = self.get_current_flow(stateId, steps)
    #         print(step)
    #
    #         # 有success操作，执行审核通过动作
    #         if success:
    #
    #             action = False
    #             for item in tt:  # 有其他参数
    #                 if str(stateId) == str(item['id']):
    #                     item['payload']['id'] = id
    #                     r = self.do_action(atype,item['payload'], success)
    #                     action = True
    #                     break
    #
    #             if not action:  # 没有特殊参数
    #                 payload = {'id': id, 'reason': ''}
    #                 r = self.do_action(atype,payload, success)
    #
    #             if r.json()['code'] != '000':
    #                 raise Exception(r.json()['message'])
    #             continue
    #
    #         if step['label'] in ['结束', '完成', '结案', '已结案']:
    #
    #             return True
    #         else:
    #             raise Exception(f"状态不正确！当前状态为{step['label']}")

    def write_flow_to_excel(self):
        r = t.get_flowlist()
        data = r.json()['data']
        # for item in r.json()['data']:
        #     print(item['id'],item['name'],item['configName'])

        data = pd.DataFrame(data)
        # print(data)
        data.to_excel(r'./liucheng.xlsx', index=False)

# liucheng1中读取
    def read_config(self):
        df2 = pd.read_excel(r'D:\Desktop\AutomaticTestClient\script\ZZ1597398638108\XM1598949386052\liucheng1.xlsx')
        adict = df2.to_dict('records')
        # print(adict)
        return adict


if __name__ == '__main__':
    t = BussinessComm()
    t.login_sys(*adminUser)
    atype='CardV1'
    # # t=BussinessComm()
    id = t.get_own_record_id()
    # print(id)
    # payload = {'id': id, 'reason': '同意'}
    # t.audit_act(atype,id,'success',payload)

    # file_data = publicMethod.convertType(r'D:\Users\monda\Desktop\测试附件\1.jpg','file')
    # fileName, filePath=t.upload_file()
    # print(fileName,filePath)

    # r = t.get_flowlist()
    r = t.read_config()
    print(r)
    # print(r.json())

