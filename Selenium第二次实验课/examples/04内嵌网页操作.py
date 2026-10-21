from pathlib import Path
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Edge()

try:
    here = Path(__file__).resolve().parent
    page = here.parent / "pages" / "contexts.html"

    driver.get(page.resolve().as_uri())
    driver.maximize_window()
    wait = WebDriverWait(driver, 5)

    # ========== 1. 查看主页面 ==========
    main = driver.find_element(By.ID, "main-marker")
    print("① 找到主页面元素：", main.text)

    print("请观察网页中的 iframe 输入框")
    time.sleep(3)

    # ========== 2. 未切换时查找 iframe 内元素 ==========
    print("\n② 不切换 iframe，直接查找里面的输入框")

    try:
        driver.find_element(By.ID, "frame-input")
    except NoSuchElementException:
        print("找不到输入框！")
        print("虽然浏览器能显示它，但 Selenium 当前只在主页面查找")
    else:
        raise AssertionError("页面结构与预期不符，请检查输入框是否位于 iframe 内")

    time.sleep(3)

    # ========== 3. 切换到 iframe ==========
    wait.until(
        EC.frame_to_be_available_and_switch_to_it(
            (By.ID, "practice-frame")
        )
    )

    print("\n③ 已切换到 iframe，现在再次查找同一个输入框")

    input_box = wait.until(
        EC.visibility_of_element_located((By.ID, "frame-input"))
    )

    input_box.send_keys("现在可以找到 iframe 内的输入框了")
    print("找到成功，并输入文字！")
    time.sleep(3)

    # ========== 4. 提交并验证 ==========
    driver.find_element(By.ID, "frame-submit").click()

    expected = "子页面收到：现在可以找到 iframe 内的输入框了"

    wait.until(
        EC.text_to_be_present_in_element(
            (By.ID, "frame-result"),
            expected
        )
    )

    actual = driver.find_element(By.ID, "frame-result").text
    assert actual == expected, "iframe 提交结果不正确"

    print("\n④ 提交结果：", actual)
    print("断言通过")
    time.sleep(3)

    # ========== 5. 在 iframe 内查找主页面元素 ==========
    print("\n⑤ 仍在 iframe 内，尝试查找主页面标记")

    try:
        driver.find_element(By.ID, "main-marker")
    except NoSuchElementException:
        print("找不到主页面标记！")
        print("当前查找范围是 iframe 子页面，需要先切回主页面")
    else:
        raise AssertionError("页面结构与预期不符，请检查主页面标记的位置")

    time.sleep(3)

    # ========== 6. 返回主页面 ==========
    driver.switch_to.default_content()

    main = driver.find_element(By.ID, "main-marker")
    assert main.text == "当前位于主页面", "主页面标记不正确"

    print("\n⑥ 已返回主页面，重新找到标记：", main.text)
    print("iframe 切换练习完成；当前仍在主页面")
    time.sleep(5)

    # ========== 7. 点击按钮打开独立的新窗口 ==========
    original_handle = driver.current_window_handle
    handles_before = set(driver.window_handles)
    driver.find_element(By.ID, "open-window").click()
    wait.until(EC.new_window_is_opened(handles_before))

    # 用新旧句柄集合的差找到新窗口，不假设固定列表下标。
    new_handles = set(driver.window_handles) - handles_before
    assert len(new_handles) == 1, f"预期新开一个窗口，实际新增 {len(new_handles)} 个"
    new_handle = new_handles.pop()
    driver.switch_to.window(new_handle)
    print("\n⑦ 已切换到独立新窗口：", driver.title)
    time.sleep(5)

    # 验证新窗口自己的标题和页面反馈。
    assert driver.title == "练习新窗口", "新窗口标题不正确"
    window_text = wait.until(
        EC.visibility_of_element_located((By.ID, "window-result"))
    ).text
    assert window_text == "新窗口已准备就绪", "新窗口内容不正确"
    print("⑧ 新窗口内容验证通过：", window_text)
    time.sleep(5)

    # 关闭新窗口后，显式切回最初的主窗口。
    driver.close()
    driver.switch_to.window(original_handle)
    main = driver.find_element(By.ID, "main-marker")
    assert main.text == "当前位于主页面", "返回后的主页面标记不正确"
    print("⑨ 已关闭新窗口并返回主页面：", main.text)
    time.sleep(5)

except Exception:
    driver.save_screenshot(str(Path(__file__).with_suffix(".png")))
    raise

finally:
    driver.quit()
