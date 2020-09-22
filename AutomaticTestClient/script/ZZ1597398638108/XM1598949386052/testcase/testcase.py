# import unittest
from script.ZZ1597398638108.XM1598949386052.AuditFunc import *
# from lib.BussinessComm import *
from faker import Faker
import random


def set_global(atype):
    publicMethod.setGlobalVariable('atype', atype)

# -------------名片印制-----------
class Card(BussinessComm):

    f = Faker('Zh_cn')
    def __init__(self):
        self.atype = 'CardV1'
        set_global(self.atype)

    def set_payload(self):
        payload = {
            'phone': self.f.phone_number(),
            'email': self.f.email(),
            'number': self.f.random_digit_not_null(),
            'job': self.f.job(),
            'cardRemark': self.f.text()
        }
        return payload

    # 创建
    def test_create_card(self):
        payload = self.set_payload()
        r = self.create(self.atype,payload)
        return r

    def test_update_card(self, id):

        payload = self.set_payload()
        r = self.update(self.atype,id, payload)
        return r


# ----------------------------请款单---------------------
class Invoice(BussinessComm):
    f = Faker('Zh_cn')

    def __init__(self):
        self.atype = 'InvoiceV1'
        set_global(self.atype)


    def set_payload(self,isComplete):
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
            'isComplete': isComplete,  # 资料不齐
            'type': random.randint(1, 25),
            'loan': self.f.pyfloat(right_digits=2, positive=True),
            'refund': self.f.pyfloat(right_digits=2, positive=True),
            'remark': self.f.text(),
            'departmentId': 42,
            'departmentName': '塑化材料中心',
            'planNo': ''
        }

        if int(isComplete) == 1:        # 资料不齐，上传资料
            fileName, filePath = self.upload_file()
            payload['file[0][name]'] = fileName
            payload['file[0][path]'] = filePath
        return payload

    # 创建
    # isComplete=0:资料不全
    # isComplete=1:资料齐全
    def test_create_invoice(self, isComplete=0):
        payload = self.set_payload(isComplete)

        r = self.create(self.atype,payload)
        return r

    # 编辑
    def test_update_invoice(self, id,isComplete=0):
        payload = self.set_payload(isComplete)

        r = self.update(self.atype, id, payload)
        return r

    def audit_all_pass(self, id):
        stateList = []
        while True:
            stateName = self.get_own_state(id)
            print(f'stateName:{stateName}')
            stateList.append(stateName)

            if stateName in ['结束', '完成', '已结案']:
                return stateList

            detail = self.detail(self.atype,id).json()
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
                    fileName, filePath = self.upload_file()
                    payload['file[0][name]'] = fileName
                    payload['file[0][path]'] = filePath

            r = self.audit_act(self.atype, detail, "success", payload)
            assert r.json()['code'] == '000', r.json()
            time.sleep(1)
# ------------------物品申购------------
class Purchase(BussinessComm):

    f = Faker('Zh_cn')

    def __init__(self):
        self.atype = 'PurchaseV1'
        set_global(self.atype)

    def set_payload(self,applyType):
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
        fileName, filePath = self.upload_file()
        payload['file[0][name]'] = fileName
        payload['file[0][path]'] = filePath
        return payload

    # 创建
    def test_create_purchase(self,applyType=1):
        payload = self.set_payload(applyType)

        r=self.create(self.atype,payload)
        return r

    # 修改
    def test_update_purchase(self, id, applyType=1):
        payload = self.set_payload(applyType)

        r = self.update(self.atype, id, payload)
        return r

