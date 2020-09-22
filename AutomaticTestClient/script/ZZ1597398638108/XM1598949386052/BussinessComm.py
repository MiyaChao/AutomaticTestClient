from lib.Login import *
from conf import *
from lib.func import *


class BussinessComm:
    def __init__(self, atype):

        self.atype = atype

        # self.get_flowlist=read_data(r'D:\myProject\Audit1\data\流程配置.xlsx',sheet_name='流程配置')
        # print(self.get_flowlist)

    # 添加申请
    def create(self, payload):
        url = f'{host}/{terminal}/{self.atype}/create'
        r = req.post_request(url, data=payload)

        return r


    # 详细信息 - 获取按钮类型：审核通过 不通过 拒绝
    def detail(self, id):
        payload={'id': id}
        url = f'{host}/{terminal}/{self.atype}/detail'
        r = req.get_request(url, params=payload)
        return r

#
    def do_action(self,
                  payload,
                  transitions,      # 审核操作类型：通过/不通过/拒绝
                  ):       # 审核原因

        for i in range(len(transitions)):
            payload[f'transitions[{i}]']= transitions[i]

        url = f'{host}/{terminal}/{self.atype}/doAction'
        r = req.post_request(url, data=payload)
        return r

    # 获取待审核列表
    def get_list(self):
        url = f'{host}/{terminal}/myFlow/getVerifyList'
        r = req.get_request(url)

        return r


    def callBack(self, id):
        url = f'{host}/{terminal}/myFlow/callBackEntry'
        r = req.post_request(url, data={'id':id})
        print(r.json()['message'])
        return r

    def do_callBack(self):
        aList = self.get_list()
        id = aList.json()['data'][0]['id']
        r = self.callBack(id)
        return r

    # 获取流程配置
    def get_flowlist(self):
        r = req.get_request(f'{host}/flow/flow/getList?page=1&pageSize=1000')
        flowlist=r.json()['data']
        return flowlist

    def write_flowlist(self,data):
        # print(data)
        filepath,sheet_name=r'D:\myProject\Audit1\data\流程配置.xlsx','流程配置'
        write_excel(data,filepath,sheet_name)

    def read_flowlist(self):
        flowlist=read_data(r'D:\myProject\Audit1\data\流程配置.xlsx',sheet_name='流程配置')
        # print(flowlist)
        return flowlist

    def get_flowid(self,atype):
        flowList=self.get_flowlist()
        for item in flowList:
            if item['name']==atype:
                return id


    # 获取流程id
    def get_flow_id(self):
        for item in alist:
            if self.atype == item['atype']:
                return item['flowId']
        raise Exception('错误：未找到flowid')

    # 获取审核流程
    def get_flow(self):
        flowId = self.get_flow_id()
        r = req.get_request(f'{host}/flow/FlowConfigUser/detail?id={flowId}')
        print(r.json()['data']['name'])
        return r.json()['data']['steps']

    def get_current_flow(self,stateId, steps):
        for step in steps:
            if int(step['stateId']) == int(stateId):
                return step

    def audit_pass(self, tt=[]):
        steps = self.get_flow()
        aList = self.get_list()
        id = aList.json()['data'][0]['id']

        while True:
            detail = self.detail(id).json()['data']
            
            stateId = detail['stateId']
            success = detail['success']

            step = self.get_current_flow(stateId, steps)
            print(step)

            # 有success操作，执行审核通过动作
            if success:

                action=False
                for item in tt:     # 有其他参数
                    if str(stateId) == str(item['id']):
                        item['payload']['id'] = id
                        r = self.do_action(item['payload'], success)
                        action=True
                        break

                if not action:      # 没有特殊参数
                    payload = {'id': id,'reason':''}
                    r = self.do_action(payload, success)

                if r.json()['code'] != '000':
                    raise Exception(r.json()['message'])
                continue

            if step['label'] in ['结束','完成','结案','已结案']:

                return True
            else:
                raise Exception(f"状态不正确！当前状态为{step['label']}")

            # return step

    # 审核不通过 拒绝
    def audit_fail(self,
                   n,               # 第n步审核不通过
                   tt=[]):    #
        steps = self.get_flow()
        aList = self.get_list()
        id = aList.json()['data'][0]['id']

        while True:
            detail = self.detail(id).json()['data']
            stateId = detail['stateId']
            currentFlow = self.get_current_flow(stateId, steps)
            print(currentFlow)

            if int(stateId) == 1:    # 状态为重新申请，则表示审核不通过流程结束
                return True

            elif currentFlow['label'] == '作废':   # 表示审核拒绝作废流程结束
                return True

            elif not detail['success']+detail['back']+detail['cancel']:
                raise Exception('状态不正确！')

            # 当前状态非拒绝、非重新申请
            else:
                success, back, cancel = detail['success'], detail['back'], detail['cancel']

                if stateId < n:     # 执行审核通过操作

                    action = False
                    for item in tt:
                        if str(stateId) == str(item['id']):
                            item['payload']['id'] = id
                            r = self.do_action(item['payload'], success)
                            action = True
                            break

                    if not action:
                        payload = {'id': id, 'reason': ''}
                        r = self.do_action(payload, success)

                elif stateId == n:  # 执行审核不通过/拒绝操作
                    if back:
                        payload = {'id': id, 'reason': '不通过'}
                        r = self.do_action(payload, back)

                    elif cancel:
                        payload = {'id': id, 'reason': '作废'}
                        r = self.do_action(payload, cancel)

                if r.json()['code'] != '000':
                    raise Exception(r.json()['message'])
                continue


