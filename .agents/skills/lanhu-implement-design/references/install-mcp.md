# 蓝湖 MCP 安装指南

本文档提供了在 Claude Code 环境中未安装蓝湖 MCP 服务器时的逐步安装和配置说明。

## 何时使用本指南

在以下情况下使用本指南：
- `lanhu_*` MCP 工具不可用
- 用户请求蓝湖相关功能但 MCP 服务器未连接
- 首次设置蓝湖集成

## 前置条件

安装前请确保：
- Node.js 18+ 或 Python 3.10+ 可用
- 已安装 Docker（可选，用于 Docker 方式安装）
- 用户拥有蓝湖平台访问权限和有效的 cookie

## 安装方式

### 方式一：Docker 安装（推荐）

Docker 提供了最可靠且隔离的安装方式。

```bash
# 克隆仓库
git clone https://github.com/dsphper/lanhu-mcp.git
cd lanhu-mcp

# 使用 Docker 构建并运行
docker build -t lanhu-mcp .
docker run -d -p 8000:8000 -e LANHU_COOKIE="your_cookie_here" lanhu-mcp
```

### 方式二：源码安装

不使用 Docker 的直接安装方式：

```bash
# 克隆仓库
git clone https://github.com/dsphper/lanhu-mcp.git
cd lanhu-mcp

# 安装依赖（基于 Python）
pip install -r requirements.txt

# 或者基于 Node.js
npm install

# 运行服务器
python main.py
# 或者
npm start
```

## 配置

### 环境变量

设置所需的环境变量：

```bash
export LANHU_COOKIE="your_lanhu_cookie_value"
```

**如何获取 LANHU_COOKIE：**

1. 登录蓝湖平台 (https://lanhuapp.com)
2. 打开浏览器开发者工具 (F12)
3. 进入 Application/Storage → Cookies
4. 找到认证 cookie 值
5. 复制完整的 cookie 字符串

### Claude Code MCP 配置

将蓝湖 MCP 服务器添加到 Claude Code 的 MCP 配置中：

**对于 Claude Desktop (config.json)：**

```json
{
  "mcpServers": {
    "lanhu": {
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

**对于 Claude Code CLI (settings.json)：**

```json
{
  "mcpServers": {
    "lanhu": {
      "command": "python",
      "args": ["main.py"],
      "cwd": "/path/to/lanhu-mcp"
    }
  }
}
```

或者使用 SSE 方式的连接：

```json
{
  "mcpServers": {
    "lanhu": {
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

## 验证

安装后，验证 MCP 服务器是否正常工作：

1. 检查服务器是否运行：

   ```bash
   curl http://localhost:8000/mcp
   ```

2. 在 Claude Code 中，检查可用工具：
   - `lanhu_resolve_invite_link`
   - `lanhu_get_pages`
   - `lanhu_get_designs`
   - 以及其他 `lanhu_*` 工具

## 故障排查

### Cookie 无效或过期

**症状：** `lanhu_resolve_invite_link` 返回认证错误

**解决方案：**
1. 重新登录蓝湖平台
2. 从浏览器获取新的 cookie
3. 更新 `LANHU_COOKIE` 环境变量
4. 重启 MCP 服务器

### 服务器无法启动

**症状：** 端口 8000 已被占用或连接被拒绝

**解决方案：**

```bash
# 检查端口占用情况
lsof -i :8000

# 如需要，使用不同端口
docker run -d -p 9000:8000 -e LANHU_COOKIE="your_cookie" lanhu-mcp
```

### 工具未在 Claude 中显示

**症状：** MCP 服务器正在运行但工具不可用

**解决方案：**
1. 验证 Claude Code MCP 配置是否正确
2. 检查服务器 URL 与配置是否匹配
3. 重启 Claude Code 以重新加载 MCP 服务器

## 快速启动清单

- [ ] 克隆 lanhu-mcp 仓库
- [ ] 安装依赖或构建 Docker 镜像
- [ ] 设置 `LANHU_COOKIE` 环境变量
- [ ] 启动 MCP 服务器
- [ ] 配置 Claude Code MCP 设置
- [ ] 验证工具是否可用
- [ ] 使用 `lanhu_resolve_invite_link` 进行测试

## 其他资源

- [蓝湖 MCP GitHub 仓库](https://github.com/dsphper/lanhu-mcp)
- [蓝湖平台](https://lanhuapp.com)
- [MCP 协议文档](https://modelcontextprotocol.io)
