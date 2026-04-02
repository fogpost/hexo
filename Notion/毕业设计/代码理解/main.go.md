## 🧩 1. 桌面入口：`wails_shell/main.go`

`main.go` 负责启动 Wails 桌面应用（Go + Web 前端）：

- `//go:embed all:frontend/dist`
    - 将前端静态资源打包到可执行文件里（`frontend/dist`）。
- `wails.Run(&options.App{...})`
    - `Title/Width/Height`：窗口标题与大小
    - `AssetServer`：用 `assets` 将前端文件提供给前端
    - `OnStartup: app.startup`, `OnShutdown: app.shutdown`：生命周期回调
    - `Bind: []interface{}{app}`：绑定 app 对象，前端可以通过 `window.go.main.App.xxx()` 访问 Go 方法

意义：

- 这是整个“桌面版本”的启动点
- 前端 `App.vue` 不直接访问后端 REST API 时走 Wails 桥接（`callApp`）

---

## 🖥️ 2. 主要 UI：`traffic-ui/src/App.vue`

### 2.1 数据与状态（`ref` / `computed`）

主状态变量：

- `serviceStatus`（后端抓包状态）
- `packets`, `detail`, `currentFile`, `fileItems`
- `report`（检测结果与告警）
- 终端相关：`terminals`, `activeTerminalId`, `terminalHistory`
Computed：

- `hexBytes`/`hexRows`：Hex 视图生成
- `liveFiles`：`live/`目录文件列表
- `selectedIfaceLabel`：当前网卡标签

---

### 2.2 接口通信（HTTP + 桌面 API）

#### HTTP REST（Web 或混合方式）

- `GET /pcap-files` → `refreshFileCatalog`
- `GET /packets` → `loadPackets`
- `GET /packet/{id}/detail` → `selectPacket`
- `GET /analysis/report` → `refreshAnalysis`
- `POST /upload-pcap`、`/load-data-file`、`/load-next-data-file`、`DELETE /data-file`

#### 桌面桥接（Wails 方式）

`callApp("Xxx", ...)`：

- `ServiceStatus`, `StartEmbeddedStack`, `StopEmbeddedStack`
- `StartCapture/StopCapture`, `ListCaptureInterfaces`
- 远程终端：`ListTerminals`, `CreateLocalTerminal`, `CreateSSHTerminalWithKey`, `WriteTerminalInputByID`, `GetTerminalLogsByID`, `CloseTerminal`

---

### 2.3 交互逻辑横向（主要行为）

- `init()`：启动前会
    
    1. 启动内置后端（桌面模式）
    2. 刷新网卡 / 状态 / 终端 / 当前用户
    3. 载入文件列表、包列表、分析报告
    4. 开启 `polling`（定时刷新）
- `pollingTick()`
    
    - 自动刷新文件列表
    - 自动解析 live 文件
    - 刷新服务状态和分析
- `loadPackets()` + `selectPacket(id)` 负责数据包列表和细节
    
- `loadDataFile(path)` 用来加载选中文件并同步刷新列表/报告
    

---

### 2.4 Hex + 解析高亮机制

- `highlightField(offset,length)` 存偏移/长度
- `isHighlighted(i)` 控制十六进制字节颜色
- 事件绑定：
    - 协议/字段 hover：强对应高亮
    - 鼠标移出：`clearHighlight()`

---

### 2.5 终端系统（xterm.js）

- 终端显示：`Terminal` + `FitAddon`
- 历史缓存：
    - `terminalHistory`（Map）
    - `terminalDecoders`（UTF-8）
    - `terminalLegacyDecoders`（GB18030 备选）
- 事件流：`onTerminalStream(payload)` 处理来自 `runtime.EventsOn("terminal:stream")` 的 Base64 字节流，解析写入终端
- 终端动作：创建、本地/SSH、关闭、重连、复制

---

## 🧾 3. 结构总结（简明）

- `wails_shell/main.go`：桌面 app 启动入口，桥接 Go API
- `App.vue`：视觉 + 状态 + HTTP/桌面连接 + 捕包、解析、终端全部交互
- 后端替换：如果切为纯 Web（没有桌面桥接），仍支持大多数 REST 操作（`hasDesktopBridge = false` 并提示）
- 功能覆盖：
    - 捕包控制（接口、状态）
    - 文件上传/载入/删除
    - 分析结果、告警、定位
    - 十六进制+层次解析可视化
    - Xia终端（本地/SSH/历史/编码）