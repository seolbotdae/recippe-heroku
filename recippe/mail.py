from .models import *

from .serializers import *

'''
221117  쪽지함 기능 requestMailList 함수 추가 (추가된 use case)
'''

class ControlMailList_b():
    '''
    수신, 발신한 쪽지들을 가져오는 메소드

    page:int 

    return type List<Mail>
    '''
    def requestMailList(self, page):
        pass

    '''
    sendResult

    result:int
    mailList:List<Mail>

    return type void -> 바꿔야함
    '''
    def sendResult(self, result, mailList):
        pass

class ControlMail_b():
    pass