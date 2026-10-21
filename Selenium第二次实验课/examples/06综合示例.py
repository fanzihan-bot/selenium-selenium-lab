"""
综合案例（慢速观察版）：表单 + 弹窗 + 等待 + 断言。

每一步前后都加了 time.sleep，方便看清：
  - 输入框里文字出现的过程
  - 弹窗弹出、停留、被 accept/dismiss 的过程
  - 结果文字显示的过程

学生可通过改 action、留空输入、故意错预期，观察不同结果。
"""
from pathlib import Path
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def run_case(name, course, action, expected):
    here = Path(__file__).resolve().parent
    page = here.parent / "pages" / "comprehensive.html"

    driver = webdriver.Edge()
    try:
        driver.get(page.resolve().as_uri())
        wait = WebDriverWait(driver, 5)

        print(f"\n===== 用例：name={name!r}, course={course!r}, action={action!r} =====")

        # ---------- 1. 填表单 ----------
        print("① 准备填写姓名……")
        time.sleep(2)

        if name:
            driver.find_element(By.ID, "student-name").send_keys(name)
            print("   已输入姓名：", name)
            time.sleep(2)                              # ← 停，看清姓名输入框
        else:
            print("   姓名为空，不输入")
            time.sleep(1)

        print("   准备填写课程……")
        time.sleep(1)

        if course:
            driver.find_element(By.ID, "course").send_keys(course)
            print("   已输入课程：", course)
            time.sleep(2)                              # ← 停，看清课程输入框
        else:
            print("   课程为空，不输入")
            time.sleep(1)

        # ---------- 2. 点击提交 ----------
        print("② 准备点击提交……")
        time.sleep(2)                                  # ← 停，让你知道"马上要提交了"

        driver.find_element(By.ID, "submit").click()
        print("   已点击提交，弹窗即将出现……")
        time.sleep(2)                                  # ← 停，看弹窗弹出来

        # ---------- 3. 只有表单完整时才会出现确认弹窗 ----------
        if name and course:
            alert = wait.until(EC.alert_is_present())
            print("③ 弹窗已出现，内容：", alert.text)
            time.sleep(3)                              # ← 看清确认弹窗

            # ---------- 4. 处理确认或取消 ----------
            if action == "accept":
                alert.accept()
                print("   已点【确定】，弹窗消失")
            elif action == "cancel":
                alert.dismiss()
                print("   已点【取消】，弹窗消失")
            else:
                raise ValueError(f"完整表单用例的 action 不支持：{action}")
        else:
            # 页面对必填项为空的处理是直接显示错误，不弹确认框。
            if action not in ("empty_name", "empty_course"):
                raise ValueError(f"必填项为空时的 action 不支持：{action}")
            print("③ 表单不完整，页面不弹确认框，直接显示必填错误")

        time.sleep(2)                                  # ← 停，看处理后的页面

        # ---------- 5. 等待并读取结果 ----------
        actual = wait.until(
            EC.visibility_of_element_located((By.ID, "result"))
        ).text
        print("④ 实际结果：", actual)
        print("   预期结果：", expected)
        time.sleep(3)                                  # ← 停，看清结果文字

        # ---------- 6. 断言 ----------
        assert actual == expected, f"预期 {expected!r}，实际 {actual!r}"
        print("⑤ 断言通过")
        time.sleep(2)                                  # ← 最后停留

    except Exception:
        driver.save_screenshot(str(Path(__file__).with_suffix(".png")))
        raise
    finally:
        driver.quit()


# ==================== 用例集 ====================

# 正常用例
run_case("林同学", "selenium", "accept", "报名成功：林同学｜selenium")

# 用例 2：填写完整信息后取消提交
run_case("周同学", "python", "cancel", "已取消提交")

# 用例 3：姓名为空，页面直接显示必填错误
run_case("", "selenium", "empty_name", "提交失败：姓名和课程都必填")

# 用例 4：课程为空，页面直接显示必填错误
run_case("周同学", "", "empty_course", "提交失败：姓名和课程都必填")

# 错误用例 4：故意用错误的预期，观察断言失败（需要时取消注释）
# run_case("林同学", "selenium", "accept", "错误预期文字")

print("\n综合用例全部通过")