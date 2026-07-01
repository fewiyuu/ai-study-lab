---
title: 24_MCP外部系统扩展
aliases:
  - MCP外部系统扩展
  - MCP与插件
  - Agent可扩展性
  - Learn Claude Code 24
tags:
  - LearnClaudeCode
  - Agent
  - MCP
  - plugin
  - learning-kit
source: https://www.bilibili.com/video/BV1ZMRdBdECv
created: 2026-06-06
---

> [!question] 常见问题速查
> 1. MCP 的本质是什么？
> 2. 为什么本地工具写死会限制 Agent 扩展性？
> 3. MCP client、Plugin loader、MCP tool router 分别做什么？
> 4. `plugin.json` 如何帮助发现 MCP server？
> 5. `initialize`、`tools/list`、`tools/call` 分别是什么？
> 6. MCP 工具为什么要加命名前缀？
> 7. 为什么 MCP 工具也必须经过权限检查？

> [!abstract] 核心主线
> MCP 的本质是把外部工具安全、统一地接入 Agent。早期 Agent 的工具写死在本地代码里，新增浏览器、数据库、业务系统能力都要改源码。MCP 让外部 MCP server 按协议暴露工具，Agent 通过 MCP client 连接 server，调用 `initialize` 建立能力协商，调用 `tools/list` 获取工具 schema，再把工具加上命名前缀合并到本地工具池。模型调用 MCP 工具时，系统先经过 permission gate，再由 MCP router 解析工具名，找到对应 server 和 actual tool，最后通过 `tools/call` 发给外部 server。外部工具不能绕过权限系统，也不能覆盖 native tools。

## 概念精讲

### MCP 解决工具写死问题

早期 native tools：

- `bash`
- `read_file`
- `write_file`
- `edit_file`

如果继续把所有能力都写成本地函数，代码会不断膨胀。

MCP 让其他团队或外部系统提供工具，Agent 只要按协议接入。

> [!abstract] 一句话
> MCP = 外部工具接入 Agent 的统一协议。

## 三个核心组件

| 组件 | 职责 | 直觉 |
|---|---|---|
| MCP client | 连接 MCP server，发送 JSON-RPC 请求 | 客户端 |
| Plugin loader | 扫描插件清单，发现 server | 注册中心 |
| MCP tool router | 根据工具名分发调用 | 路由器 |

## 插件清单

`plugin.json` 告诉系统有哪些 MCP server：

```json
{
  "name": "plugin1",
  "mcpServers": {
    "server1": {
      "command": "python",
      "args": ["mcp_simple_server.py"],
      "transport": "stdio"
    }
  }
}
```

Plugin loader 扫描 `.cloud-plugin/plugin.json`，把清单读入内存。

## MCP client 连接流程

1. 根据 manifest 创建 MCP client。
2. 用 stdio 启动 server 进程。
3. 发送 `initialize`。
4. 接收 server capabilities。
5. 发送 `tools/list`。
6. 获取 server 提供的工具。
7. 注册到 router。

示例：

```json
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}
{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}
```

stdio transport 是通过标准输入输出管道通信；也可以类比成“发 request，收 response”。

## 工具池合并

本地工具先加入：

```text
bash
read_file
write_file
edit_file
```

MCP tools 加前缀后加入：

```text
mcp__plugin1__server1__list_files
mcp__plugin1__server1__add
```

前缀作用：

- 标识工具来自 MCP。
- 避免和 native tools 重名。
- 让 router 能解析 server name 和 actual tool。

> [!warning] native tools 优先
> 外部工具不应覆盖核心本地工具，否则可能污染基础能力。

## MCP 工具调用流程

模型调用：

```text
mcp__plugin1__server1__list_files
```

系统执行：

1. permission gate 先检查风险。
2. 判断这是 MCP tool。
3. router 解析：
   - server = `plugin1__server1`
   - actual_tool = `list_files`
4. 找到对应 MCP client。
5. client 发送：

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "list_files",
    "arguments": {"path": "."}
  }
}
```

6. server 返回结果。
7. 结果作为 tool_result 回到 Agent loop。

## 权限不可绕过

MCP 工具也必须经过权限检查。

原因：

- 外部 server 可能提供危险工具。
- MCP 工具可能读写文件、查询数据库、调用外部系统。
- 如果绕过权限，就相当于给 Agent 开后门。

只读 MCP 工具可以更宽松；写操作、高风险操作必须 ask 或 deny。

## 判断与行动清单

> [!todo] 接入 MCP 前先检查
> - [ ] 是否有插件清单。
> - [ ] server command / args / transport 是否明确。
> - [ ] client 是否能 initialize。
> - [ ] 是否能 `tools/list`。
> - [ ] 工具 schema 是否包含 name、description、input_schema。
> - [ ] MCP 工具名是否加命名前缀。
> - [ ] native tools 是否优先。
> - [ ] MCP 工具是否经过 permission gate。
> - [ ] router 是否能解析 server 和 actual tool。
> - [ ] `tools/call` 失败是否有错误恢复。
> - [ ] 调用是否有审计日志。

## 应用与迁移问答

> [!question] MCP 和普通插件有什么区别？
> MCP 强调统一协议和工具调用 schema，让外部 server 能被 Agent 统一发现、列出和调用。

> [!question] stdio 和 HTTP/SSE 传输有什么直觉差别？
> stdio 像启动一个本地子进程后通过管道通信；HTTP/SSE 更像通过网络服务通信。

> [!question] 如果 MCP server 连接失败怎么办？
> 不应阻塞整个 Agent。应跳过该 server、记录错误，并只把可用工具加入工具池。

## 练习 / 盲区复盘

> [!failure] 容易卡住的地方
> - 只记 MCP 名词，不理解 initialize / list / call。
> - 外部工具不加命名前缀。
> - 允许 MCP 工具覆盖 native tools。
> - MCP 工具绕过权限检查。
> - server 连接失败导致整个 Agent 启动失败。
> - 不记录 MCP 调用日志。
> - 把工具 schema 写得太模糊，模型不知道怎么调用。

## 费曼解释润色版

> [!quote]
> MCP 的核心是把外部工具按统一协议接入 Agent。早期 Agent 的工具都写在本地，比如 bash、read_file、write_file；如果要新增浏览器、数据库或业务系统能力，继续改源码会越来越臃肿。MCP 让外部 MCP server 提供工具，Agent 通过 Plugin loader 扫描 `plugin.json`，找到 server 的 command、args 和 transport。然后 MCP client 启动或连接 server，先发送 `initialize`，再通过 `tools/list` 拿到工具 schema。系统把这些外部工具加上前缀，例如 `mcp__plugin1__server1__list_files`，再合并到工具池里。模型调用这个工具时，系统先经过 permission gate，确认风险可接受，再由 MCP router 解析 server 和 actual tool，最后通过 `tools/call` 发给外部 server。这样外部能力可以动态接入，但仍然走统一工具池、统一命名和统一权限控制。

## 易错卡片

> [!warning] 误区：MCP 就是多装几个插件
> 正确说法：MCP 是外部工具接入 Agent 的统一协议。

> [!warning] 误区：MCP 工具可以绕过权限系统
> 正确说法：外部工具更要经过 permission gate。

> [!warning] 误区：外部工具可以覆盖 native tools
> 正确说法：native tools 应优先，MCP 工具要命名隔离。

> [!warning] 误区：连接失败就让整个 Agent 不可用
> 正确说法：应记录失败并降级，只注册可用 server 的工具。
