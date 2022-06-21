import json
import  debugtalk
"""
tid = 'T20220424102640539793298'
content = {
    "DATA": [
        {
            "BSTKD": "T20220424102640539793255",
            "ITEMS": [
                {
                    "LGORT": "D009",
                    "ZWLDH": "1304463068301",
                    "ZWLGS":"jd",
                    "MATNR": "4030310DB1-ZZ-01",
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

content["DATA"][0]['BSTKD'] = tid
content_js = json.dumps(content)
print(type(content_js))
print(content_js)


# 将json类型转换为dict类型
content_str = json.loads(s=content)
print(content_str)
"""
tid = 'T20220524105153144851598'
orderId = '1528931765168316418'
debugtalk.sql_insert_send(tid,orderId)









