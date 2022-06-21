from httprunner import HttpRunner, Config, Step, RunRequest, RunTestCase


class TestCase(HttpRunner):
    config = (
        Config("预发环境-回归主流程-XPILOT3.0软件及升级服务")
        .base_url("http://logan-gateway.test.logan.xiaopeng.local/xp-lark-trade-boot")
        )

    teststeps = [
        Step(
            RunRequest("创建交易预订单")
            .post("/v1/api/trade/pre/create")
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
            .with_json({"goodsContent":
                                        [{"consumeAmount": 1, "skuId": "1482903849148588033", "spuId": "1482903848053874690"}],
                        "preTradeOrderType": 0
                        })
            .extract()
            # 创建交易预订单-preTid
            .with_jmespath("body.data.preTid", "preTid")
            .validate()
            .assert_equal("body.code", 200, "断言失败")
            .assert_equal("body.msg", "success", "断言失败")
        ),


        Step(
            RunRequest("确认下单前的商品订单")
            .get("/v1/api/trade/pre/info/$preTid")
            .with_headers(
                **{
                    "Cookie": "${get_cookies()}"
                }
            )
            .with_params(
                **{
                    "redirectURL": "http%3A%2F%2Fwww.baidu.com",
                    "useCredit": "true"
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
            .post("/v1/api/trade/create")
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
                    "needCredit": "$needCredit",
                    "needPayment": "$needPayment",
                    "useCredit": "canUseCredit",
                    "useActivity": "$useActivity",
                    "payScene": 2,
                    "payType": 0,
                    "preTid": "$preTid",
                    "returnUrl": "http://store.xiaopeng.com",
                    "source": 0
                }
            )
            .extract()
            .validate()
            .assert_equal("body.code", 200, "断言失败")
            .assert_equal("body.msg", "success", "断言失败")


        )


    ]


if __name__ == '__main__':
    TestCase().test_start()
