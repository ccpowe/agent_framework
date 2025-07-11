# 斗地主API日志系统

## 功能概述

本API系统现在支持完整的日志记录功能，所有API请求、响应和游戏运行过程都会被记录到日志文件中。

## 日志文件结构

系统会在项目根目录下创建 `logs/` 文件夹，包含以下日志文件：

- `doudizhu_api.log` - 主日志文件（10MB轮转，保留5个备份）
- `doudizhu_error.log` - 错误日志文件（5MB轮转，保留3个备份）  
- `doudizhu_game.log` - 游戏专用日志文件（20MB轮转，保留5个备份）

## 日志内容

### API请求日志
- 请求开始时间和客户端IP
- 请求方法、URL和处理时间
- 响应状态码
- 异常信息（如果有）

### 游戏运行日志
- 游戏创建和启动
- 游戏状态变更
- 智能体决策过程
- 游戏结束和结果

### 系统日志
- 应用启动和关闭
- 内存使用情况
- 错误和异常信息

## 日志管理API

### 获取日志文件列表
```http
GET /api/logs
```

返回所有日志文件的详细信息，包括文件大小、修改时间等。

### 查看日志内容
```http
GET /api/logs/{filename}?lines=100
```

获取指定日志文件的最后N行内容，默认100行。

### 删除日志文件
```http
DELETE /api/logs/{filename}
```

删除指定的日志文件（主日志文件受保护，不能删除）。

### 清理旧日志
```http
POST /api/logs/cleanup?days=30
```

清理超过指定天数的旧日志备份文件，默认30天。

## 日志配置

日志配置在 `logging_config.py` 文件中，可以调整：

- 日志文件大小限制
- 备份文件数量
- 日志级别
- 日志格式

## 使用示例

### 查看最新日志
```bash
curl http://localhost:8000/api/logs/doudizhu_api.log?lines=50
```

### 获取日志统计
```bash
curl http://localhost:8000/api/logs
```

### 清理30天前的日志
```bash
curl -X POST http://localhost:8000/api/logs/cleanup?days=30
```

## 开发调试

在开发过程中，可以通过以下方式查看实时日志：

1. **控制台输出**：直接在运行API的终端查看
2. **日志文件**：使用 `tail -f logs/doudizhu_api.log` 实时查看
3. **API接口**：通过浏览器访问 `http://localhost:8000/api/logs`

## 注意事项

1. 日志文件会自动轮转，避免单个文件过大
2. 主日志文件受保护，不能通过API删除
3. 游戏运行日志单独记录，便于分析游戏逻辑
4. 所有敏感信息已过滤，不会记录到日志中
5. 日志文件使用UTF-8编码，支持中文内容

## 性能影响

- 日志记录对API性能影响极小（< 1ms）
- 使用异步日志写入，不阻塞主线程
- 日志轮转自动进行，不影响运行时性能
- 建议定期清理旧日志文件以节省磁盘空间 