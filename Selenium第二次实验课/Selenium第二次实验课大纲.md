# 《软件测试与质量保证》第二次实验指导

## 一、实验前准备

1. 将本文件夹完整解压，保留 `examples` 与 `pages` 的相对目录关系。文件夹中包括教程、实验大纲、综合练习任务、6 个 Python 示例和本地 HTML 页面。
2. 准备 Python 3.9 或更高版本、PyCharm 或其他 Python 编辑器、Google Chrome（也可使用 Microsoft Edge）。
3. 在所用 Python 环境执行 `python -m pip install -U selenium`，再用 `python --version` 和 `python -m pip show selenium` 检查安装。编辑器使用的解释器应与安装 Selenium 的环境一致。
4. 运行 `examples/01断言验证.py`，确认浏览器能启动、访问本地页面并关闭。Selenium 4 通常通过 Selenium Manager 管理驱动；自动获取失败时检查浏览器版本、网络或驱动配置。
5. 用浏览器打开 `pages` 中的本地 HTML 页面，确认页面能正常显示。默认示例使用 Chrome；改用 Edge 时，将 `webdriver.Chrome()` 改为 `webdriver.Edge()`，浏览器选项也要对应替换。

## 二、实验目标

- 使用 `assert` 比较页面实际结果和预期结果，理解 `AssertionError`。
- 区分断言失败与元素找不到、等待超时等脚本执行异常。
- 根据元素是否存在、可见或可点击选择三种显式等待条件。
- 处理 alert、confirm、prompt 并验证页面反馈。
- 切换 iframe 和多个浏览器窗口，操作后返回正确上下文。
- 使用 `ActionChains` 悬停，使用 `Keys` 完成回车提交。
- 组合表单、弹窗、动态等待、断言和截图，形成可复核的自动化验证。

## 三、实验内容与时间安排

本次实验共 90 分钟，不引入 pytest、unittest、Page Object、Allure、Selenium Grid 或持续集成。

| 环节 | 建议用时 |
| --- | ---: |
| 基础回顾与断言 | 10 分钟 |
| 显式等待深化 | 20 分钟 |
| JavaScript 弹窗处理 | 15 分钟 |
| iframe 与多窗口 | 20 分钟 |
| 鼠标键盘操作 | 10 分钟 |
| 综合练习、结果整理与提交 | 15 分钟 |
| 合计 | 90 分钟 |

## 四、实验步骤

1. **基础回顾与断言：运行 `01断言验证.py`。**观察输入用户名、点击按钮、读取提示和 `assert actual == expected` 的过程。脚本还用 `assert "登录成功" in actual` 检查关键词。将 `expected` 改成错误文字，或将 `DEMO_ASSERTION_FAILURE` 改为 `True`，观察 `AssertionError` 并恢复正确预期。断言失败不能被宽泛 `except` 捕获后只打印。

2. **显式等待深化：运行 `02显示等待条件.py`。**在 `pages/waits.html` 中依次观察延迟插入、已有元素延迟显示、按钮延迟启用。分别使用 `presence_of_element_located`、`visibility_of_element_located`、`element_to_be_clickable`。presence 不等于可见，可见也不保证实际点击成功；动态状态主要使用 `WebDriverWait`，`time.sleep()` 只用于课堂观察。

3. **JavaScript 弹窗：运行 `03提示确认输入弹窗.py`。**使用 `EC.alert_is_present()` 等待 alert、confirm、prompt。读取 alert 后 `accept()`；confirm 分别 `accept()` 和 `dismiss()`，验证确认与取消；prompt 使用 `send_keys("课堂练习")` 后确认，验证页面反馈。

4. **iframe：运行 `04内嵌网页操作.py` 的前半部分。**在 `pages/contexts.html` 中，未切换 iframe 时查找子页面输入框应失败；使用 `frame_to_be_available_and_switch_to_it` 切换后输入并提交，断言“子页面收到：现在可以找到 iframe 内的输入框了”，再用 `default_content()` 返回主页面并断言主页面标记。

