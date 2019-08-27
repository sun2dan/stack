# 跨域请求测试实例
文章地址：[https://ashita.top/front/cors.html](https://ashita.top/front/cors.html)

## 运行
需要配置的hosts：
```
127.0.0.1 test.com a.test.com b.test.com server.com
```

程序入口：main.js

运行步骤：
1. node main.js
2. 在浏览器中访问：http://test.com:8090/menu.html，点击链接，进入对应的页面；
3. 打开开发者工具的Network，查看XHR请求；


## server 文件夹
- server.html.js : html页面所在的服务器；端口8090；
- server1.js : 带/不带cookie，简单/复杂请求，四种情况的测试；端口8091；  
- server5.js : 验证同域下复杂请求没有预检；端口8095；
- server6.js : 三种特殊情况的验证；端口8096；

## html 文件夹
- menu.html : 测试页面入口
- server1-6.html：参照 menu.html 中的导航文案；
