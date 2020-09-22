import unittest
from script.ZZ1597398638108.XM1598949386052.AuditFunc import *
# from lib.BussinessComm import *
from faker import Faker

class TestCardV1(unittest.TestCase):
    def setUp(self):
        self.l = Login()
        self.l.login_sys(*adminUser)

    def login_out(self):
        self.l.login_out()


    f = Faker('Zh_cn')


    atype='CardV1'
    # flowId = '015e95acb103520384'
    #
    t = BussinessComm(atype)

    # 创建
    def test_create_CardV1(self):
        payload = {
            'phone': self.f.phone_number(),
            'email': self.f.email(),
            'number': self.f.random_digit_not_null(),
            'job': self.f.job()
        }
        r = self.t.create(payload)
        self.assertEqual(r.json()['message'],'申请成功!')
        print('测试提交申请')

    def test_audit_pass(self):
        r = self.t.audit_pass()
        # print(f'{currentFlow}_测试审核通过流程')
        self.assertEqual(r, True)

    # def test_audit_fail(self):
    #     r = self.t.audit_fail(n=2)
    #     self.assertEqual(r, True)

if __name__ == '__main__':
    # unittest.main()

    # 构造测试集
    suit = unittest.TestSuite()

    suit.addTest(TestCardV1("test_create_CardV1"))
    suit.addTest(TestCardV1("test_audit_pass"))

    # suit.addTest(TestCardV1("test_audit_fail"))         #

    runner = unittest.TextTestRunner()
    runner.run(suit)  # 运行测试用例










