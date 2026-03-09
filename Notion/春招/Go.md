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