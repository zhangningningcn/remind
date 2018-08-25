# -*- encoding:utf-8 -*-

from datetime import date,datetime,timedelta
import smtplib
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import tkinter

try:
    import config
except ImportError:
    import configDemo as config
"""
RD_List = RepaymeltDateList((("a",1),("b",2),("c",3)))
a,b,c是银行名字;1,2,3是还款日

"""

__version__ = "0.1"

class RepaymeltDate(object):
    """RepaymeltDate"""
    def __init__(self, name,dt,payDate = None):
        super(RepaymeltDate, self).__init__()
        if not isinstance(name,str):
            raise ValueError("name mast be srt")
        if not isinstance(dt,int):
            raise ValueError("date mast be int")
        if payDate is None:
            payDate = date(2018,1,1)
        else:
            if not isinstance(payDate,date):
                raise ValueError("Repaymelt date type mast be date")
        self.name = name
        self.date = dt
        self.nextRepaymelt = payDate
    def setNextRepaymelt(self,rp):
        if not isinstance(rp,date):
            raise ValueError("Repaymelt date type mast be date")
        self.nextRepaymelt = rp
        
class RepaymeltDateList(object):
    def __init__(self,arr = None):
        super(RepaymeltDateList, self).__init__()
        self.bank_array = []
        self.iter_index = 0
        if arr:
            for n,d in arr:
                rd = RepaymeltDate(n,d)
                self.bank_array.append(rd)

    def add(self,rd = None,name = None,dt = None):
        if rd == None:
            rd = RepaymeltDate(name,dt)
        self.bank_array.append(rd)

    def __iter__(self):
        self.iter_index = 0
        return self
    def __next__(self):
        if self.iter_index < len(self.bank_array):
            # v,k = (self.bank_array[self.iter_index].name,self.bank_array[self.iter_index].date)
            rd = self.bank_array[self.iter_index]
            self.iter_index += 1

            return rd
        else:
            raise StopIteration
    def __len__(self):
        return len(self.bank_array)

    def sort(self,reverse = False):
        self.bank_array.sort(key = lambda x: x.nextRepaymelt,reverse = reverse)


RD_List = RepaymeltDateList(config.BankList)

def check_date():
    """
    查询所有日期，返回到期列表
    """
    rd_list = RepaymeltDateList()
    for rd in RD_List:
        #print("i={},k={}".format(i,k))
        d,dt = time_remainder(rd.date)
        if d < 4:
            rd.setNextRepaymelt(dt)
            rd_list.add(rd)
    return rd_list

def time_remainder(repayment_date):
    """计算剩余日期
    参数 repayment_date int型 还款日
    """
    today = date.today()

    year = today.year
    month = today.month
    day = today.day

    if day > repayment_date:
        month += 1
        if month > 12:
            month = 1
            year += 1
    #else:
    datetime_repayment_date = date(year,month,repayment_date)
    time_sub = datetime_repayment_date - today
    return time_sub.days,datetime_repayment_date

def send_mail(msg):
    msg = MIMEText(msg, 'plain', 'utf-8')
    msg['From'] = config.emailFromAddr
    msg['To'] = config.emailToAddr
    msg['Cc'] = config.emailCcAddr
    msg['Subject'] = Header('提醒', 'utf-8').encode()
    #print(msg)

    server = smtplib.SMTP(config.smtp_server, config.smtpport)
    #server.set_debuglevel(1)
    server.login(config.emailuser, config.passwdmail)
    server.send_message(msg)
    server.quit()
if __name__ == "__main__":
    rd_list = check_date()
    log_file = open("rd.log","a",encoding="utf-8")
    log_file.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S\n"))
    log_file.write("最近3天有{}张卡还款到期\n".format(len(rd_list)))
    log_str = ""
    if len(rd_list) > 0:
        rd_list.sort()
        msg = "测试程序\n"
        msg += "最近3天有{}张卡还款到期\n".format(len(rd_list) )
        for rd in rd_list:
            info_str = rd.name + ": " + "{}月{}日\n".format(rd.nextRepaymelt.month,rd.nextRepaymelt.day)
            msg += info_str
            log_str += info_str
        try:
            send_mail(msg)
        except Exception as e:
            # 出错后弹出界面提醒
            root = tkinter.Tk()
            w = tkinter.Label(root, text="send mail error")
            w.pack()
            w = tkinter.Label(root, text=str(e))
            w.pack()
            root.mainloop()
    log_str += "\n"
    log_file.write(log_str)
    log_file.close()