from script.ZZ1597398638108.XM1598949386052 import *
from script.ZZ1597398638108.XM1598949386052.conf import *
from method.PublicMethod import *
import functools


def assert_fun(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print('call %s():' % func.__name__)
        # print('args = {}'.format(*args))
        r = func(*args, **kwargs)
        # print(r.status_code)
        assert r.status_code == 200
        assert r.json()['code'] == '000'
        return r
    return wrapper


class AuditApi:
    def __init__(self):
        # self.host = publicMethod.getEnvironmentVariable("host")
        self.host='http://test.dasu123.inet'

    # 登录
    def login_sys(self, account, password):
        payload = {
            'account': account,
            'password': password,
        }
        url = f'{self.host}/admin/login/login'

        r = s.request('POST',url, data=payload)

        return r

    # 退出登录
    def login_out(self):
        url = f'{self.host}/admin/login/logout'
        r = s.request('POST',url)
        return r

    # 添加申请
    def create(self, atype, payload):
        url = f'{self.host}/{terminal}/{atype}/create'
        r = s.request('POST', url, data=payload)
        return r

    # 审核
    def do_action(self,
                  atype,
                  payload,
                  ):

        url = f'{self.host}/{terminal}/{atype}/doAction'
        r = s.request('POST', url, data=payload)
        return r

    # 详细信息 - 获取按钮类型：审核通过 不通过 拒绝
    @assert_fun
    def detail(self,atype, id):
        payload = {'id': id}
        url = f'{self.host}/{terminal}/{atype}/detail'
        r = s.request('GET', url, data=payload)
        print(r.json())
        return r

    # 获取待审核列表
    def get_verify_list(self):
        url = f'{self.host}/{terminal}/myFlow/getVerifyList'
        r = s.request('GET', url)
        return r

# 获取已发起列表
    def get_own_list(self):
        url = f'{self.host}/{terminal}/myFlow/getOwnList?page=1&pageSize=10'
        r = s.request('GET', url)
        return r

    def callBack(self, id):
        url = f'{self.host}/{terminal}/myFlow/callBackEntry'
        r = s.request('POST', url, data={'id': id})
        # print(r.json()['message'])
        return r

# 获取流程配置
    def get_flowlist(self):
        r = s.request('GET',f'{self.host}/flow/flow/getList?page=1&pageSize=1000')
        flowlist = r.json()['data']
        return flowlist


class BussinessComm(AuditApi):

    # 获取已发起列表最新一条记录的id
    def get_own_record_id(self):
        r = self.get_own_list()
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
                return item['stateName']
        raise Exception('已发起列表中未找到该记录！')

    def get_transactions(self,detail,act):
        if act == 'success':
            transitions = detail['data']['success']
        elif act == 'back':
            transitions = detail['data']['back']
        elif act == 'cancel':
            transitions = detail['data']['cancel']
        return act

    # 审核操作： 审核通过  审核不通过  拒绝
    def audit_act(self,atype,detail,act,payload):

        if act == 'success':
            transitions = detail['data']['success']
        elif act == 'back':
            transitions = detail['data']['back']
        elif act == 'cancel':
            transitions = detail['data']['cancel']
        # transitions = self.get_detail_action(detail,act)

        for i in range(len(transitions)):
            payload[f'transitions[{i}]'] = transitions[i]
        r = self.do_action(atype, payload)

        return r

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


if __name__ == '__main__':
    t = BussinessComm()
    t.login_sys(*adminUser)
    atype='CardV1'
    # t=BussinessComm()
    id = t.get_own_record_id()
    print(id)
    detail = t.detail(atype,id).json()

    # transitions = t.get_detail_action(atype, id,'success')
    # payload = {'id': id, 'reason': '同意'}
    # t.audit_act(atype,detail,'success',payload)
    # t.callBack(id)
    # t.check_state(id,'pass')