# 更新日志

本项目的所有重要更改都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [0.1.1]

### 新增

- 新增`DataCenter.JAPAN`和`DataCenter.BRAZIL`，可按应用所属接入点选择对应 AppPush 地址。
- 新增`device.register_token`，适配`POST /v4/devices/token/registration_id`；请求支持`platform`、`tokens`、`apns_production`，结果支持每个 Token 的`registration_id`、`is_new`、`code`、`message`。
- 新增`app.get_vip_status`并挂载到`Client.app`，映射`vip_status`和`vip_end_time`。

### 变更

- Push 请求模型补齐`body.voip`、Android`badge_set_num/is_fold`、Message`test_message/receipt_id`、Options`auto_truncation`。
- `notification.alert`、Android`alert`和`message.msg_content`使用`str/dict`联合类型；VoIP 与厂商扩展继续使用动态 dict。
- Batch Push 补齐逐目标成功/失败模型、`error.code/error.message`和顶层`rate_limit_info`，可以识别 HTTP 200 下的部分失败和限流。
- Group Push 按顶层动态 AppKey 解析成功与失败结果，分别写入`successes`、`errors`，并保留`group_msgid`。
- Device 标签支持`DeviceSetTags`对象或空字符串：对象用于增删标签，`tags=""`用于清空全部标签。
- Schedule 新增`TriggerIntelligent.backup_time`，创建和更新定时任务均复用补齐后的 Push 模型。
- Tag-device 查询改为返回`TagStatusGetResult.result`；Tag 计数和配额接口改为`List[str] tags + 单个 platform`，公共 query 编码启用 repeated-key。
- Plan Detail 查询参数修正为`plan_ids/start_date/end_date`，返回值继续保持可自行解析的 dict。
- Voice`create`由 JSON 文本参数改为官网`language + file` multipart 上传；列表返回数组，单项结果补齐`file_url`。
- OPPO Image 由 multipart 文件上传改为 JSON URL 请求，使用`big_picture_url/small_picture_url`并映射`big_picture_id/small_picture_id`；移除不符合官网协议的`upload_oppo_from_reader`。
- Device Token 和 OPPO Image 的数量、平台、条件及二选一业务约束交由服务端校验，SDK 沿用`ApiError`返回错误。

### 修复

- 修正 Tag、Status Plan Detail、Voice、Image 和 Group Push 中与官网不一致的 query、body 与响应层级。
- 补充请求序列化、动态 AppKey、部分限流、响应解析及错误响应测试，并通过完整 unittest 与 compileall 验证。

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
