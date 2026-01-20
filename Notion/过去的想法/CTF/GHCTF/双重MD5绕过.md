---
create: 2026-01-18T12:49
updated: 2026-01-20T15:39
crated: 2026-01-18T12:49
---
```python
# -*- coding: utf-8 -*-
# 运行: python3 md5.py "666" 0
import multiprocessing
import hashlib
import random
import string
import sys

CHARS = string.ascii_letters + string.digits

def cmp_md5(substr, stop_event, str_len, start=0, size=20):
    global CHARS
    while not stop_event.is_set():
        rnds = ''.join(random.choice(CHARS) for _ in range(size))
        md5 = hashlib.md5(rnds.encode())  # 在 Python 3 中需要编码成字节流
        value = md5.hexdigest()
        if value[start: start + str_len] == substr:
            # 碰撞双md5
            md5 = hashlib.md5(value.encode())  # 同样需要编码
            if md5.hexdigest()[start: start + str_len] == substr:
                print(f"{rnds} => {value} => {md5.hexdigest()}\n")
                stop_event.set()

if __name__ == '__main__':
    substr = sys.argv[1].strip()
    start_pos = int(sys.argv[2]) if len(sys.argv) > 2 else 0  # 修改了对 start_pos 的处理，防止缺少参数时报错
    str_len = len(substr)
    cpus = multiprocessing.cpu_count()
    stop_event = multiprocessing.Event()
    processes = [multiprocessing.Process(target=cmp_md5, args=(substr, stop_event, str_len, start_pos))
                 for _ in range(cpus)]  # 用 _ 代替 i，因为这里的 i 没有被使用
    for p in processes:
        p.start()
    for p in processes:
        p.join()

```
