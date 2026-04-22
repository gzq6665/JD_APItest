# HRJD 接口自动化测试

本项目根据 `HRJD.postman_collection.json` 中的接口业务流，使用 `pytest + requests` 重新封装接口自动化测试。
当前按你的要求调整为：

- `tests/`：14 个独立接口测试脚本
- `data/`：测试数据文件
- `api/`：接口请求脚本与响应断言脚本
- 使用 `pytest.mark.parametrize` 参数化读取 JSON 测试数据
- 使用 `fixture + yield` 处理前后置和资源释放
- 支持生成离线 Allure 测试报告

## 目录说明

- `api/`：接口请求与响应断言封装。
- `data/`：按接口拆分的 JSON 测试数据。
- `scripts/`：测试辅助脚本，例如生成 Allure 报告。
- `utils/`：配置、HTTP 客户端、上下文模型、随机数据与 JSON 数据加载。
- `tests/`：14 个接口测试脚本。

## 运行前准备

默认会使用当前项目的测试环境地址：

- `BASE_URL=http://121.43.169.97:8081`
- `ADMIN_BASE_URL=http://121.43.169.97:8082`

如果你想切换到其他环境，也可以覆盖这两个环境变量：

- `BASE_URL`：前台系统地址，对应 Postman 中的 `{{base_url}}`
- `ADMIN_BASE_URL`：后台系统地址，对应 Postman 中的 `{{base_url2}}`

PowerShell 示例：

```powershell
$env:BASE_URL = "http://your-front-host"
$env:ADMIN_BASE_URL = "http://your-admin-host"
```

安装依赖：

```powershell
python -m pip install -r requirements.txt
```

执行测试：

```powershell
python -m pytest -s -v
```

如果使用默认环境，直接执行即可；如果切换环境，再设置对应环境变量。

## 生成离线 Allure 报告

直接执行：

```powershell
python .\scripts\generate_allure_report.py
```

或者执行快捷脚本：

```powershell
.\run_allure_report.ps1
```

生成完成后，离线报告位于：

```text
report\allure-report\index.html
```

原始结果文件位于：

```text
report\allure-results
```

## 参数化说明

每个接口脚本都通过 `@pytest.mark.parametrize(..., indirect=True)` 读取对应 JSON 文件中的 `cases` 列表。

- `tests/` 中的脚本负责声明参数化入口。
- `data/test_*.json` 中存放该接口的请求参数和断言期望。
- `conftest.py` 中的 fixture 负责前置依赖、调用接口、执行断言、处理后置资源释放。

## 当前 14 个接口脚本

1. `test_01_get_register_image_code.py`
2. `test_02_send_sms.py`
3. `test_03_register.py`
4. `test_04_login.py`
5. `test_05_is_login.py`
6. `test_06_approve_realname.py`
7. `test_07_get_approve_info.py`
8. `test_08_open_account.py`
9. `test_09_apply_amount.py`
10. `test_10_admin_login.py`
11. `test_11_search_amount_apply_list.py`
12. `test_12_open_amount_verify_page.py`
13. `test_13_submit_amount_verify.py`
14. `test_14_get_amount_apply_log.py`
