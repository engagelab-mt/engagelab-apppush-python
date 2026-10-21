# 发布 Python SDK

正式 GitHub Release 会触发 `.github/workflows/publish.yml`，自动校验 Tag、运行测试、构建并检查发行包、验证 wheel 安装，再上传 PyPI。

## 一次性配置

1. 在 GitHub 仓库 Settings → Environments 中创建名为 `pypi` 的 Environment。可按团队约定添加 required reviewers。
2. 登录 PyPI，进入 `engagelab-apppush` 项目的 Manage → Publishing，添加 GitHub Trusted Publisher：

| 字段 | 值 |
| --- | --- |
| Owner | `engagelab-mt` |
| Repository name | `engagelab-apppush-python` |
| Workflow name | `publish.yml` |
| Environment name | `pypi` |

这是项目级发布授权，无需在 GitHub Secrets 保存 PyPI API Token。仅发布 job 具有 OIDC 权限，构建和测试 job 不具备此权限。

## 每次发布

1. 修改 `pyproject.toml` 版本和 `CHANGELOG.md`，评审、测试通过后合并到 `main`。
2. 基于包含该改动的 `main` 提交创建正式 GitHub Release，如包版本 `0.1.2` 对应 Tag `v0.1.2`。
3. 不勾选 Pre-release，点击 Publish release。只打 Tag 或保存 Draft 不触发上传。
4. 查看 Actions 中的 `Publish Python SDK to PyPI`。如配置了 Environment 审批，审核后继续。
5. 发布成功后，在独立虚拟环境运行 `pip install --no-cache-dir --index-url https://pypi.org/simple engagelab-apppush==版本号` 验证公共安装。

流水线拒绝版本与 Tag 不一致、非正式版本号或尚未合入 `main` 的发布源码。

## 失败后重试

修复配置后可通过 Actions → Publish Python SDK to PyPI → Run workflow，选择工作流分支 `main` 并填写现有 Tag。上传前应先检查 PyPI 是否已存在该版本，避免重复上传；已有版本文件不可覆盖，流水线不会静默跳过冲突。

`0.1.1` 已手动发布，不要用它测试上传。可检查构建步骤，但端到端自动发布应等下一个正式版本。

参考：[PyPI Trusted Publishing](https://docs.pypi.org/trusted-publishers/using-a-publisher/)。
