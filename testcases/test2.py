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
        )
    ]


if __name__ == '__main__':
    TestCase().test_start()
