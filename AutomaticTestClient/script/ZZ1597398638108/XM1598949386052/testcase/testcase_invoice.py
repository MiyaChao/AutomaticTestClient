
from script.ZZ1597398638108.XM1598949386052.AuditFunc import *
import random
from faker import Faker
import time
'''
请款单

'''

class Invoice():
    t = BussinessComm()
    f = Faker('Zh_cn')

    def __init__(self):
        self.atype = 'InvoiceV1'
        publicMethod.setGlobalVariable('atype',self.atype)

    # 创建
    # isComplete=0:资料不全
    # isComplete=1:资料齐全
    def test_create_invoice(self, isComplete=0):

        payload = {
            'reason': '',
            'use[0]': self.f.word(),
            'money[0]': 99.99,
            'totalMoney': 99.99,
            'totalMoneyChinese': '玖拾玖元玖角玖分',
            'currency': random.randint(1, 2),
            'mainCompany': random.randint(1, 9),
            'chargeCompany': self.f.company(),
            'chargeAccount': self.f.credit_card_number(),
            'chargeBank': '平安银行',
            'isComplete': isComplete,                    # 资料不齐
            'type': random.randint(1, 25),
            'loan': self.f.pyfloat(right_digits=2, positive=True),
            'refund': self.f.pyfloat(right_digits=2, positive=True),
            'remark': self.f.text(),
            'departmentId':42,
            'departmentName':'塑化材料中心',
            'planNo':''
        }
        if int(isComplete)==1:
            fileName, filePath = self.t.upload_file()
            payload['file[0][name]']=fileName
            payload['file[0][path]']=filePath
        r = self.t.create(self.atype,payload)

        return r

    # 编辑
    def test_update_invoice(self, id,isComplete=0):

        payload = {
            # 'reason': '',
            'payStatus': '0',
            'use[0]': self.f.word(),
            'money[0]': 99.99,
            'totalMoney': 99.99,
            'totalMoneyChinese': '玖拾玖元玖角玖分',
            'currency': random.randint(1, 2),
            'mainCompany': random.randint(1, 9),
            'chargeCompany': self.f.company(),
            'chargeAccount': self.f.credit_card_number(),
            'chargeBank': '平安银行',
            'isComplete': isComplete,  # 资料不齐
            'type': random.randint(1, 25),
            'loan': self.f.pyfloat(right_digits=2, positive=True),
            'refund': self.f.pyfloat(right_digits=2, positive=True),
            'remark': self.f.text(),
            'departmentId': 42,
            'departmentName': '塑化材料中心',
            'planNo': ''
        }
        if int(isComplete) == 1:
            fileName, filePath = self.t.upload_file()
            payload['file[0][name]'] = fileName
            payload['file[0][path]'] = filePath
        r = self.t.update(self.atype, id, payload)

        return r

    def audit_all_pass(self,id):
        stateList = []
        while True:
            stateName, stateStatus = self.t.get_own_state(id)
            print(f'stateName:{stateName},stateStatus:{stateStatus}')
            stateList.append(stateName)

            if stateName in ['结束', '完成', '已结案']:
                return stateList

            detail = self.t.detail(self.atype,id).json()
            stateId  = detail['data']['stateId']
            payload = {'id': id, 'reason': '同意'}
            if int(stateId) >= 4:
                payload = {
                    'id':id,
                    # 'transitions[0]':'4_5_success',
                    'reason':'同意',
                    'departmentId':'43',
                    'mainCompany':'2',
                    'type':'1',
                    'currency':'1',
                    'planNo':'',
                    'departmentName':'技术中心'
                }
                if int(stateId)==8:     # 补充资料
                    fileName, filePath = self.t.upload_file()
                    payload={
                        'id':id,
                        'file[0][name]':fileName,
                        'file[0][path]':filePath,
                        'reason': '同意',
                        'departmentId': '43',
                        'mainCompany': '2',
                        'type': '1',
                        'currency': '1',
                        'planNo': '',
                        'departmentName': '技术中心'
                    }

            r = self.t.audit_act(self.atype, detail, "success", payload)
            assert r.json()['code'] == '000', r.json()
            time.sleep(1)

    # def test_audit_pass(self):
    #     r = self.t.audit_pass(self.auditList)
    #     self.assertEqual(r, True)
    #
    # def test_audit_fail(self):
    #     r = self.t.audit_fail(6, self.auditList)
    #     self.assertEqual(r, True)
    #
    # def test_callBack(self):
    #     r =self.t.callBack()

if __name__ == '__main__':
    atype = 'InvoiceV1'
    l = BussinessComm()
    adminUser = ('admin@pvc123.com',
                 'sdc5r9y9owfndtijuhtM52YRDmbIKKGHkEsQ2Lh4HHoJrq0nYtl+nhC8NZ89hVZQvyjw6P/W2Y2EKOR3yST8p5xfSnfU1j59PVNSoGUQfk2AGN+F6k/lO5Ke3Fs4gbjsKkndxCT9xlPPLCdpedP8uVwfyxXjUYbWIPIzhPDXqvY='
                 )
    r1 = l.login_sys(*adminUser)

    c = Invoice()

    r = c.test_create_invoice_1()
    id = l.get_own_record_id()
    # print(r.json())
    # id = l.get_own_record_id()
    # l.call_back(id)
    # c.test_update_card(id)
    stateList = c.audit_all_pass(id)
    print(f'stateList:{stateList}')
    # unittest.main()

    # 构造测试集
    # suit = unittest.TestSuite()

    # suit.addTest(TestInvoiceV1("test_create_InvoiceV1_1"))
    # suit.addTest(TestInvoiceV1("test_list"))
    # suit.addTest(TestInvoiceV1("test_audit_pass"))

    # suit.addTest(TestInvoiceV1("test_audit_fail"))         #

    # runner = unittest.TextTestRunner()
    # runner.run(suit)  # 运行测试用例










