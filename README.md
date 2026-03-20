# EngageLab AppPush Python SDK

EngageLab AppPush REST API 的 Python SDK，零第三方依赖，仅使用 Python 标准库。

## 安装

```bash
pip install engagelab-apppush
```

或从源码安装：

```bash
pip install .
```

## 快速开始

```python
import engagelab

# 创建客户端（默认新加坡数据中心）
client = engagelab.Client("your-app-key", "your-master-secret")

# 或指定数据中心
client = engagelab.Client(
    "your-app-key",
    "your-master-secret",
    base_url=engagelab.DataCenter.HONG_KONG,
)

# 发送推送
result = client.push.send(engagelab.PushParam(
    from_="push",
    to="all",
    body=engagelab.PushBody(
        platform="all",
        notification=engagelab.NotificationMessage(
            alert="Hello from Python SDK!",
            android=engagelab.AndroidNotification(
                alert="Hello Android!",
                title="Test Push",
            ),
            ios=engagelab.IOSNotification(
                alert="Hello iOS!",
            ),
        ),
    ),
))
print(f"Push sent: msg_id={result.msg_id}")
```

## 数据中心

| 常量                        | 区域        | Base URL                              |
| --------------------------- | ----------- | ------------------------------------- |
| `DataCenter.SINGAPORE`      | 新加坡 (默认) | `https://pushapi-sgp.engagelab.com`   |
| `DataCenter.HONG_KONG`      | 香港         | `https://pushapi-hk.engagelab.com`    |
| `DataCenter.VIRGINIA`       | 美国弗吉尼亚   | `https://pushapi-usva.engagelab.com`  |
| `DataCenter.FRANKFURT`      | 德国法兰克福   | `https://pushapi-defra.engagelab.com` |

## API 模块

### Push — 推送

```python
client.push.send(param)                # 创建推送
client.push.send_raw(raw_body)         # 自定义 JSON 推送
client.push.validate(param)            # 推送校验
client.push.withdraw(msg_id)           # 消息撤回
client.push.batch_by_regid(param)      # 按 Registration ID 批量推送
client.push.batch_by_alias(param)      # 按 Alias 批量推送
```

### Group Push — 应用分组推送

```python
# Group Push 使用独立认证: group-{GroupKey}:{GroupMasterSecret}
group_client = engagelab.GroupPushClient(
    "group-key",
    "group-master-secret",
    base_url=engagelab.DataCenter.SINGAPORE,
)
group_client.send(param)
```

### Device — 设备

```python
client.device.get(registration_id)              # 查询设备信息
client.device.set(registration_id, param)        # 设置设备标签/别名
client.device.delete(registration_id)            # 删除设备
client.device.get_status(param)                  # 查询设备在线状态
```

### Tag — 标签

```python
client.tag.list()                                           # 获取标签列表
client.tag.set(tag, param)                                  # 添加/移除标签设备
client.tag.delete(tag, platforms=["android"])                # 删除标签
client.tag.get_count(tags, platforms=["android"])            # 查询标签设备数
client.tag.get_device_status(tag, registration_id)          # 查询设备标签绑定状态
client.tag.get_quota(tags=["vip"], platforms=["android"])    # 查询标签配额
```

### Alias — 别名

```python
client.alias.get(alias, platforms=["android"])     # 查询别名设备
client.alias.delete(alias, platforms=["android"])  # 删除别名
```

### Schedule — 定时任务

```python
client.schedule.create(param)           # 创建定时推送
client.schedule.update(id, param)       # 更新定时推送
client.schedule.delete(id)              # 删除定时推送
client.schedule.get(id)                 # 获取定时推送详情
client.schedule.list(page=1)            # 获取定时推送列表
client.schedule.get_msg_ids(id)         # 获取定时推送消息 ID
```

### Status — 统计

```python
client.status.users(time_unit, start, duration)            # 用户统计
client.status.message_detail(message_ids)                  # 消息送达统计
client.status.message_lifecycle(msg_id, registration_ids)  # 消息生命周期
client.status.batch_message_detail(message_ids)            # 批量消息统计
client.status.plan_detail(plan_id, message_ids)            # 推送计划统计
```

### Plan — 推送计划

```python
client.plan.create_or_update(param)                                       # 创建/更新推送计划
client.plan.list(page_index=1, page_size=10, send_source=None, search_description="")  # 查询列表
client.plan.query_msg(plan_ids, start_date, end_date)                     # 查询计划消息 ID
client.plan.delete(plan_id)                                               # 删除推送计划
client.plan.batch_delete(plan_ids)                                        # 批量删除推送计划
```

### Voice — 语音/TTS

```python
client.voice.create(param)        # 创建语音模板
client.voice.list()               # 获取语音模板列表
client.voice.get(language)        # 获取语音模板
client.voice.delete(language)     # 删除语音模板
```

### Image — 图片

```python
client.image.upload_oppo(file_path)                       # 上传 OPPO 大图 (文件路径)
client.image.upload_oppo_from_reader(filename, reader)    # 上传 OPPO 大图 (file-like object)
```

## 错误处理

SDK 使用 `engagelab.ApiError` 异常类型返回 API 错误：

```python
try:
    result = client.push.send(param)
except engagelab.ApiError as e:
    print(f"API Error: status={e.status_code} code={e.error.code} message={e.error.message}")
except Exception as e:
    print(f"Network Error: {e}")
```

## 客户端配置

```python
# 指定数据中心
client = engagelab.Client("key", "secret",
    base_url=engagelab.DataCenter.HONG_KONG,
)

# 自定义超时
client = engagelab.Client("key", "secret", timeout=60)

# 自定义 Base URL
client = engagelab.Client("key", "secret",
    base_url="https://custom-api.example.com",
)
```

## 认证方式

| API 模块                                                               | 认证                                            |
| ---------------------------------------------------------------------- | ----------------------------------------------- |
| Push / Device / Tag / Alias / Schedule / Status / Plan / Voice / Image | Basic Auth: `appKey:masterSecret`               |
| Group Push                                                             | Basic Auth: `group-{GroupKey}:GroupMasterSecret` |

## 更新日志

详见 [CHANGELOG.md](CHANGELOG.md)。

## 许可证

MIT License
