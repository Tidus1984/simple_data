#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
检测: pip 有无安装
检测: 需要三方库 有无安装
初始化参数

"""
import os,re

CONFIG_FILE='../config.ini'
APP = 'pip'  # Linux需要有pip安装
URL = r'https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple/'  #清华镜像网站
# 第三方库
LIBS = ['pandas',\
		'zmail',\
		"akshare",\
		"baostock",\
		"configparser"\
		]

def check_app():
	res = os.popen("{0} -V".format(APP)).read()
	if res != '':  # 成功安装
		pass
	else:
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
    # TODO 检测config.ini config不在新建
    # https://github.com/Tidus1984/AV_Data_Capture/blob/master/ADC_function.py
    #
    # 学习 configparser 模块
    # https://docs.python.org/zh-cn/3/library/configparser.html
    # 存储到db数据库内
    pass

def main():
	# 1. pip 有无安装
	check_app()
	# 2. 第三方库检测没有安装
	check_Installed(LIBS)
	# 3. config.ini 初始化参数
	# 4. 检测config.ini 填写是否正确，排除#注释
	# 5. 检测网络 
	

if __name__ == "__main__":
	main()
