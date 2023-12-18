from httprunner import HttpRunner, Config, Step, RunRequest, RunTestCase


class TestCase(HttpRunner):
    config = (
        Config("测试环境-回归主流程：橙券-直充")
        .base_url("http://logan-gateway.test.logan.xiaopeng.local")
        .variables(
            **{
                "tid": "T20220524105642381491156",
                "orderId": '1528932979993944066'
            }
        )
    )

    teststeps = [
        Step(
            RunRequest("催发货")
            .post("/xp-lark-trade-boot/v1/api/trade/urgeDelivery")
            .with_headers(
                **{
                    "Cookie": "${get_cookies()}"
                }
            )
            .with_params(
                **{
                    "tid":"T20220602095821877214579",
                    "orderId":"1532179788651872257",
                    "redirectURL": "https:%2F%2Fpmall.cs-pre.xiaopeng.com%2Forder%2Fdetail%2F1525022461846548481"
                }
            )
            .validate()
            .assert_equal("body.code", 200, "断言失败")
            .assert_equal("body.msg", "success", "断言失败")
        ),

        Step(
            RunRequest("催发货")
            .post("/xp-lark-trade-boot/v1/api/trade/urgeDelivery")
            .with_headers(
                **{
                    "Cookie": "${get_cookies()}"
                }
            )
            .with_params(
                **{
                    "tid": "T20220602095821877214579",
                    "orderId": "1532179788651872257",
                    "redirectURL": "https:%2F%2Fpmall.cs-pre.xiaopeng.com%2Forder%2Fdetail%2F1525022461846548481"
                }
            )
            .validate()
            .assert_equal("body.code", 200, "断言失败")
            .assert_equal("body.msg", "success", "断言失败")
        )
    ]


if __name__ == '__main__':
    TestCase().test_start()