class AgreementApproval(BussinessComm):
    f = Faker('Zh_cn')

    def __init__(self):
        self.atype = 'AgreementApprovalV1'
        set_global(self.atype)

    def set_payload(self):
        payload = {
            'agreementType': random.randint(1, 3),
            'agreementTarget': self.f.word(),
            'companyName': self.f.company(),
            'companyAddress': self.f.address(),
            'companyContactName': self.f.name(),
            'companyJob': self.f.job(),
            'companyPhone': self.f.phone_number(),
            'companyEmail': self.f.email(),
            'agreementPrice': self.f.pyfloat(right_digits=2, positive=True),
            'agreementCondition': self.f.sentence(),
            'agreementPayTime': self.f.future_date(),
            'agreementQuality': self.f.word(),
            'agreementService': '暂无售后',
            'agreementBill': '未开发票',
            'businessContact': self.f.name(),
            'businessJob': self.f.job(),
            'businessPhone': self.f.phone_number(),
            'businessEmail': self.f.email(),
            'businessBankName': '中国银行',
            'businessBank': self.f.credit_card_number(),
            'businessAccount': self.f.company(),
            'payType[checkList][0]': '1',
            # 'payType[checkList][1]': '2',
            # 'payType[checkList][2]': '3',
            'payType[hirePurchaseStatus]': '3',
            'payType[priceList][1]': self.f.pyfloat(right_digits=2, positive=True),
            'payType[priceList][2]': '',
            'payType[priceList][3]': '',
            'ourCompanyName': self.f.company(),
            'ourCompanyPhone': self.f.phone_number(),
            'ourCompanyContact': self.f.name(),
            'ourCompanyJob': self.f.job(),
            'leaderId': '015f574a0101185b7c',
            'userRemark': self.f.sentences()
        }
        fileName, filePath = self.upload_file()
        payload['ourCompanyAgreementFile[0][name]'] = fileName
        payload['ourCompanyAgreementFile[0][path]'] = filePath

        return payload


    # 创建
    def test_create_agreement_approval(self):
        payload=self.set_payload()
        r=self.create(self.atype, payload)
        return r

    # 修改
    def test_update_agreement_approval(self, id):
        payload = {
            'leaderName': '哈哈01',
            'sponsor': 'admin'
        }
        payload=dict(self.set_payload(),**payload)
        r=self.update(self.atype,id, payload)
        return r

# --------------------合同审核--------------
class AgreementVerify(BussinessComm):
    f = Faker('Zh_cn')

    def __init__(self):
        self.atype = 'AgreementVerifyV1'
        set_global(self.atype)

    # auditList = [
    #     {'id': 5,
    #      'payload': {
    #          'legalAgreementFile[0][name]': '1.jpg',
    #          'legalAgreementFile[0][path]': imgPath
    #      }
    #      }
    # ]
    #
    def set_payload(self, ttype):
        department = random.choice(self.get_department().json()['data'])
        departmentId,departmentName  = department['value'], department['label']

        payload = {
            'type':ttype,
            'departmentId': departmentId,
            'departmentName':departmentName,
            'agreementName': self.f.sentence(),
            'leaderId': '1',
            'sponsor': self.f.name(),
            'agreementReason': '\n'.join(self.f.sentences()),
            'useAt': '\n'.join(self.f.sentences()),
            'agreementContent': '\n'.join(self.f.sentences()),
            'suggest': self.f.text()
        }
        fileName, filePath = self.upload_file()
        payload['file[0][name]'] = fileName
        payload['file[0][path]'] = filePath
        return payload

    def test_create_agreement_verify(self, ttype=1):
        payload =self.set_payload(ttype)
        r=self.create(self.atype, payload)
        return r

    def test_update_agreement_verify(self, id,ttype=1):
        payload={
            'leaderName':'哈哈01',
            'typeName':'大易直供商',
            'remark:':''

        }
        payload =dict(self.set_payload(ttype),**payload)
        r=self.update(self.atype, id,payload)
        return r

# --------------------业务招待--------------
class Serve(BussinessComm):
    f = Faker('Zh_cn')

    def __init__(self):
        self.atype = 'serve'
        set_global(self.atype)

    def set_payload(self):

        payload = {
            'company':self.f.company(),
            'customerName':self.f.name(),
            'position':self.f.job(),
            'serveTime':self.f.future_date(),
            'serveAddress':self.f.address(),
            'money':'561.19',
            'serveLevel':random.randint(1,3),
            'receptionStaff': ','.join([self.f.name() for i in range(3)]),
            'cause':self.f.text(),
        }
        fileName, filePath = self.upload_file()
        payload['file[0][name]'] = fileName
        payload['file[0][path]'] = filePath
        return payload

    def test_create(self):
        payload =self.set_payload()
        r=self.create(self.atype, payload)
        return r

    def test_update(self, id,):
        # payload = self.set_payload()
        # # payload =dict(self.set_payload(ttype),**payload)
        # r=self.update(self.atype, id,payload)
        # return r
        pass

