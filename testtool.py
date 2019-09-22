import hashlib
import pyperclip
import base64
import os
import smtplib
from os import walk
import re
import datetime
import json, shutil, time


# 获取MD5加密的方法
def getMD5(str):
    m = hashlib.md5()
    m.update(str.encode())
    # 获取sign
    sign = m.hexdigest().upper()
    print(sign)
    return sign


# 获取MD5加密，并且进行打印操作的方法
def getMD5AndPrint():
    new_temp = input("******请在此输入需要进行MD5加密的内容******：")
    m = hashlib.md5()
    m.update(new_temp.encode())
    # 获取sign
    sign = m.hexdigest()
    print(sign.upper())
    pyperclip.copy(sign.upper())
    print("以上显示的内容为加密之后的报文；系统已经自动复制内容，如需使用，直接【Ctrl+V】进行粘贴即可")


# ""中为pdf的base64码
def getPDF(base64String, path):
    with open(path, 'wb') as f:
        f.write(base64.b64decode(base64String))


# 获取文件的行数
def getTXTLine(path):
    count = 0
    thefile = open(path)
    while True:
        buffer = thefile.read(1024 * 8192)
        if not buffer:
            break
        count += buffer.count('\n')
    thefile.close()
    # print(count)
    return count


# 获取某一行的字符串
# 这个需要进行优化，根据指定的符号进行不同的切分
def getTXTcontent(filePath, serialNumber):
    # 1.range中填写的数据 跟txt中行数保持一致 默认按照空格分隔(想改成什么都可以在split中改)
    f_space = open(filePath, "r")
    line_space = f_space.readlines()
    # 获取文件名字
    # print(line_space[serialNumber-1].split()[0])
    return line_space[serialNumber - 1].split()[0]
    f_space.close()


# 获取文件夹的中的文件夹和文件夹里文件
def do_file(save_filepath, to_filepath):  # 定义函数 传入写入文档保存的位置和要操作的任意电脑路径
    file = open(save_filepath, "w+")
    # 遍历文件路径
    for parent, dirnames, filenames in walk(to_filepath):
        print(dirnames)
        if 'bin' in dirnames:
            file.write(("\n\n根目录为：{0}~~~~~~").format(parent))
            for dirname in dirnames:
                file.write(("   文件夹：{0}、").format(dirname))
            for filename in filenames:
                file.write(("   文件：{0}、").format(filename))
    file.close()


def get_dir(path):  # 获取目录路径
    for root, dirs, files in os.walk(path):  # 遍历path,进入每个目录都调用visit函数，，有3个参数，root表示目录路径，dirs表示当前目录的目录名，files代表当前目录的文件名
        for dir in dirs:
            # print(dir)             #文件夹名
            print(os.path.join(root, dir))  # 把目录和文件名合成一个路径


def get_file(path):  # 获取文件路径
    for root, dirs, files in os.walk(path):

        for file in files:
            # print(file)     #文件名
            print(os.path.join(root, file))


def get_fileName(save_filepath, to_filepath, filetype='.config'):  # 定义函数 传入写入文档保存的位置和要操作的任意电脑路径，获取文件的路径列表
    file = open(save_filepath, "w+")
    # 遍历文件路径
    for parent, dirnames, filenames in walk(to_filepath):
        # print(dirnames)
        file.write(("\n\n根目录为：{0}~~~~~~").format(parent))
        for dirname in dirnames:
            file.write(("文件夹：{0}、").format(dirname))
        for filename in filenames:
            if os.path.splitext(filename)[1] == filetype:
                file.write(("文件：{0}、").format(filename))
    file.close()
    pyperclip.copy(save_filepath)
    print("请打开文件复制更新内容；******文件路径已经自动复制了，直接打开即可******")


def get_fileNameCustom(save_filepath, to_filepath, filetype='.config'):  # 定义函数 传入写入文档保存的位置和要操作的任意电脑路径，并且获取指定类型的文件名称
    file = open(save_filepath, "w+")
    # 遍历文件路径
    for parent, dirnames, filenames in walk(to_filepath):
        # print(dirnames)
        for dirname in dirnames:
            file.write(("文件夹：{0}\n").format(dirname))
        for filename in filenames:
            if os.path.splitext(filename)[1] == filetype:
                file.write(("{0}\n").format(filename))
    file.close()
    pyperclip.copy(save_filepath)
    print("请打开文件复制更新内容；******文件路径已经自动复制了，直接打开即可******")


# get_fileNameCustom(r"F:\Users\45209\JmeterNEW\运行结果保存\updateList.txt", r"F:\Users\45209\JmeterNEW\运行结果保存",".txt")  # 传入相关的参数即可


a = 0


def counterA(num):
    def f():
        global a
        a = a + 1
        if (a == 1):
            a = a + num
        return a

    return f()


s = [0]


def counterB():
    def f():
        s[0] = s[0] + 1
        return s[0]

    return f


'''
w=counterA()
print("w",w)

m=counterA()
print("m",m)
'''


