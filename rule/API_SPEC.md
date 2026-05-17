## API 设计规范
### URL 规则
- 命名尽量使用直白的英文单词，避免缩写，多个单的使用连字符连接，如 /api/user-profile/update ，说明清晰，易于理解，单层级最多三个单词，尽量使用一个单词
- 路径规则 /api/功能类别/具体操作 ，如 /api/auth/login、/api/orders/create
- 不在 URL 中使用动词（cancel 等操作除外）

### HTTP 方法 
- 所有接口使用 POST 方法 ，创建、删除、查询、修改 ，

### 请求参数
- 所有参数放在请求体中，使用 JSON 格式
- 请求体示例{
    "page": 1,
    "pageSize": 200,
    "device_id": "ffffffff-c582-ded7-0000-0000157e82af",
    "deviceMode": "ASUS_I003DD"
}
- 请求头必须包含 Content-Type: application/json ，token：XXXX（需要认证）,timestamp: 1778208341408#毫秒级时间戳
- 请求头示例{
    "Content-Type": "application/json",
    "token": "abcdef123456",
    "timestamp": "1778208341408"
}



### 响应结构（固定，禁止变形）
所有接口返回：{ code, message, data, traceId }
- 成功：code=0，HTTP 200/201/204
- 失败：code=非0，HTTP 4xx/5xx
- 分页：data 中含 { total, page, pageSize, items }
- 成功（单条）
{
  "code": 0,
  "message": "success",
  "data": { "id": 1, "name": "张三" },
  "traceId": "abc-123"
}

- 成功（分页列表）
{
  "code": 0,
  "message": "success",
  "data": {
    "total": 100,
    "page": 1,
    "pageSize": 20,
    "items": [...]
  },
  "traceId": "abc-123"
}

- 失败
{
  "code": 4001,
  "message": "用户未登录",
  "data": null,
  "traceId": "abc-123"
}

- 字段校验失败（400）
{
  "code": 1001,
  "message": "参数错误",
  "data": null,
  "errors": [
    { "field": "email", "message": "邮箱格式不正确" },
    { "field": "age",   "message": "年龄必须大于 0" }
  ],
  "traceId": "abc-123"
}



### 错误处理
- 参数校验失败：HTTP 400 + code=1001 + errors 数组
- 未授权：HTTP 401 + code=3001
- 禁止操作：HTTP 403 + code=3002
- 不存在：HTTP 404 + code=2001
- 服务器错误：HTTP 500 + code=5000（不暴露堆栈）

### 后端结构
- Controller 只做参数提取和响应包装
- 业务逻辑在 Service 层
- 数据访问在 Repository/DAO 层
- 每个请求生成唯一 traceId 并写入日志

### 注释
- 所有接口必须有注释，说明功能、参数、返回值、错误码等