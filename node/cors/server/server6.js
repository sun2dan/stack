let http = require("http");

let bodyData = {
  "code": 200, "data": {
    nick: 'sun2dan',
    url: 'https://ashita.top'
  }
};

http.createServer(function (request, response) {
  let origin = request.headers['origin'] || '*';
  let url = request.url;

  if (/demo1$/.test(url)) {
    // 特殊情况1：只在预检请求中返回 Access-Control-Allow-Origin: Content-Type
    // 真实请求依旧正常工作

    let headers = {
      'Access-Control-Allow-Origin': origin,
      'Access-Control-Allow-Headers': 'Content-Type',
    };

    if (request.method === "OPTIONS") {
      response.writeHead(200, headers);
      return response.end();
    }

    response.writeHead(200, {
      'Access-Control-Allow-Origin': origin,
      //'Access-Control-Allow-Headers': 'Content-Type',
    });
    bodyData.cookie = request.headers.cookie;
    response.write(JSON.stringify(bodyData));
    response.end();

  } else if (/demo2$/.test(url)) {
    // 特殊情况2：只在预检请求中返回 'Access-Control-Allow-Credentials': true
    // 浏览器报错，ajax没有获取到结果，但是开发者工具中可以看到返回的数据

    let headers = {
      'Access-Control-Allow-Origin': origin,
      'Access-Control-Allow-Headers': 'Content-Type',
      'Access-Control-Allow-Credentials': true,
    };
    if (request.method === "OPTIONS") {
      response.writeHead(200, headers);
      return response.end();
    }

    response.writeHead(200, {
      'Access-Control-Allow-Origin': origin,
      'Access-Control-Allow-Headers': 'Content-Type',
      //'Access-Control-Allow-Credentials': true,
    });
    bodyData.cookie = request.headers.cookie;
    response.write(JSON.stringify(bodyData));
    response.end();

  } else if (/demo3$/.test(url)) {
    // 特殊情况3：预检请求只返回响应头就可以，如果在预检请求中就返回响应体，浏览器依旧会接着发送第二个真实的请求；
    // 所以预检请求的时候，只返回响应头就可以，返回响应体会浪费资源、延长整个请求的时间；

    let headers = {
      'Access-Control-Allow-Origin': origin,
      'Access-Control-Allow-Headers': 'Content-Type',
      'Access-Control-Allow-Credentials': true,
    };
    if (request.method === "OPTIONS") {
      response.writeHead(200, headers);
      response.write(JSON.stringify(bodyData));
      return response.end();
    }

    response.writeHead(200, {
      'Access-Control-Allow-Origin': origin,
      'Access-Control-Allow-Headers': 'Content-Type',
      'Access-Control-Allow-Credentials': true,
    });
    bodyData.cookie = request.headers.cookie;
    response.write(JSON.stringify(bodyData));
    response.end();
  }
}).listen(8096);





