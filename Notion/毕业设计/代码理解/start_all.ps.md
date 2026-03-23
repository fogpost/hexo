## 代码展示
```powershell
param(
  [switch]$WithCapture
)

$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $PSScriptRoot

Start-Process powershell -ArgumentList "-NoExit", "-ExecutionPolicy", "Bypass", "-File", (Join-Path $repoRoot 'scripts\start_backend.ps1')
Start-Process powershell -ArgumentList "-NoExit", "-ExecutionPolicy", "Bypass", "-File", (Join-Path $repoRoot 'scripts\start_frontend.ps1')

if ($WithCapture) {
  Start-Process powershell -ArgumentList "-NoExit", "-ExecutionPolicy", "Bypass", "-File", (Join-Path $repoRoot 'scripts\start_go_capture.ps1')
}

Write-Host 'Backend and frontend launch commands have been started in new PowerShell windows.'
if ($WithCapture) {
  Write-Host 'Go live capture process has also been started.'
}

```

## 功能介绍
1. 参数定义
```powershell
param(
  [switch]$WithCapture
)
```
定义一个开关参数$WithCapture
- 不加 → 不启动抓包
- 加上 → 启动抓包模块

2. 错误处理
```powershell
$ErrorActionPreference = 'Stop'
```
- 一旦报错，脚本立即停止（防止半启动状态）

3. 获取项目根目录
```powershell
$repoRoot = Split-Path -Parent $PSScriptRoot
```
- `$PSScriptRoot` = 当前脚本所在目录
- `Split-Path -Parent` = 取上一级目录

4. 启动后端：
```powershell
Start-Process powershell -ArgumentList "-NoExit", "-ExecutionPolicy", "Bypass", "-File", (Join-Path $repoRoot 'scripts\start_backend.ps1')
```
- 打开一个新的PowerShell窗口执行scripts/start_backend.ps1，且不关闭窗口

5. 启动前端：
```powershell
Start-Process powershell -ArgumentList "-NoExit", "-ExecutionPolicy", "Bypass", "-File", (Join-Path $repoRoot 'scripts\start_frontend.ps1')
```

6. 抓包模块：
```powershell
if ($WithCapture) { 
  Start-Process powershell -ArgumentList "-NoExit", "-ExecutionPolicy", "Bypass", "-File", (Join-Path $repoRoot 'scripts\start_go_capture.ps1')   
} 
```

7. 输出提示：
```powershell
Write-Host 'Backend and frontend launch commands have been started in new PowerShell windows.'
```