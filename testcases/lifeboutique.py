from httprunner import HttpRunner, Config, Step, RunRequest, RunTestCase


class TestCase(HttpRunner):
    config = (
        Config("测试环境-回归主流程:生活精品-椰树牌椰奶")
        .base_url("http://logan-gateway.test.logan.xiaopeng.local")
    )

    teststeps = [
        # 订单正向流程
        Step(
            RunRequest("创建交易订单")
            .post("/xp-lark-trade-boot/v1/api/trade/pre/create")
            .with_headers(
                **{
                    "Cookie": "${get_cookies()}"
                }
            )
            .with_params(
                **{
                    "redirectURL": "http%3A%2F%2Fwww.baidu.com"
                }
            )
            .with_json(
                {
                    "preTradeOrderType": 0,
                    "goodsContent": [
                        {
                            "spuId": "1435415401007611906",
                            "skuId": "1435415402156851201",
                            "consumeAmount": 1,
                            "serviceStoreCode": ""
                        }
                    ]
                }
            )
            .extract()
            # 创建交易预订单-preTid
            .with_jmespath("body.data.preTid", "preTid")
            .validate()
            .assert_equal("body.code", 200, "断言失败")
            .assert_equal("body.msg", "success", "断言失败")
        ),

        Step(
            RunRequest("确认下单前的商品订单")
            .get("/xp-lark-trade-boot/v1/api/trade/pre/info/$preTid")
            .with_headers(
                **{
                    "Cookie": "${get_cookies()}"
                }
            )
            .with_params(
                **{
                    "useCredit": "true",
                    "useCoupon": "true",
                    "buyMode": "",
                    "redirectURL": "https:%2F%2Fpmall.cs-pre.xiaopeng.com%2Forder%2Fconfirm%2F1524943761594118145"
                }
            )
            .extract()
            # 确认下单前的商品订单-needPayment;needCredit;canUseCredit;useActivity
            .with_jmespath("body.data.needPayment", "needPayment")
            .with_jmespath("body.data.needCredit", "needCredit")
            .with_jmespath("body.data.canUseCredit", "canUseCredit")
            .with_jmespath("body.data.useActivity", "useActivity")
            .validate()
            .assert_equal("body.code", 200, "断言失败")
            .assert_equal("body.msg", "success", "断言失败")
        ),

        Step(
            RunRequest("创建交易单")
            .post("/xp-lark-trade-boot/v1/api/trade/create")
            .with_headers(
                **{
                    "Cookie": "${get_cookies()}"
                }
            )
            .with_params(
                **{
                    "redirectURL": "https:%2F%2Fpmall.cs-pre.xiaopeng.com%2Forder%2Fconfirm%2F1522840702524592130"
                }
            )
            .with_json(
                {
                    "deviceSource": 1,
                    "source": 0,
                    "returnUrl": "http://pmall.test.xiaopeng.local/pay/success",
                    "payScene": 2,
                    "preTid": "1527491360458723330",
                    "payType": 0,
                    "useCredit": "$canUseCredit",
                    "useActivity": "$useActivity",
                    "needCredit": "$needCredit",
                    "needPayment": "$needPayment",
                    "clientPreTradeDto": None,
                    "tradeAddress": {
                        "receiverName": "曲奇",
                        "receiverTel": "17820722788",
                        "province": "北京",
                        "provinceCode": "110000",
                        "city": "北京市",
                        "cityCode": "110100",
                        "district": "东城区",
                        "districtCode": "110101",
                        "address": "荔湾区"
                    }
                }
            )
            .extract()
            .with_jmespath("body.data.tid", "tid")
            .validate()
            .assert_equal("body.code", 200, "断言失败")
            .assert_equal("body.msg", "success", "断言失败")
        ),

        Step(
            RunRequest("查询交易单详情")
            .get("/xp-lark-trade-boot/v1/api/trade/info/$tid")
            .with_headers(
                **{
                    "Cookie": "${get_cookies()}"
                }
            )
            .with_params(
                **{
                    "redirectURL": "https:%2F%2Fpmall.cs-pre.xiaopeng.com%2Forder%2Fconfirm%2F1522840702524592130"
                }
            )
            # 提取orderId
            .extract()
            .with_jmespath("body.data.orders[0].orderId", "orderId")
            .with_jmespath("body.data.orders[0].items[0].orderItemId", "orderItemId")
            .validate()
            .assert_equal("body.code", 200, "断言失败")
            .assert_equal("body.msg", "success", "断言失败")
            .assert_equal("body.data.trade.tradeStatus", 5, "断言失败")
        ),

        Step(
            RunRequest("查询订单详情")
            # Hook机制，查询订单状态，设置接口请求前的等待时间:生活精品30s
            .setup_hook("${sleep(10)}")
            .get("/xp-lark-trade-boot/v1/api/order/info/$orderId")
            .with_headers(
                **{
                    "Cookie": "${get_cookies()}"
                }
            )
            .with_params(
                **{
                    "redirectURL": "https:%2F%2Fpmall.cs-pre.xiaopeng.com%2Forder%2Fdetail%2F1525022461846548481"
                }
            )
            .validate()
            .assert_equal("body.code", 200, "断言失败")
            .assert_equal("body.msg", "success", "断言失败")
            # 订单状态变为：“待发货”
            .assert_equal("body.data.orders[0].orderStatus", 5, "断言失败：交易失败")
        ),

        # 发货
        Step(
            RunRequest("查询订单详情")
            # Hook机制，查询订单状态，设置接口请求前的等待时间
            .setup_hook("${sql_insert_send($tid,$orderId)}")
            .get("/xp-lark-trade-boot/v1/api/order/info/$orderId")
            .with_headers(
                **{
                    "Cookie": "${get_cookies()}"
                }
            )
            .with_params(
                **{
                    "redirectURL": "https:%2F%2Fpmall.cs-pre.xiaopeng.com%2Forder%2Fdetail%2F1525022461846548481"
                }
            )
            .teardown_hook("${sleep(40)}")
            .validate()
            .assert_equal("body.code", 200, "断言失败")
            .assert_equal("body.msg", "success", "断言失败")
            # 订单状态变为：“已发货”
            .assert_equal("body.data.orders[0].orderStatus", 15, "断言失败：交易失败")
        ),

        Step(
            RunRequest("订单确认收货")
            .post("/xp-lark-trade-boot/logan/trade/transferToBuyerConfirm")
            .with_headers(
                **{
                    "Cookie": "${get_cookies()}",
                    "logan": "test"
                }
            )
            .with_params(
                **{
                    "orderId": "$orderId"
                }
            )
            .validate()
            .assert_equal("body.code", 200, "断言失败")
            .assert_equal("body.msg", "success", "断言失败")
            # 已确认收货
            .assert_equal("body.data.flag", "true", "断言失败")
        ),

        # 逆向流程-C端申请售后仅退款
        Step(
            RunRequest("创建售后单")
            .post("/xp-lark-trade-boot/v1/api/refund/create")
            .with_headers(
                **{
                    "Cookie": "${get_cookies()}"
                }
            )
            .with_params(
                **{
                    "redirectURL": "https:%2F%2Fpmall.cs-pre.xiaopeng.com%2Forder%2Fdetail%2F1525022461846548481"
                }
            )
            .with_json(
                {
                    "tradeId": "$tid",
                    "orderId": "$orderId",
                    "orderItemId": "$orderItemId",
                    "demand": 1,
                    "itemNum": 1,
                    "reasonId": "aeab5903-2a73-11ec-8d4a-b8599f37f1d8",
                    "refundUserData": {
                        "selectedGoodsStatus": 1,
                        "description": "逆向流程-仅退款",
                        "refundCertificates": [
                            {
                                "type": 1,
                                "url": "https://hd1-pre-www.oss-cn-hangzhou.aliyuncs.com/xp-lark/img/2022-06-20/1655696709804.jpg"
                            }
                        ]
                    }
                }
            )
            # 提取售后单ID
            .extract()
            .with_jmespath("body.data.refundId", "refundId")
            .validate()
            .assert_equal("body.code", 200, "断言失败")
            .assert_equal("body.msg", "success", "断言失败")
        ),

        # 后台拒绝第一次售后仅退款申请
        Step(
            RunRequest("售后单审核操作")
            .post("/xp-lark-admin-boot/v1/api/refund/audit")
            .with_headers(
                **{
                    "Cookie": "${get_adm_cookies()}"
                }
            )
            .with_json(
                {
                    "refundId": "$refundId",
                    "operation": "refuse",
                    "refuseReason": "第一次拒绝售后仅退款",
                    "sellerAddressId": "",
                    "giveBackGoodsType": ""
                }
            )
            .validate()
            .assert_equal("body.code", 200, "断言失败")
            .assert_equal("body.msg", "success", "断言失败")
        ),

        # C端再次申请售后换货
        Step(
            RunRequest("创建售后单")
            .post("/xp-lark-trade-boot/v1/api/refund/create")
            .with_headers(
                **{
                    "Cookie": "${get_cookies()}"
                }
            )

            .with_params(
                **{
                    "redirectURL": "https:%2F%2Fpmall.cs-pre.xiaopeng.com%2Forder%2Fdetail%2F1525022461846548481"
                }
            )
            .with_json(
                {
                    "tradeId": "$tid",
                    "orderId": "$orderId",
                    "orderItemId": "$orderItemId",
                    "demand": 3,
                    "itemNum": 1,
                    "reasonId": "e26c2b2e-2a78-11ec-8d4a-b8599f37f1d8",
                    "refundUserData": {
                        "selectedGoodsStatus": 1,
                        "description": "逆向流程-二次售后换货",
                        "refundCertificates": [
                            {
                                "type": 1,
                                "url": "https://hd1-pre-www.oss-cn-hangzhou.aliyuncs.com/xp-lark/img/2022-06-20/1655696709804.jpg"
                            }
                        ]
                    }
                }
            )
            # 提取售后单ID
            .extract()
            .with_jmespath("body.data.refundId", "refundId")
            .validate()
            .assert_equal("body.code", 200, "断言失败")
            .assert_equal("body.msg", "success", "断言失败")
        ),

        # 后台同意第二次售后换货申请
        Step(
            RunRequest("售后单审核操作")
            .post("/xp-lark-admin-boot/v1/api/refund/audit")
            .with_headers(
                **{
                    "Cookie": "${get_adm_cookies()}"
                }
            )
            .with_json(
                {
                    "refundId": "$refundId",
                    "operation": "agree",
                    "refuseReason": "第一次拒绝售后仅退款",
                    "sellerAddressId": "",
                    "giveBackGoodsType": "2"
                }
            )
        )

    ]


if __name__ == '__main__':
    TestCase().test_start()




# 收货
'''

# 逆向：取消单
Step(
    RunRequest("取消订单")
        .post("/xp-lark-trade-boot/v1/api/cancelOrder/create")
        .with_headers(
        **{
            "Cookie": "${get_cookies()}"
        }
    )
        .with_params(
        **{
            "redirectURL": "https:%2F%2Fpmall.cs-pre.xiaopeng.com%2Forder%2Fdetail%2F1525022461846548481"
        }
    )
        .with_json(
        {
            "tradeId": "T20220524110830610468021",
            "orderId": "1528935949745725442"
        }
    )
        .validate()
        .assert_equal("body.code", 200, "断言失败")
        .assert_equal("body.msg", "success", "断言失败")

),
'''

#


