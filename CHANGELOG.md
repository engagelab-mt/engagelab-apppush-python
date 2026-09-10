# 更新日志

本项目的所有重要更改都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [0.1.1]

### 新增

- `DataCenter`：新增`JAPAN`和`BRAZIL`，用于连接部署在日本、巴西数据中心的应用。
- `client.device.register_token`：新增厂商 Token 注册能力；`DeviceTokenRegisterResult`可获取每个 Token 对应的 Registration ID、是否首次创建、错误码和错误信息。
- `client.app.get_vip_status`：新增应用 VIP 状态和到期时间查询。

### 变更

- `client.push.send`、`client.push.validate`、Batch Push、Group Push 和 Schedule 推送参数：新增`PushBody.voip`、Android`badge_set_num/is_fold`、Message`test_message/receipt_id`、Options`auto_truncation`。
- `NotificationMessage`、`AndroidNotification`和`CustomMessage`：通知内容及自定义消息内容支持`str`或结构化`dict`。
- `client.push.batch_by_regid`和`client.push.batch_by_alias`：`BatchPushResult`新增逐目标成功/失败结果和限流信息，可识别请求成功时返回的部分失败。
- `GroupPushClient.send`：`GroupPushResult.successes`和`errors`可按 AppKey 获取各应用结果，同时保留`group_msgid`。
- `client.device.set`：`DeviceSetParam.tags`支持`DeviceSetTags`对象；传入空字符串可清空设备全部标签。
- `client.schedule.create`和`client.schedule.update`：新增`TriggerIntelligent.backup_time`智能定时配置。
- `client.tag.get_device_status`：改为返回`TagStatusGetResult.result`，用于判断设备是否拥有指定标签。
- `client.tag.get_count`和`client.tag.get_quota`：参数改为`List[str] tags`和单个`platform`。
- `client.status.plan_detail`：参数改为`List[str] plan_ids, str start_date, str end_date`；返回值继续保持可自行解析的 dict。
- `client.voice.create`：参数改为`language, file_path`并上传本地语音文件；`client.voice.list`返回列表，`client.voice.get`结果新增`file_url`。
- `client.image.upload_oppo`：参数改为`OppoImageParam`，通过大图或小图 URL 上传，结果返回对应的图片 ID；不符合要求的参数通过既有`ApiError`返回。
- `client.image.upload_oppo_from_reader`：已移除，请改用`client.image.upload_oppo`。
- `client.device.register_token`：数量、平台和 APNs 条件不在客户端提前拦截，服务端错误继续通过`ApiError`返回。

### 修复

- `client.tag.get_count`、`client.tag.get_quota`和`client.status.plan_detail`：修正参数编码，避免服务端收到错误的查询条件。
- `client.voice.create`、`client.voice.list`和`client.image.upload_oppo`：修正请求或响应格式不一致导致的调用失败、字段丢失问题。
- Tests：补充公开方法的请求序列化、Group Push 多应用结果、Batch Push 部分限流、响应解析及错误响应测试。

## [0.1.0] - 2026-03-20

### 新增

- `Client` 客户端初始化，支持 `base_url`、`timeout` 等参数
- 四大数据中心常量：`DataCenter.SINGAPORE`（默认）、`HONG_KONG`、`VIRGINIA`、`FRANKFURT`
- **Push** — 推送服务：`send`、`send_raw`、`validate`、`withdraw`、`batch_by_regid`、`batch_by_alias`
- **Group Push** — 应用分组推送：独立 `GroupPushClient` + `send`
- **Device** — 设备管理：`get`、`set`、`delete`、`get_status`
- **Tag** — 标签管理：`list`、`set`、`delete`、`get_count`、`get_device_status`、`get_quota`
- **Alias** — 别名管理：`get`、`delete`
- **Schedule** — 定时推送：`create`、`update`、`delete`、`get`、`list`、`get_msg_ids`
- **Status** — 统计查询：`users`、`message_detail`、`message_lifecycle`、`batch_message_detail`、`plan_detail`
- **Plan** — 推送计划：`create_or_update`、`list`、`query_msg`、`delete`、`batch_delete`
- **Voice** — 语音/TTS 模板：`create`、`list`、`get`、`delete`
- **Image** — 图片上传：`upload_oppo`、`upload_oppo_from_reader`
- `ApiError` 结构化异常类型，包含 HTTP 状态码和业务错误码
- 完整的单元测试（使用 `http.server` 模拟，零外部依赖）
- 零第三方依赖，仅使用 Python 标准库
