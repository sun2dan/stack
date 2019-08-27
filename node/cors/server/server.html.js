let http = require("http");
let fs = require("fs");

http.createServer(function (request, response) {
  let headers = {
    'Set-Cookie': [
      //getCookieStr('.test.com'),
      getCookieStr('test.com'), //==> domain->.test.com
      getCookieStr('server.com'),
      getCookieStr('a.test.com'),
      getCookieStr('b.test.com'),
      getCookieStr('localhost')
    ],
    'Content-Type': 'text/html'
  };

  let url = request.url;

  if (/^\/\w+\.html/.test(url)) {
    let html = fs.readFileSync("html" + url, "utf-8");
    response.writeHead(200, headers);
    response.write(html);
  } else {
    let html = fs.readFileSync("html/menu.html", "utf-8");
    response.writeHead(200, headers);
    response.write(html);
  }

  response.end();


  function getCookieStr(domain) {
    var date = new Date();
    date.setTime(date.getTime() + 100 * 60 * 60 * 24 * 20);
    return 'value=' + domain + '; expires=' + date.toGMTString() + '; domain=' + domain + '; HttpOnly';
  }
}).listen(8090);


