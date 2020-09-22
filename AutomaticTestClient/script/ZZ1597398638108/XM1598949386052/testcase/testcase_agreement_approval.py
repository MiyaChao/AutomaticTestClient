from script.ZZ1597398638108.XM1598949386052.AuditFunc import *
import random
from faker import Faker
import time

'''
合同审批
申请-上传合同
'''
class AgreementApproval():
    t = BussinessComm()
    f = Faker('Zh_cn')

    def __init__(self):
        self.atype = 'AgreementApprovalV1'
        publicMethod.setGlobalVariable('atype',self.atype)


    # auditList = [
    #     {'id': 4,
    #      'payload': {
    #          'legalAgreementFile[0][name]': '1.jpg',
    #          'legalAgreementFile[0][path]': imgPath
    #      }
    #      }
    # ]

    # 创建
    def test_create_agreement_approval(self):
        payload = {
            'agreementType':random.randint(1,3),
            'agreementTarget': self.f.word(),
            'companyName':self.f.company(),
            'companyAddress': self.f.address(),
            'companyContactName': self.f.name(),
            'companyJob': self.f.job(),
            'companyPhone': self.f.phone_number(),
            'companyEmail': self.f.email(),
            'agreementPrice':self.f.pyfloat(right_digits=2, positive=True),
            'agreementCondition':self.f.sentence(),
            'agreementPayTime': self.f.future_date(),
            'agreementQuality':self.f.word(),
            'agreementService':'暂无售后',
            'agreementBill':'未开发票',
            'businessContact':self.f.name(),
            'businessJob':self.f.job(),
            'businessPhone':self.f.phone_number(),
            'businessEmail': self.f.email(),
            'businessBankName':'中国银行',
            'businessBank':self.f.credit_card_number(),
            'businessAccount': self.f.company(),
            'payType[checkList][0]': '1',
            # 'payType[checkList][1]': '2',
            # 'payType[checkList][2]': '3',
            'payType[hirePurchaseStatus]': '3',
            'payType[priceList][1]': self.f.pyfloat(right_digits=2, positive=True),
            'payType[priceList][2]': '',
            'payType[priceList][3]': '',
            'ourCompanyName': self.f.company(),
            'ourCompanyPhone':self.f.phone_number(),
            'ourCompanyContact': self.f.name(),
            'ourCompanyJob': self.f.job(),
            'leaderId': '015f574a0101185b7c',
            'userRemark': self.f.sentences()
        }
        fileName, filePath = self.t.upload_file()
        payload['ourCompanyAgreementFile[0][name]'] = fileName
        payload['ourCompanyAgreementFile[0][path]'] = filePath
        r=self.t.create(self.atype, payload)
        return r

    # 修改
    def test_update_agreement_approval(self , id):
        payload = {
            'agreementType':random.randint(1,3),
            'agreementTarget': self.f.word(),
            'companyName':self.f.company(),
            'companyAddress': self.f.address(),
            'companyContactName': self.f.name(),
            'companyJob': self.f.job(),
            'companyPhone': self.f.phone_number(),
            'companyEmail': self.f.email(),
            'agreementPrice':self.f.pyfloat(right_digits=2, positive=True),
            'agreementCondition':self.f.sentence(),
            'agreementPayTime': self.f.future_date(),
            'agreementQuality':self.f.word(),
            'agreementService':'暂无售后',
            'agreementBill':'未开发票',
            'businessContact':self.f.name(),
            'businessJob':self.f.job(),
            'businessPhone':self.f.phone_number(),
            'businessEmail': self.f.email(),
            'businessBankName':'中国银行',
            'businessBank':self.f.credit_card_number(),
            'businessAccount': self.f.company(),
            'payType[checkList][0]': '1',
            # 'payType[checkList][1]': '2',
            # 'payType[checkList][2]': '3',
            'payType[hirePurchaseStatus]': '3',
            'payType[priceList][1]': self.f.pyfloat(right_digits=2, positive=True),
            'payType[priceList][2]': '',
            'payType[priceList][3]': '',
            'ourCompanyName': self.f.company(),
            'ourCompanyPhone':self.f.phone_number(),
            'ourCompanyContact': self.f.name(),
            'ourCompanyJob': self.f.job(),
            'leaderId':'015f574a0101185b7c',
            'userRemark': self.f.sentences(),
            'leaderName': '哈哈01',
            'sponsor': 'admin'
        }
        fileName, filePath = self.t.upload_file()
        payload['ourCompanyAgreementFile[0][name]'] = fileName
        payload['ourCompanyAgreementFile[0][path]'] = filePath
        r=self.t.update(self.atype,id, payload)
        return r






if __name__ == '__main__':
    atype = 'InvoiceV1'
    l = BussinessComm()
    adminUser = ('admin@pvc123.com',
                 'sdc5r9y9owfndtijuhtM52YRDmbIKKGHkEsQ2Lh4HHoJrq0nYtl+nhC8NZ89hVZQvyjw6P/W2Y2EKOR3yST8p5xfSnfU1j59PVNSoGUQfk2AGN+F6k/lO5Ke3Fs4gbjsKkndxCT9xlPPLCdpedP8uVwfyxXjUYbWIPIzhPDXqvY='
                 )
    r1 = l.login_sys(*adminUser)

    c = AgreementApproval()

    r = c.test_create_agreement_approval()
    # id = '015f61aad0000b219c'
    # r = c.test_update_agreement_approval(id)
    print(r.json())
    # id = l.get_own_record_id()










