from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# 改为 True 后，最后一条断言会故意失败；程序应以失败状态结束。
DEMO_ASSERTION_FAILURE = False

here = Path(__file__).resolve().parent
page = here.parent / "pages" / "assertion_demo.html"
driver = webdriver.Edge()

try:
    driver.get(page.resolve().as_uri())

    # 1. 输入并通过正常页面操作产生实际结果。
    driver.find_element(By.ID, "username").send_keys("testuser")
    driver.find_element(By.ID, "login").click()

    # 2. 读取元素文本，打印实际值，再用 == 比较完整预期文本。
    message = driver.find_element(By.ID, "message")
    actual = message.text
    expected = "登录成功！用户：testuser"
    print("实际结果：", actual)
    print("预期结果：", expected)
    assert actual == expected, "页面提示与预期不一致"
    print("完整文本断言通过")

    # 3. 用 in 检查提示中是否包含关键文字。
    assert "登录成功" in actual, "页面未显示登录成功提示"
    print("关键文字断言通过")

    # 页面结果已显示后停留 5 秒，方便观察浏览器操作。
    time.sleep(5)

    # 4. 可选的故意失败演示。启用后 AssertionError 会向上传递，
    #    不会被捕获后伪装成通过；finally 仍会关闭浏览器。
    if DEMO_ASSERTION_FAILURE:
        wrong_expected = "当前位于子页面"
        print("故意使用错误预期：", wrong_expected)
        assert actual == wrong_expected, "故意演示：实际结果与错误预期不一致"

    print("本次断言测试通过")
except Exception:
    # 失败时保存截图作为辅助记录，然后重新抛出异常保留失败状态。
    driver.save_screenshot(str(Path(__file__).with_suffix(".png")))
    raise
finally:
    driver.quit()
