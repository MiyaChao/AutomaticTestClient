# -*- coding: utf-8 -*-
"""
@Time ： 2020/9/1 11:05
@Auth ： 邓锐坤
@File ：CustomScript.py
@IDE ：PyCharm

"""
# from script.ZZ1597398638108.XM1598949386052.testcase.testcase_card import *
# from script.ZZ1597398638108.XM1598949386052.testcase.testcase_invoice import *
# from script.ZZ1597398638108.XM1598949386052.testcase.testcase_purchase import *
# from script.ZZ1597398638108.XM1598949386052.testcase.testcase_agreement_approval import *
from script.ZZ1597398638108.XM1598949386052.testcase.testcase import *
from script.ZZ1597398638108.XM1598949386052.AuditFunc import *
from faker import Faker
import json

f = Faker('Zh_cn')


def run(methodName, paramDict):
    result = globals().get(methodName)(paramDict)
    return result


def login_crm_test_inet(paramDict):
    username = paramDict['username']
    password = paramDict['password']
    # adminUser = ('wang@qq.com',
    #              'dlhVBnlYrba25NJSj6R7wjkramZn1GI6DAkcLkQ9p/7T0fm09uzqXgiHR+lcwb0NC1JTSWx0jAa6cmK0wN00yG3fD6yM2wjqzWajwmfkYTLnCVZ3AE0opjw8txgfh9/ejNLtOGpazE6n9A82rPdRGNx5UjhNgKOZr60oH/oJwMk='
    #              )
    l = BussinessComm()
    r = l.login_sys(username,password)
    print(r.json())
    return r.json()

def login_out():
    t=BussinessComm()
    r = t.login_out()
    return r.json()


# “已发起”列表最新记录的id
def get_own_record_id(paramDict):
    t = BussinessComm()
    id = t.get_own_record_id()
    print(id)
    return id

# 撤回
def call_back(paramDict):
    t = BussinessComm()
    id = publicMethod.getGlobalVariable('id')

    r = t.call_back(id)
    return r.json()

# 详情，返回详情消息体
def detail(paramDict):
    # atype = paramDict['businessType']
    atype = publicMethod.getGlobalVariable('atype')
    id=publicMethod.getGlobalVariable('id')

    t = BussinessComm()
    r = t.detail(atype,id)
    print(r.json())
    return r.json()


# 通过
def audit_pass(paramDict):
    atype = publicMethod.getGlobalVariable('atype')
    # atype = paramDict['businessType']
    id = publicMethod.getGlobalVariable('id')
    detail = publicMethod.getGlobalVariable('detail')

    t = BussinessComm()
    payload = {'id': id, 'reason': '同意'}

    r = t.audit_act(atype, detail, "success", payload)
    return r.json()

# 不通过
def audit_back(paramDict):
    atype = publicMethod.getGlobalVariable('atype')
    # atype = paramDict['businessType']
    id = publicMethod.getGlobalVariable('id')
    detail = publicMethod.getGlobalVariable('detail')

    t = BussinessComm()

    payload = {'id': id, 'reason': '不同意，请重新提交'}

    r = t.audit_act(atype,detail,"back",payload)

    return r.json()

# 拒绝
def audit_cancel(paramDict):
    atype = publicMethod.getGlobalVariable('atype')
    # atype = paramDict['businessType']
    id = publicMethod.getGlobalVariable('id')
    detail = publicMethod.getGlobalVariable('detail')

    t = BussinessComm()
    payload = {'id': id, 'reason': '不同意，作废'}

    r = t.audit_act(atype, detail, "cancel", payload)

    return r.json()


# 审核通过-指定执行人
def audit_pass_assign(paramDict):
    atype = publicMethod.getGlobalVariable('atype')
    # atype = paramDict['businessType']
    id = publicMethod.getGlobalVariable('id')
    detail = publicMethod.getGlobalVariable('detail')

    t = BussinessComm()
    payload = {'id': id,
               'dynamicUserIds[0]': '015db7b10b048f65e8'    # wang5
               }

    r = t.audit_act(atype,detail,"success",payload)

    return r.json()

