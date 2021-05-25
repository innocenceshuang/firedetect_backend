from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError

# 传参列表里面的元素必须是str
def sendMessages(devices):
    appid = 1400505540
    appkey = '9b3bacc2ed8ceeaa1cb41c34b47ef332'
    phone_numbers = ["18810700178"]
    template_id = 920308
    sms_sign  = "Morpho的小窝"

    content = ', '.join(devices)
    ssender = SmsSingleSender(appid, appkey)
    params = [content]
    result = ssender.send_with_param(86, phone_numbers[0],template_id, params, sign=sms_sign, extend="", ext="")