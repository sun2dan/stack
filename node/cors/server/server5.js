let http = require("http");
let fs = require("fs");

let bodyData = {
  "code": 200, "data": {
    nick: 'sun2dan',
    url: 'https://ashita.top'
  }
};

http.createServer(function (request, response) {
  let origin = request.headers['origin'] || '*';
  if (!origin) return response.end();

  // html 页面的响应
  let url = request.url;
  if (/^\/\w+\.html/.test(url)) {
    let html = fs.readFileSync("html" + url, "utf-8");
    response.writeHead(200, {'Content-Type': 'text/html'});
    response.write(html);
    return response.end();
  }

  // ajax 接口的响应
  response.writeHead(200, {});
  bodyData.cookie = request.headers.cookie;
  response.write(JSON.stringify(bodyData));
  response.end();
}).listen(8095);





