from pathlib import Path
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException   # ← 新增


driver = webdriver.Edge()
try:
    here = Path(__file__).resolve().parent
    page = here.parent / "pages" / "waits.html"
    driver.get(page.resolve().as_uri())

    wait_seconds = 5
    wait = WebDriverWait(driver, wait_seconds)

    # 触发异步插入；presence 只保证 DOM 中存在
    driver.find_element(By.ID, "insert-start").click()
    inserted = wait.until(EC.presence_of_element_located((By.ID, "inserted")))
    assert inserted.text == "延迟插入完成"

    # 触发已有元素显示；visibility 还要求元素可见
    driver.find_element(By.ID, "show-start").click()
    visible = wait.until(EC.visibility_of_element_located((By.ID, "hidden-result")))
    assert visible.text == "延迟显示完成"

    # 等按钮从 disabled 变为可点击
    driver.find_element(By.ID, "enable-start").click()
    button = wait.until(EC.element_to_be_clickable((By.ID, "delayed-button")))
    button.click()
    result = wait.until(EC.visibility_of_element_located((By.ID, "click-result")))
    assert result.text == "延迟按钮已点击"

    print("三种动态状态均验证通过")
    time.sleep(5)

except TimeoutException:                          # ← 专门抓等待超时
    print(f"❌ 等待超时：最长等待 {wait_seconds} 秒仍未满足条件。")
    print("   原因可能是：等待时间设置过短，或页面延迟比等待时间更长。")
    driver.save_screenshot(str(Path(__file__).with_suffix(".png")))
    raise

except Exception:
    driver.save_screenshot(str(Path(__file__).with_suffix(".png")))
    raise

finally:
    driver.quit()