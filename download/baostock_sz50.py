#!/usr/local/bin/python3
"""
作用: 1. 每日baostock接口更新上证50组成成分
      2. 存入数据库./db/stock.db BAOSTOCK_SZ50表中
用法:
- baostock_sz50_update()
    - 每日更新上证50组成成分从baostock
    - updateDate    |   code    |   code_name
        2021-10-18     sh.603986     兆易创新

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

def baostock_sz50_update(sql_table_name = "BAOSTOCK_SZ50"):
    # 从baostock下载上证50成分
    lg = bs.login()  # 登陆
    rs = bs.query_sz50_stocks()
    sz50_stocks = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        sz50_stocks.append(rs.get_row_data())
    df = pd.DataFrame(sz50_stocks, columns=rs.fields)
    conn = sqlite3.connect(DB_NAME)
    # 如果没有 BAOSTOCK_SZ50 tables
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
        else:  # sz50数据表更新
            if df.shape[0] == 50:
                df.to_sql(sql_table_name, conn, if_exists="replace",index=False)
                # print(f"{sql_table_name}更新")
            else:
                print(df)
                raise Exception(f"{os.path.abspath(__file__)}模块: baostock下载数据错误")

if __name__ == "__main__":
    baostock_sz50_update()