from httprunner import HttpRunner, Config, Step, RunRequest, RunTestCase


class TestCase(HttpRunner):
    config = (
        Config("测试环境-回归主流程：橙券-卡密卡号")
        .base_url("http://logan-gateway.test.logan.xiaopeng.local")
    )

    teststeps = [
        # C端正向流程
        Step(
            RunRequest("创建交易预订单")
            .post("/xp-lark-trade-boot/v1/api/trade/pre/create")
            .with_headers(
                **{
                    "Cookie": "${get_cookies()}"
                }
            )
            .with_params(
                **{
                    "redirectURL": "https:%2F%2Fpmall.cs-pre.xiaopeng.com%2Fproduct%2F1473219860712726529"
                }
            )
            .with_json(
                {
                    "preTradeOrderType": 0,
                    "goodsContent": [
                        {
                            "spuId": "1446768533702807553",
                            "skuId": "1446768534965293058",
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
                    "redirectURL": "https:%2F%2Fpmall.cs-pre.xiaopeng.com%2Forder%2Fconfirm%2F1524943761594118145"
                }
            )
            .with_json(
                {
                    "deviceSource": 1,
                    "source": 0,
                    "returnUrl": "https://pmall.cs-pre.xiaopeng.com/pay/success",
                    "payScene": 2,
                    "preTid": "$preTid",
                    "payType": 0,
                    "useCredit": "$canUseCredit",
                    "useActivity": "$useActivity",
                    "needCredit": "$needCredit",
                    "needPayment": "$needPayment",
                    "clientPreTradeDto": None,
                    "redirectURL": "https://pmall.cs-pre.xiaopeng.com/order/confirm/1525021898076057602"
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
            # Hook机制，设置接口请求后的等待时间
            # .teardown_hook("${sleep(50)}")
            # 提取orderId
            .extract()
            .with_jmespath("body.data.orders[0].orderId", "orderId")
            .with_jmespath("body.data.orders[0].items[0].orderItemId", "orderItemId")
            .validate()
            .assert_equal("body.code", 200, "断言失败")
            .assert_equal("body.msg", "success", "断言失败")
        ),

        Step(
            RunRequest("查询订单详情")
            .setup_hook("${sleep(50)}")
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
            .assert_equal("body.data.orders[0].orderStatus", 35, "断言失败：交易失败")
        ),

        # 后台逆向流程
        Step(
            RunRequest("后台发起主动退款")
            .post("/xp-lark-admin-boot/v1/api/refund/create")
            .with_headers(
                **{
                    "Cookie": "${get_adm_cookies()}"
                }
            )
            .with_json(
                {
                    "tradeId": "$tid",
                    "orderId": "$orderId",
                    "orderItemId": "$orderItemId",
                    "itemNum": 1,
                    # demand = 1为仅退款；2为退货退款；3为换货
                    "demand": 1,
                    "memo": "服务端要求此字段必填，但提交上去的内容会被覆盖为操作人"
                }
            )
            .extract()
            .with_jmespath("body.data.refundId", "refundId")
            .validate()
            .assert_equal("body.code", 200, "断言失败")
            .assert_equal("body.msg", "success", "断言失败")
        ),

        Step(
            RunRequest("售后审核操作")
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
                    "refuseReason": "",
                    "sellerAddressId": "",
                    "giveBackGoodsType": ""
                }
            )
            .validate()
            .assert_equal("body.code", 200, "断言失败")
            .assert_equal("body.msg", "success", "断言失败")
        ),

        Step(
            RunRequest("查询退款单详情")
            # 过两分钟查询售后单详情信息
            .setup_hook("${sleep(60)}")
            .get("/xp-lark-admin-boot/v1/api/refund/info")
            .with_headers(
                **{
                    "Cookie": "${get_adm_cookies()}"
                }
            )
            .with_params(
                **{
                    "refundId": "$refundId"
                }
            )
            .validate()
            .assert_equal("body.code", 200, "断言失败")
            .assert_equal("body.msg", "success", "断言失败")
            .assert_equal("body.data.refund.status", 70, "断言失败：未退款成功")
        )
    ]


if __name__ == '__main__':
    TestCase().test_start()