def increase():  # 定义一个还有自然数算法的生成器,企图使用next来完成不断调用的递增
    n = 0
    while True:
        n = n + 1
        yield n


# it = increase()  # 一定要将生成器转给一个(生成器)对象,才可以完成,笔者第一次做,这里一直出问题,
# 一直没解开,看到别人做的才更改完成
def counter():  # 再定义一内函数
    return next(it)  # 调用生成器的值,每次调用均自增（
    # 注意：it不要加()括号调用会出错的


def sendEmail(toEmailAddress, title, text):  # toEmailAddress收件人，title标题，text内容
    HOST = "smtp.qq.com"  # 定义smtp主机
    SUBJECT = title  # 定义邮件主题
    TO = toEmailAddress  # 定义邮件收件人
    FROM = "***********@qq.com"  # 定义邮件发件人
    text = text  # 邮件的内容
    str = "\r\n"
    seq = {"From:%s" % FROM,
           "To:%s" % TO,
           "Subject:%s" % SUBJECT,
           "", text}
    BODY = str.join(seq)
    print(BODY)
    server = smtplib.SMTP()  # 创建一个SMTP对象
    server.connect(HOST, "25")  # 通过connect方法连接smtp主机
    server.starttls()  # 启动安全传输模式
    server.login("***********@qq.com", "*********")  # 邮件账户登录校验
    server.sendmail(FROM, TO, BODY)  # 邮件发送
    server.quit()  # 断开smtp连接


# 删除文件夹下面，指定类型的文件
def removeFile(dir, postfix):
    if os.path.isdir(dir):
        for file in os.listdir(dir):
            removeFile(dir + r'/' + file, postfix)
            # print(dir+'/'+file,postfix)
    else:
        if os.path.splitext(dir)[1] == postfix:
            os.remove(dir)


def copyPDF(dir):
    Labelhistory = r"F:\Users\zhuangmiaona\面单历史记录\\"
    f_list = os.listdir(dir)
    n = 0
    for fileNAME in f_list:
        if os.path.splitext(fileNAME)[1] == '.pdf':
            n += 1
            oldname = dir + fileNAME
            newname = Labelhistory + fileNAME
            shutil.copyfile(oldname, newname)


def deleteline(file, str1):
    with open(file, "r") as f:
        lines = f.readlines()
    with open(file, "w", encoding="utf-8") as f_w:
        for line in lines:
            if str1 not in line:
                print(line)
                continue
            f_w.write(line)


def replaceWord(file, needReplaceWord, forReplaceWord):
    with open(file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        f.close()
    with open(file, "w+", encoding="utf-8") as f_w:
        for line in lines:
            a = re.sub(needReplaceWord, forReplaceWord, line)
            f_w.writelines(a)
        f.close()


def getday():
    today = datetime.date.today()
    formatted_today = today.strftime('%Y%m%d')
    return formatted_today


def gettime():
    time = datetime.datetime.now()
    formatted_time = time.strftime('%Y%m%d %H%M%S').replace(" ", "")
    return formatted_time


def getMD5Input():
    new_temp = input("******请在此输入需要进行MD5加密的内容******：")
    m = hashlib.md5()
    m.update(new_temp.encode())
    # 获取sign
    sign = m.hexdigest()
    print(sign.upper())
    pyperclip.copy(sign.upper())
    print("以上显示的内容为加密之后的报文；系统已经自动复制内容，如需使用，直接【Ctrl+V】进行粘贴即可")


def getMD5(password):
    m = hashlib.md5()
    m.update(password.encode())
    # 获取sign
    sign = m.hexdigest().upper()
    return sign


def getJsonFormat():
    '''
    该功能主要实现了json自动格式化，根据提示输入需要格式化的代码，系统将自动格式化、打印、并且自动复制
    '''
    requestSTR = input("******请在此输入需要进行JSON格式化的内容******：")
    dicts = json.loads(requestSTR)
    json_dicts = json.dumps(dicts, indent=4)
    print(json_dicts)
    pyperclip.copy(json_dicts)
    print("以上显示的内容为格式化之后的报文；系统已经自动复制内容，如需使用，直接【Ctrl+V】进行粘贴即可")


def getMiddleStr(content, startStr, endStr):  # 获取指定字符串中间的字符
    startIndex = content.index(startStr)
    if startIndex >= 0:
        startIndex += len(startStr)
    endIndex = content.index(endStr)
    return content[startIndex:endIndex]


def getDaygap(startime, endtime=str(datetime.date.today())):  # 计算时间差
    format = '%Y-%m-%d'
    a = datetime.datetime.strptime(startime, format)
    b = datetime.datetime.strptime(endtime, format)
    t1 = time.mktime(a.timetuple()) * 1000 + a.microsecond / 1000
    t2 = time.mktime(b.timetuple()) * 1000 + b.microsecond / 1000
    a = t2 - t1
    b = a / 1000 / 3600
    c = int(b / 24)
    times = "经过了：" + str(c) + "天"
    print(times)
    print(c)
    return c
