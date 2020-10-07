## 说明

只增加了匿名用户，允许写入
默认目录在 /Users/Haiyuan/vmshare
默认端口 2121


## py2app生成独立应用
$ rm -rf build dist
$ python setup.py py2app

#问题
发现有# import tkinter as tk 这个以后
做成的app，无法运行，暂时去掉


## 使用 sslforfree.com 生成证书

## 折腾了半天，完全没有用
因为运营商IP，封杀了80端口，因此let's Encrypt完全无法验证。
只能临时把域名指到外部vps，在用nginx申请，申请之后，再指回来

