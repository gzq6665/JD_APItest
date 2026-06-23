# JD 自动化测试项目集

本仓库包含针对同一借贷业务系统的两套自动化测试工程，分别覆盖**接口层**与**UI 层**。

| 子项目 | 目录 | 技术栈 | 说明 |
| --- | --- | --- | --- |
| 接口自动化测试 | [`api-test/`](api-test/) | pytest + requests + Allure | 14 个接口测试脚本，参数化 + fixture 前后置 |
| UI 自动化测试 | [`ui-test/`](ui-test/) | pytest + Selenium + POM + Allure | 6 条端到端业务流程，页面对象模型设计 |

## api-test —— 接口自动化测试

- `pytest + requests` 封装接口请求与响应断言
- `@pytest.mark.parametrize` 参数化读取 JSON 测试数据
- `fixture + yield` 处理前后置依赖与资源释放
- 支持生成离线 Allure 报告
- 覆盖注册、登录、实名认证、开户、额度申请、后台审核等 14 个接口

详见 [api-test/README.md](api-test/README.md)。

## ui-test —— UI 自动化测试

- 基于 **Selenium + Page Object Model（页面对象模型）** 分层设计
  - `base/`：浏览器驱动工厂与基础页面封装
  - `page/`：各业务页面的元素与操作封装
  - `script/`：测试用例脚本
  - `data/`：JSON 测试数据
- 覆盖用户注册、登录、开户、借款额度申请、后台登录、后台额度审核等 6 条核心业务流程
- 使用 `conftest.py` fixture 管理驱动生命周期与失败截图
- 支持生成 Allure 报告

## 运行方式

两个子项目均为独立的 pytest 工程，进入对应目录后安装依赖并运行：

```powershell
# 接口测试
cd api-test
python -m pip install -r requirements.txt
python -m pytest -s -v

# UI 测试（需本地安装 Chrome 及对应 chromedriver）
cd ui-test
python -m pytest -s -v
```