if __name__ == '__main__':
    l=Login()
    l.login_sys(*adminUser)
    u = Transation('a')
    print(u.get_list().json())
    # u.l.login_sys(*adminUser)
    # flowList=u.get_flowlist()

    # alist=u.read_flowlist()
    # print(alist)
    # func(flowList)


    # print(u.login_out().json())

    # payload={
    #     'businessType': 2,
    #     'dayiCompanyId': 5870,
    #     'dayiAccount': '13923363961',
    #     'companyName': '珠海市精模有限公司',
    #     'linkPerson': '杨志宇',
    #     'memberType': '战略直供商',
    #     'agentType': 2,
    #     'contractPeriod': '2018-12-29-2020-12-27',
    #     'saleQuota': '4000000',
    #     'saleQuotaed': '3691800',
    #     'repoQuota': '0',
    #     'repoQuotaed': '0',
    #     'puchasQuota': '0',
    #     'puchasQuotaed': '0',
    #     'useableQuota': '259900',
    #     'factorQuota': '0',
    #     'factorQuotaed': '0',
    #     'queQuota': '1200000',
    #     'queQuotaed': '1248300',
    #     'agreement': '',
    #     'serviceCharge': '0.099',
    #     'agentSave': '',
    #     'reposId': '0',
    #     'reposName': '在途货物仓库',
    #     'agentGoods': '19000.00',
    #     'agentAvailGoods': '17100.00',
    #     'agentService': '228.00',
    #     'agentCycle': '30',
    #     'tradeDeposit': '1900.00',
    #     'reposServiceCharge': '1900',
    #     'goods[0][goodsName]': '通用塑料|CPE|日本住友化学|SWA310',
    #     'goods[0][qty]': '120',
    #     'goods[0][price]': '200',
    #     'goods[0][isWmsOrder]': '1',
    #     'goods[0][money]': '24000.00',
    #     'goods[0][disabled]': 'false',
    #     'goods[0][brandNumber]': 'SWA310',
    #     'goods[0][typeName]': '通用塑料',
    #     'goods[0][factoryName]': '日本住友化学',
    #     'goods[0][productName]': 'CPE',
    #     'goods[0][typeNumber]': 'FL0001',
    #     'goods[0][productNumber]': 'PM000204',
    #     'followUp': '王大鹏',
    #     'suggest': '111111'
    # }
    # u.create('agent',payload)
    # alist = u.get_list()
    # id = alist.json()['data'][0]['id']

    # u.evaluate(id)  # 第一步：价格评估
    # u.evaluate()
    # u.creat()
    # atype='invoiceV1'
    # list = u.get_list(atype).json()
    # id=list['data'][0]['id']
    # print('---------------------')
    # d = u.detail(atype,id)
    # sucess= d.json()['data']['success']
    # flow=d.json()['data']['workFlow']
    # stateId=d.json()['data']['stateId']
    # print(type(stateId))
    # print(flow[str(stateId)])
    # u.do_action(type,id,sucess)

