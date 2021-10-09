#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
检测: pip3 有无安装
检测: 需要三方库 有无安装
初始化参数

"""
import os,re,configparser,sqlite3

CONFIG_FILE = os.path.join(os.path.abspath(".."),"config.ini")
APP = 'pip3'  # Linux需要有pip3安装
URL = r'https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple/'  #清华镜像网站
# 第三方库
LIBS = [
	'pandas',\
	'zmail',\
	'akshare',\
	'baostock',\
	'configparser',\
	'requests',\
	'zmail'
	]

def check_app():
	res = os.popen("{0} -V".format(APP)).read()
	if res == '':  # 没有成功安装抛出异常
		raise Exception("{0} 没有安装\n请先安装 {0}".format(APP))

def _sep(s):
	# s --> 'pandas                            1.4.4'
    s = re.sub(r'\s+',' ', s).strip()
    return s.split(' ')

def _getDict(command = APP):
    alllib = os.popen(f"{command} list").read()  # str
    alist = alllib.splitlines()  # list
    assert len(alist) > 2, alllib  # 断言如果不满足print alllib
    alist = alist.__iter__()  # alist生成迭代器liter()也可以
    assert next(alist).startswith('Package'), alllib  # 跳过第一行str Package
    assert next(alist).startswith('---'), alllib  # 跳过第二行str  ---
    # map(_sep, alist)
    # [ ['appdirs', '1.4.4'],['akshare', '0.8.70'], ... ,['astroid', '2.5.6'] ]
    # 嵌套列表转换dic
    # https://www.pythonf.cn/read/61002#2.dict%E8%BD%ACList
    return dict(map(_sep, alist))

def check_Installed(LIBS):
    libdict = _getDict()
    for lib in LIBS:
        if lib not in libdict:  # libdict.keys()也可以
                os.system('sudo %s install %s -i %s'%(APP,lib,URL))
        else:
        	pass
        	# print(f"{lib}第三方库已经安装")

def check_config():
    # 检测config.ini
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE,"w") as code:
            print("[common]",file=code)
            print("# 管理员邮箱",file=code)
            print("admin_mail_address =",file=code)
            print("# 域名",file=code)
            print("url = ",file=code)
            print("# 自动发邮件邮箱地址",file=code)
            print("mail_address =",file=code)
            print("# 邮箱pop3密码",file=code)
            print("mail_passwd =",file=code)
            pwd = os.getcwd()  # 当前目录
            father_path=os.path.abspath(os.path.dirname(pwd)+os.path.sep+".")  # 父目录
            db_path = os.path.join(father_path,"db")
            print("# 数据库路径",file=code)
            print(f"DB_PATH = {db_path}",file=code)
            print("新建 config.ini 请填写参数")
    # 检测config.ini 参数有无填写
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    # print(config["common"]['admin_mail_address'],config["common"]['url'],config["common"]['mail_address'],config["common"]['mail_passwd'])
    assert config["common"]['admin_mail_address'] !='',"config.ini admin_mail_address 未填写"
    assert config["common"]['url'] !='',"config.ini url 未填写"
    assert config["common"]['mail_address'] !='',"config.ini mail_address 未填写"
    assert config["common"]['mail_passwd'] !='',"mail_passwd 未填写"

def check_web():
    import requests
    dic = {"国内网络":\
                ["https://www.baidu.com","https://www.sogou.com"],\
            "国外网路":\
                ["https://www.google.com"]
    	  }
    for web in dic.keys():
        for url in dic[web]:
            r = requests.get(url)
            if r.status_code !=200:
                print("{0}: {1}连接发生问题请检测网路".format(web,url))
            # print(f"检查{web} ： {url}")

def creat_sqlite3_db(db_name = "stock.db"):
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    db_file = os.path.join(config["common"]['DB_PATH'],db_name)
    # print(os.path.abspath(db_file))
    if not os.path.exists(db_file):
        conn = sqlite3.connect(db_file)
        # 初始化MAIL_CLIENT客户邮箱 自动插入id
        sql = """
        CREATE TABLE IF NOT EXISTS MAIL_CLIENT
        (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        邮箱 text,
        时间 text,
        策略 text,
        备注 text)
        """
        conn.execute(sql)
        # 初始化MAIL_MSG记录邮件基本信息 设置外键
        # id INTEGER PRIMARY KEY AUTOINCREMENT
        sql = """
        CREATE TABLE IF NOT EXISTS MAIL_MSG
        (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        模块 text,
        日期 text,
        时间 text,
        邮箱 text,
        内容 text)
        """
        conn.execute(sql)

        # 初始化MAIL_AD记录管理员邮箱
        sql = """
        CREATE TABLE IF NOT EXISTS MAIL_AD
        (邮箱 text,
        时间 text,
        备注)
        """
        conn.execute(sql)
        conn.close()
    else:
        pass
        # print(f"无需创建初始化数据库{db_name}路径{db_file}")

def main():
    # 只能ubuntu20.04系统
	# 1. pip3 有无安装
	check_app()
	# 2. 第三方库检测没有安装
	check_Installed(LIBS)
	# 3. config.ini 初始化检测参数有无正确填写
	check_config()
	# 4. 检测网络
	check_web()
	# 5. 初始化数据库和表格
	creat_sqlite3_db()

if __name__ == "__main__":
    main()
