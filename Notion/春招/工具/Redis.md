综述：Redis 常见的基本数据类型主要有五种：String、Hash、List、Set、Sorted Set。  
String 用于缓存和计数器；  
Hash 用于存储对象，比如用户信息；  
List 常用于消息队列；  
Set 用于去重或标签；  
Sorted Set 用于排行榜等需要排序的场景。
## 数据类型
1. String
最基本类型：存储字符串、数字、二进制数据
SET key value、GET key、INCR key
缓存、计数器、token
2. Hash
key-value 的 map
HSET user:1 name fogpost
存储对象、用户信息
3. List
双向链接表：LPUSH、RPUSH、LPOP、RPOP
消息队列、最新消息队列
4. Set
无序集合，不重复
SADD、SMEMBERS
去重、标签系统
5. Sorted Set(Zset)
带score 的有序集合
ZADD、ZRANGE
排行榜、权重排序