# --------------------雀喜卡券--------------
class RuYiCard(BussinessComm):
    f = Faker('Zh_cn')

    def __init__(self):
        self.atype = 'RuYiCard'
        set_global(self.atype)

    def set_payload(self):

        payload = {
            'agentName': self.f.name(),
            'phone': self.f.phone_number(),
            'activity': '活动有礼',
            'cardType': random.randint(1,3),
            'money': self.f.pyfloat(left_digits=2,right_digits=2, positive=True),
            'validTime': self.f.future_date(),
            'miniMoney': 1000,
            'useType': '9',
            'applyRemark': self.f.sentences(),
            'applyReason': self.f.text()
        }
        fileName, filePath = self.upload_file()
        payload['file[0][name]'] = fileName
        payload['file[0][path]'] = filePath
        return payload

    def test_create(self):
        payload =self.set_payload()
        r=self.create(self.atype, payload)
        return r

    def test_update(self, id,):
        # payload = self.set_payload()
        # # payload =dict(self.set_payload(ttype),**payload)
        # r=self.update(self.atype, id,payload)
        # return r
        pass

# --------------------雀喜卡券--------------
class QueXiCard(BussinessComm):
    f = Faker('Zh_cn')

    def __init__(self):
        self.atype = 'QueXiCard'
        set_global(self.atype)


    def set_payload(self,ctype=1):

        payload = {
            'type':ctype,
            'nickName':self.f.name(),
            'memberId':self.f.uuid4(),
            'orderNo':self.f.pystr(),
            'cardName':'活动优惠券',
            'money':self.f.pyfloat(left_digits=2,right_digits=2, positive=True),
            'condition':'满减',
            'quantity':'100',
            'user':'全部用户',
            'useType':'全部商品',
            'customTime[0]':'2020-09-13',
            'customTime[1]':'2020-09-18',
            'applyRemark': self.f.sentences(),
            'applyReason': self.f.text(),
            'startTime':'2020-09-13',
            'endTime':'2020-09-18'
        }
        fileName, filePath = self.upload_file()
        payload['file[0][name]'] = fileName
        payload['file[0][path]'] = filePath
        return payload

    def test_create(self,ctype):
        payload =self.set_payload(ctype)
        r=self.create(self.atype, payload)
        return r

    def test_update(self, id,):
        # payload = self.set_payload()
        # # payload =dict(self.set_payload(ttype),**payload)
        # r=self.update(self.atype, id,payload)
        # return r
        pass


if __name__ == '__main__':
    l=BussinessComm()
    adminUser = ('wang@qq.com',
                 'dlhVBnlYrba25NJSj6R7wjkramZn1GI6DAkcLkQ9p/7T0fm09uzqXgiHR+lcwb0NC1JTSWx0jAa6cmK0wN00yG3fD6yM2wjqzWajwmfkYTLnCVZ3AE0opjw8txgfh9/ejNLtOGpazE6n9A82rPdRGNx5UjhNgKOZr60oH/oJwMk='
                 )
    r1 = l.login_sys(*adminUser)

    # ------CardV1--------
    # atype = 'CardV1'
    # c=Card()
    # c.test_create_card()
    # id = l.get_own_record_id()
    # l.call_back(id)
    # c.test_update_card(id)
    # stateList = l.audit_all_pass(atype,id)
    # print(f'stateList:{stateList}')
    # c.test_audit_pass(id)

    # -----合同审批---
    # atype = 'CardV1'
    # c = AgreementApproval()
    # id = l.get_own_record_id()
    # c.test_update_agreement_approval(id)

    # ---------业务招待---------
    # c = Serve()
    # c.test_create()
    # c.test_create_agreement_verify()
    # ---------雀喜卡券---------
    atype = 'QueXiCard'
    c = QueXiCard()
    # flowid = c.get_flow(atype)
    # print(flowid)
    c.test_create(ctype=1)
    id = l.get_own_record_id()
    stateList = l.audit_all_pass(atype, id)
    print(stateList)
    #  ---------塑如意卡券---------
    # atype = 'RuYiCard'
    # c = RuYiCard()
    # c.test_create()

    # id = l.get_own_record_id()

    # stateList = l.audit_all_pass(atype, id)
    # print(stateList)











