from pathlib import Path
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Edge()
try:
    here = Path(__file__).resolve().parent
    page = here.parent / "pages" / "actions.html"
    driver.get(page.resolve().as_uri())
    wait = WebDriverWait(driver, 5)

    print("① 已打开页面，观察 3 秒……")
    time.sleep(3)

    # ===== 悬停菜单 =====
    menu = driver.find_element(By.ID, "menu")
    ActionChains(driver).move_to_element(menu).perform()
    print("② 已悬停菜单，观察 2 秒，看菜单是否展开……")
    time.sleep(2)                      # ← 关键：停在悬停状态，看菜单展开

    # ===== 点下拉项 =====
    item = wait.until(EC.element_to_be_clickable((By.ID, "menu-item")))
    item.click()
    print("③ 已点击下拉项，观察 2 秒，看结果文字……")
    time.sleep(2)

    assert wait.until(EC.visibility_of_element_located((By.ID, "menu-result"))).text == "已选择：课程介绍"
    print("   菜单结果正确")
    time.sleep(1)

    # ===== 输入 + 回车 =====
    keyword = driver.find_element(By.ID, "keyword")
    keyword.send_keys("Selenium")
    print("④ 已输入 Selenium，观察 2 秒，看输入框内容……")
    time.sleep(2)                      # ← 停在输入状态
    keyword.send_keys(Keys.ENTER)
    print("⑤ 已按回车，观察 2 秒，看提交结果……")
    time.sleep(2)

    assert driver.find_element(By.ID, "key-result").text == "已提交：Selenium"
    print("⑥ 悬停菜单和回车提交验证通过")
    time.sleep(5)

except Exception:
    driver.save_screenshot(str(Path(__file__).with_suffix(".png")))
    raise
finally:
    driver.quit()