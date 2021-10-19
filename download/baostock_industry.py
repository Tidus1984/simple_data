#!/usr/local/bin/python3
"""
作用: 1. 每日baostock接口更新行业分类
      2. 存入数据库./db/stock.db BAOSTOCK_INDUSTRY表中
用法:
- baostock_industry_update()
    - 每日从baostock更新行业分类
    - updateDate   code      code_name   industry industryClassification
      2021-10-18 sh.600000    浦发银行    银行        申万一级行业

"""
from simple_data.app import defaults
import configparser,os,sqlite3
import baostock as bs
import pandas as pd

CONFIG_FILE = defaults.CONFIG_FILE
config = configparser.ConfigParser()
config.read(CONFIG_FILE)
DB_NAME = os.path.join(config["common"]['STOCK_PATH'])  # ./db/stock.db

def is_db_table(tb_name):
    # 通过查询数据库失败判断是否有此数据库
    try:
        conn = sqlite3.connect(DB_NAME)
        CMD = "SELECT * FROM " + tb_name
        conn = conn.execute(CMD)
        conn.close()
        return True
    except:
        return False

def baostock_industry_update(sql_table_name = "BAOSTOCK_INDUSTRY"):
    # 从baostock下载行业分类
    lg = bs.login()  # 登陆
    rs = bs.query_stock_industry()
    industry_list  = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        industry_list .append(rs.get_row_data())
    df = pd.DataFrame(industry_list , columns=rs.fields)
    conn = sqlite3.connect(DB_NAME)
    # 如果没有 BAOSTOCK_INDUSTRY tables
    if not is_db_table(sql_table_name):
        df.to_sql(sql_table_name, conn, if_exists="replace",index=False)
        print(f"{os.path.basename(__file__)}模块初始化:\n{DB_NAME}数据库-->{sql_table_name}表")
    else:
        data = pd.read_sql(f"SELECT * from {sql_table_name}",conn)
        a = df["code"].tolist()
        b = data["code"].tolist()
        rs = list(set(a).difference(set(b)))  # a中有而b中没有的
        if rs == []:
            pass  # 完全一样不用更新
            # print(f"{os.path.abspath(__file__)}模块不需要更新")
        else:  # BAOSTOCK_INDUSTRY 数据表更新
            if df.shape[0] >= 3000:
                df.to_sql(sql_table_name, conn, if_exists="replace",index=False)
            else:
                print(df)
                raise Exception(f"{os.path.abspath(__file__)}模块: baostock下载数据错误")

if __name__ == "__main__":
    baostock_industry_update()