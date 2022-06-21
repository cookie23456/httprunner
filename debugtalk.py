import time
import pymysql
import json
from httprunner import __version__



def get_httprunner_version():
    return __version__


def sum_two(m, n):
    return m + n


def sleep(n_secs):
    time.sleep(n_secs)


def get_cookies():
    # 注意相对路径的使用，要回溯到debugtalk所在目录的上一级再去寻找cookie_init.txt
    with open('D:\\HrunProject\\cookie_init.txt', 'r', encoding='utf-8') as f:
        cookies = f.read()
        return cookies


def get_adm_cookies():
    # 注意相对路径的使用，要回溯到debugtalk所在目录的上一级再去寻找cookie_init.txt
    with open('D:\\HrunProject\\adm_cookie_init.txt', 'r', encoding='utf-8') as f:
        adm_cookies = f.read()
        return adm_cookies


def sql_select_order_no(tid):
    # 打开数据库连接
    db = pymysql.connect(host='rm-bp1x0ypop4kx4z2qbto.mysql.rds.aliyuncs.com',
                        user='xp_flamingo',
                        password='Os4UoXDPSctZU3Af',
                        database='xp_flamingo',
                        cursorclass=pymysql.cursors.DictCursor
                        )
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # SQL查询语句
    sql = "select * from chengquan_coupon where tid='%s'"%(tid)
    cursor.execute(sql)
    result = cursor.fetchone()
    order_no = result.get('user_order_no')
    db.close()
    return order_no

# 一件代发发货
def sql_insert_send(tid, orderId):
    # 打开数据库连接
    db = pymysql.connect(host='rm-bp1x0ypop4kx4z2qbto.mysql.rds.aliyuncs.com',
                         user='xp_flamingo',
                         password='Os4UoXDPSctZU3Af',
                         database='xp_flamingo',
                         cursorclass=pymysql.cursors.DictCursor
                         )
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    content_dict = {
        "DATA": [
            {
                "BSTKD": "",
                "ITEMS": [
                    {
                        "LGORT": "D009",
                        "ZWLDH": "1304463068301",
                        "ZWLGS": "jd",
                        "MATNR": "YN888",
                        "ZREVS4": "X",
                        "POSNR": "000010",
                        "VBELN": "0080017484",
                        "WERKS": "2200",
                        "KWMENG": 2,
                        "WADAT_IST": "20201230"}
                ],
                "ZBSTKD": 1518053794924920833,
                "ZSFLAG": "X1"
            }
        ],
        "HEADER":
            {
                "BUSID": "XPM0030",
                "RECID": "286ED488C63A1EDB92C99B67645ED48C",
                "DTSEND": "20201230111231",
                "SENDER": "ERP",
                "RECEIVER": "XP-MALL"
            }
    }
    content_dict["DATA"][0]["BSTKD"] = tid

    # orderId = int(orderId)
    content_dict["DATA"][0]["ZBSTKD"] = orderId
    content_str = json.dumps(content_dict)

    # SQL查询语句
    sql = "INSERT INTO push_msg(msg_id, biz_id, msg_group, version, content,error_msg, create_time, update_time, is_delete)\
           VALUES (MD5(UUID()), 'XPM0030', 'ERP_MSG', 1609212214919,'%s','', CURRENT_TIME, CURRENT_TIME, 2)"%(content_str)
    cursor.execute(sql)
    db.commit()
    db.close()
    return 0






