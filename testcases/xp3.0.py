from httprunner import HttpRunner, Config, Step, RunRequest, RunTestCase


class TestCase(HttpRunner):
    config = (
        Config("预发环境-回归主流程-XPILOT3.0软件及升级服务")
        .base_url("https://pmall.cs-pre.xiaopeng.com")
    )

    teststeps = [
        Step(
            RunRequest("创建交易预订单")
            .post("/api/trade/pre/create")
            .with_headers(
                **{
                    "Cookie": "${get_cookies()}"
                }
            )
            .with_params(
                **{
                    "redirectURL": "https:%2F%2Fpmall.cs-pre.xiaopeng.com%2Fproduct%2F1272458064570126337"
                }
            )
            .with_json(
                {"goodsContent":
                     [{"spuId": "1272458064570126337", "skuId": "1483383418826833922", "consumeAmount": 1, "serviceStoreCode": ""}],
                 "preTradeOrderType": 0,
                 "redirectURL": "https://pmall.cs-pre.xiaopeng.com/product/1272458064570126337",
                 "_csrf": "vHNGipvP-aXX5oG6AAAnSGPe0YHVkmjeIqFY"
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
            .get("/api/trade/pre/info/$preTid")
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
                    "redirectURL": "https:%2F%2Fpmall.cs-pre.xiaopeng.com%2Forder%2Fconfirm%2F1522780459270672386"
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
