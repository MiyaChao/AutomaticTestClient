# import unittest
from script.ZZ1597398638108.XM1598949386052.AuditFunc import *
# from lib.BussinessComm import *
from faker import Faker
import random

class Purchase():
    t = BussinessComm()
    f = Faker('Zh_cn')

    def __init__(self):
        self.atype = 'PurchaseV1'
        publicMethod.setGlobalVariable('atype',self.atype)


    # 创建
    def test_create_purchase(self,applyType=1):
        if int(applyType) ==1:
            price=999.00
        elif int(applyType) == 2:
            price = 4999.00
        elif int(applyType) == 3:
            price = 50000.00
        else:
            raise Exception('applyType参数错误！')
        payload = {
            'goodType':random.randint(1,11),
            'goods[0][name]':self.f.word(),
            'goods[0][specs]':self.f.word(),
            'goods[0][number]':1,
            'goods[0][price]':price,
            'goods[0][unit]':'个',
            'goods[0][total]':price*1,
            'goods[0][description]':''.join(self.f.sentences()),
            'deliveryDate':self.f.future_date()
        }
        fileName, filePath = self.t.upload_file()
        payload['file[0][name]'] = fileName
        payload['file[0][path]'] = filePath

        r=self.t.create(self.atype,payload)
        return r

    # 修改
    def test_update_purchase(self, id, applyType=1):
        if int(applyType) == 1:
            price = 999.00
        elif int(applyType) == 2:
            price = 4999.00
        elif int(applyType) == 3:
            price = 50000.00
        else:
            raise Exception('applyType参数错误！')
        payload = {
            'goodType': random.randint(1, 11),
            'goods[0][name]': self.f.word(),
            'goods[0][specs]': self.f.word(),
            'goods[0][number]': 1,
            'goods[0][price]': price,
            'goods[0][unit]': '个',
            'goods[0][total]': price * 1,
            'goods[0][description]': ''.join(self.f.sentences()),
            'deliveryDate': self.f.future_date()
        }
        fileName, filePath = self.t.upload_file()
        payload['file[0][name]'] = fileName
        payload['file[0][path]'] = filePath

        r = self.t.update(self.atype, id, payload)
        return r


if __name__ == '__main__':
    l = BussinessComm()
    adminUser = ('admin@pvc123.com',
                 'sdc5r9y9owfndtijuhtM52YRDmbIKKGHkEsQ2Lh4HHoJrq0nYtl+nhC8NZ89hVZQvyjw6P/W2Y2EKOR3yST8p5xfSnfU1j59PVNSoGUQfk2AGN+F6k/lO5Ke3Fs4gbjsKkndxCT9xlPPLCdpedP8uVwfyxXjUYbWIPIzhPDXqvY='
                 )
    r1 = l.login_sys(*adminUser)
    atype = 'PurchaseV1'
    c = Purchase()
    c.test_create_purchase(3)
    id = l.get_own_record_id()


    # stateList = l.audit_all_pass(atype,id)
    # print(stateList)
    # unittest.main()

    # 构造测试集
    # suit = unittest.TestSuite()
    #
    #
    # suit.addTest(TestPurchaseV1("test_create"))
    # suit.addTest(TestPurchaseV1("test_audit_pass"))
    # suit.addTest(TestPurchaseV1("test_create"))
    # suit.addTest(TestPurchaseV1("test_audit_fail"))         #
    #
    #
    #
    # runner = unittest.TextTestRunner()
    # runner.run(suit)  # 运行测试用例










