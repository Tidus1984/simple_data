#!/usr/local/bin/python3
"""
app接口下载数据存入数据库
"""
from simple_data.download.baostock_hs300 import baostock_hs300_update



def main():
    baostock_hs300_update()

if __name__=="__main__":
    main()