# 通用审核通过流程,审核过程中无其他参数
def audit_all_pass(paramDict):
    atype = publicMethod.getGlobalVariable('atype')
    # atype = paramDict['businessType']
    # staList = paramDict['staList']
    id = publicMethod.getGlobalVariable('id')

    b = BussinessComm()
    stateList = b.audit_all_pass(atype,id)
    # assert stateList == staList, f'审核流程不正确：{stateList}'
    return stateList

def check_state_list(ParamDict):
    stateList = publicMethod.getGlobalVariable('stateList')
    staList = ParamDict['ParamDict']
    assert stateList == staList,f'审核流程不正确{stateList}'

# 从“已发起”列表获取审核流程
def check_state(paramDict):
    id = publicMethod.getGlobalVariable('id')
    act = paramDict['act']
    t = BussinessComm()
    stateName= t.get_own_state(id)      # 从已发起列表获取
    if act == 'pass':
        assert stateName in ['结束', '完成', '已结案']
    elif act == 'back':
        assert stateName in ['提交申请']
    elif act == 'cancel':
        assert stateName in ['作废']
    else:
        raise Exception('act参数错误！')
    print(stateName)

    return stateName

# 从“待审核”列表获取审核流程
def get_verify_state(ParamDict):
    id = publicMethod.getGlobalVariable('id')
    t = BussinessComm()
    stateName = t.get_verify_state(id)
    print(stateName)

    return stateName




# ========================具体业务=========================
# -------------名片印制---------------
# def get_info():
#     c = Card()
#     atype = c.card_info()
#     return atype

# 名片印制_创建申请
def create_card(paramDict):
    c = Card()
    r = c.test_create_card()

    print(r.json())
    return r.json()

# 名片印制_修改
def update_card(paramDict):
    id = publicMethod.getGlobalVariable('id')

    c = Card()
    r = c.test_update_card(id)

    print(r.json())
    return r.json()
# ---------名片印制：结束-----------

# ----------请款单---------
# 请款单_提交申请
def create_invoice(paramDict):
    isComplete = int(paramDict['isComplete'])       # isComplete:1 资料齐全    0 资料不齐

    c = Invoice()
    r = c.test_create_invoice(isComplete=isComplete)
    print(r.json())
    return r

# 请款单_修改
def update_invoice(paramDict):
    id = publicMethod.getGlobalVariable('id')

    c = Invoice()
    r = c.test_update_invoice(id, isComplete=0 )

    print(r.json())
    return r.json()

# 请款单_全部审核通过流程
def audit_all_pass_invoice(paramDict):
    id = publicMethod.getGlobalVariable('id')
    # staList = paramDict['staList']

    c = Invoice()
    stateList = c.audit_all_pass(id)

    return stateList

# ----------结束----------

# ----------物品申购---------
# 物品申购_提交申请
def create_purchase(paramDict):
    applyType = int(paramDict['applyType'])       # applyType:1 500元以下    2 ：500~5W      3: 5w以上

    c = Purchase()
    r = c.test_create_purchase(applyType=applyType)
    print(r.json())
    return r

# 物品申购_修改
def update_purchase(paramDict):
    id = publicMethod.getGlobalVariable('id')

    c = Purchase()
    r = c.test_update_purchase(id)

    print(r.json())
    # assert r.json()['code']== '000','update_purchase出错！'
    return r.json()
# ---------结束----------

#  ----------合同审批---------
# 合同审批_提交申请
def create_agreement_approval(paramDict):
    c = AgreementApproval()
    r = c.test_create_agreement_approval()
    print(r.json())
    return r

# 物品申购_修改
def update_agreement_approval(paramDict):
    id = publicMethod.getGlobalVariable('id')

    c = AgreementApproval()
    r = c.test_update_agreement_approval(id)

    print(r.json())
    # assert r.json()['code']== '000','update_purchase出错！'
    return r.json()
# ---------结束----------

# 合同审批_提交申请
def create_agreement_verify(paramDict):
    c = AgreementVerify()
    r = c.test_create_agreement_verify()
    print(r.json())
    return r

# 物品申购_修改
def update_agreement_verify(paramDict):
    # ttype = paramDict['ttype']
    id = publicMethod.getGlobalVariable('id')

    c = AgreementVerify()
    r = c.test_update_agreement_verify(id)

    print(r.json())
    return r.json()
# ---------结束----------





# if  __name__=="__main__":

    # login_crm_test_inet()