6. **鼠标键盘：运行 `05鼠标与键盘操作.py`。**用 `ActionChains(driver).move_to_element(menu).perform()` 悬停菜单，点击“课程介绍”并断言结果；在输入框输入 `Selenium`，发送 `Keys.ENTER`，断言“已提交：Selenium”。拖拽为选做内容。

7. **教师综合示例：运行 `06综合示例.py`。**脚本在 `pages/comprehensive.html` 已经演示确认提交、取消提交、姓名为空、课程为空四种场景。教师示例第 1 条使用“林同学”只是演示数据，与下一步作业的业务场景相同。完整表单才弹确认框；任一必填项为空时直接显示“提交失败：姓名和课程都必填”。结果使用 `WebDriverWait` 等待并用 `assert` 验证，失败时保存截图后重新抛出异常。

8. **综合练习（课后作业）。**作业与教师示例使用相同的页面行为和四类业务场景，但要求学生新建脚本、独立实现，不直接复制 `06综合示例.py`。作业将第 1 条姓名统一指定为“周同学”，便于按统一数据记录结果。页面为 `pages/comprehensive.html`，必须完成以下四条用例：

   | 编号 | 输入 | 操作 | 预期结果 |
   | --- | --- | --- | --- |
   | 1 | 姓名“周同学”，选择 Selenium 自动化 | 点击提交，在确认弹窗点确定 | `报名成功：周同学｜selenium` |
   | 2 | 姓名“周同学”，选择 Python 入门 | 点击提交，在确认弹窗点取消 | `已取消提交` |
   | 3 | 姓名留空，选择 Selenium 自动化 | 点击提交，不处理弹窗 | `提交失败：姓名和课程都必填`，不出现确认弹窗 |
   | 4 | 姓名“周同学”，课程保持“请选择” | 点击提交，不处理弹窗 | `提交失败：姓名和课程都必填`，不出现确认弹窗 |

   四条用例均须用 `assert` 比较完整提示文本，动态反馈使用 `WebDriverWait`。记录编号、输入、操作、预期、实际和断言结论；保存正常提交、取消提交和空值场景的关键截图。截图只能辅助取证，不能替代断言。

9. **整理结果。**提交独立脚本、关键截图和至少四条用例的测试记录表，并简要说明：页面出现正确提示但没有断言时为什么不能算自动测试通过；截图为什么不能替代断言。

## 五、提交要求

1. 学生独立编写的综合练习 Python 脚本。
2. 正常确认、取消提交、空值场景的关键截图。
3. 至少四条用例的测试记录表，字段包括编号、输入、操作、预期、实际和断言结论。
4. 对退出码、断言和截图关系的简短说明。

不要提交真实账号、密码、个人信息或外部网站数据。

## 六、注意事项

- 使用 `Path(__file__).resolve().parent` 和 `as_uri()` 定位本地页面，不依赖当前工作目录。
- 每个示例可独立运行，使用 `try/finally` 确保 `driver.quit()` 执行。
- 断言失败应保留失败状态，不要用宽泛 `except` 吞掉 `AssertionError`。
- 浏览器有动作、程序退出码为 0，不代表测试通过；必须确认断言执行并通过。
- 定位失败、等待超时、驱动不兼容属于执行异常；实际结果与预期不一致属于断言失败。
- 动态状态优先使用 `WebDriverWait`；`time.sleep()` 只用于暂停观察。
- 使用正常 Selenium API，不用 JavaScript 点击绕过要练习的交互。
- alert 使用 `accept()`，confirm 使用 `accept()` 或 `dismiss()`，prompt 使用 `send_keys()` 后确认。
- 本地页面不连接后端或外部 CDN；驱动获取失败时先检查网络和配置。
- 截图是辅助证据，不能代替页面文本断言。
