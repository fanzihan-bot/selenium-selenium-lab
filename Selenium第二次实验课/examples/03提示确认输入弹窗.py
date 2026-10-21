from pathlib import Path
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Edge()
try:
    page = Path(__file__).resolve().parent.parent / "pages" / "dialogs.html"
    driver.get(page.resolve().as_uri())
    wait = WebDriverWait(driver, 5)

    # ===== 1. alert =====
    driver.find_element(By.ID, "alert-btn").click()
    alert = wait.until(EC.alert_is_present())
    print("alert 文字：", alert.text)
    time.sleep(2)
    alert.accept()
    assert wait.until(EC.visibility_of_element_located((By.ID, "feedback"))).text == "alert 已确认"
    time.sleep(1)

    # ===== 2. confirm 点确认 =====
    driver.find_element(By.ID, "confirm-btn").click()
    wait.until(EC.alert_is_present())
    time.sleep(2)
    wait.until(EC.alert_is_present()).accept()
    assert wait.until(EC.visibility_of_element_located((By.ID, "feedback"))).text == "confirm：已确认"
    time.sleep(1)

    # ===== 3. confirm 点取消 =====
    driver.find_element(By.ID, "confirm-btn").click()
    wait.until(EC.alert_is_present())
    time.sleep(2)
    wait.until(EC.alert_is_present()).dismiss()
    assert wait.until(EC.visibility_of_element_located((By.ID, "feedback"))).text == "confirm：已取消"
    time.sleep(1)

    # ===== 4. prompt 输入文字 =====
    driver.find_element(By.ID, "prompt-btn").click()
    prompt = wait.until(EC.alert_is_present())
    time.sleep(2)
    prompt.send_keys("课堂练习")
    time.sleep(2)
    prompt.accept()
    assert wait.until(EC.visibility_of_element_located((By.ID, "feedback"))).text == "prompt：课堂练习"

    print("alert、confirm、prompt 验证通过")
    time.sleep(5)

except Exception:
    driver.save_screenshot(str(Path(__file__).with_suffix(".png")))
    raise
finally:
    driver.quit()