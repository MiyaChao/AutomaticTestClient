# import unittest
from script.ZZ1597398638108.XM1598949386052.AuditFunc import *
# from lib.BussinessComm import *
from faker import Faker


'''
名片印制
'''
class Card():

    t = BussinessComm()
    f = Faker('Zh_cn')
    # atype='CardV1'

    def __init__(self):
        self.atype = 'CardV1'
        publicMethod.setGlobalVariable('atype',self.atype)

    # def card_info(self):
    #     self.atype = 'CardV1'
    #     return self.atype

    # 创建
    def test_create_card(self):
        payload = {
            'phone': self.f.phone_number(),
            'email': self.f.email(),
            'number': self.f.random_digit_not_null(),
            'job': self.f.job()
        }
        r = self.t.create(self.atype,payload)
        # print(r.json())
        return r

    def test_update_card(self, id):

        payload = {
            'phone': self.f.phone_number(),
            'email': self.f.email(),
            'number': self.f.random_digit_not_null(),
            'job': self.f.job(),
            'cardRemark': self.f.text()
        }
        r = self.t.update(self.atype,id, payload)
        return r


    def create_payload(self):
        payload = {
            'phone': self.f.phone_number(),
            'email': self.f.email(),
            'number': self.f.random_digit_not_null(),
            'job': self.f.job()
        }
        return payload



    # def test_audit_pass(self,id):
    #     act = "success"
    #     payload = {'id': id, 'reason': '同意'}
    #     r = self.t.audit_act(self.atype,id,act,payload)
    #     print(r.json())
    #     return r
    #
    # def test_audit_back(self, id):
    #     act = "back"
    #     payload = {'id': id, 'reason': '不同意，重新填写'}
    #     r = self.t.audit_act(atype,id,act,payload)
    #     return r
    # #
    # def test_audit_cancel(self,id):
    #     act = "cancel"
    #     payload = {'id': id, 'reason': '不同意，退回！'}
    #     r = self.t.audit_act(atype, id, act,payload)
    #     return r



if __name__ == '__main__':
    l=BussinessComm()
    adminUser = ('wang@qq.com',
                 'dlhVBnlYrba25NJSj6R7wjkramZn1GI6DAkcLkQ9p/7T0fm09uzqXgiHR+lcwb0NC1JTSWx0jAa6cmK0wN00yG3fD6yM2wjqzWajwmfkYTLnCVZ3AE0opjw8txgfh9/ejNLtOGpazE6n9A82rPdRGNx5UjhNgKOZr60oH/oJwMk='
                 )
    r1 = l.login_sys(*adminUser)
    atype = 'CardV1'
    c=Card()
    c.test_create_card()
    id = l.get_own_record_id()
    # l.call_back(id)
    # c.test_update_card(id)


    stateList = l.audit_all_pass(atype,id)
    # print(f'stateList:{stateList}')
    # c.test_audit_pass(id)
    # unittest.main()
    #
    # # 构造测试集
    # suit = unittest.TestSuite()
    #
    # suit.addTest(Card("test_create_card"))
    # suit.addTest(Card("test_audit_pass"))
    #
    # # suit.addTest(TestCardV1("test_audit_fail"))         #
    #
    # runner = unittest.TextTestRunner()
    # runner.run(suit)  # 运行测试用例










