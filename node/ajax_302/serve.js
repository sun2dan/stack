/**
 * Created by dandan on 2019-10-09.
 * vision:1.0
 * title:
 * e-mail: supericesun@gmail.com
 */

var http = require("http");
var fs = require("fs");
var index = 1;

http.createServer(function (request, response) {
  var origin = request.headers['origin'] || '*';
  if (!origin) return response.end();

  // html 页面的响应
  var url = request.url;
  if (/^\/\w+\.html/.test(url)) {
    var html = fs.readFileSync("ajax_302/" + url, "utf-8");
    response.writeHead(200, {'Content-Type': 'text/html'});
    response.write(html);
    return response.end();
  }

  // 重定向过来的，能加载到的页面
  if (/redirect$/.test(url)) {
    var html = fs.readFileSync("ajax_302/redirect.html", "utf-8");
    response.writeHead(200, {'Content-Type': 'text/html'});
    response.write(html);
    return response.end();
  }

  // 重定向过来的，404情况
  if (/404$/.test(url)) {
    //var html = fs.readFileSync("ajax_302/404.html", "utf-8");
    response.writeHead(404, {'Content-Type': 'text/html'});
    response.write('');
    return response.end();
  }

  // ajax 接口的响应
  var type = index % 3;
  var path = '';

  // type: 0, redirect - 测试同域重定向，页面加载成功，
  // type: 1, 404 - 测试同域重定向，页面加载失败
  // type: 2, 测试跨域情况下，ajax中的状态码
  if (type === 2) path = 'http://ashita.com';
  else path = 'http://test.com:8098/' + ['redirect', '404'][type];

  index++;
  response.writeHead(302, {Location: path});
  response.end();
}).listen(8098);






