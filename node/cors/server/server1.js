let http = require("http");

let bodyData = {
  "code": 200, "data": {
    nick: 'sun2dan',
    url: 'https://ashita.top'
  }
};

// test1-4 分别对应页面 test1-4.html
let resp = {
  test1(response, request) {
    let origin = request.headers['origin'] || '*';
    let headers = {
      'Access-Control-Allow-Origin': origin
    };
    response.writeHead(200, headers);

    bodyData.cookie = request.headers.cookie;
    response.write(JSON.stringify(bodyData));
    response.end();
  },
  test2(response, request) {
    let origin = request.headers['origin'] || '*';
    let headers = {
      'Access-Control-Allow-Origin': origin,
      'Access-Control-Allow-Credentials': true,
    };
    response.writeHead(200, headers);

    bodyData.cookie = request.headers.cookie;
    response.write(JSON.stringify(bodyData));
    response.end();
  },
  test3(response, request) {
    let origin = request.headers['origin'] || '*';
    let headers = {
      'Access-Control-Allow-Origin': origin,
      'Access-Control-Allow-Headers': 'Content-Type',
    };

    if (request.method === "OPTIONS") {
      response.writeHead(200, headers);
      return response.end();
    }

    response.writeHead(200, headers);
    response.write(JSON.stringify(bodyData));
    response.end();
  },
  test4(response, request) {
    let origin = request.headers['origin'] || '*';
    let headers = {
      'Access-Control-Allow-Origin': origin,
      'Access-Control-Allow-Headers': 'Content-Type',
      'Access-Control-Allow-Credentials': true,
    };

    if (request.method === "OPTIONS") {
      response.writeHead(200, headers);
      return response.end();
    }

    response.writeHead(200, headers);
    bodyData.cookie = request.headers.cookie;
    response.write(JSON.stringify(bodyData));
    response.end();
  },
};


http.createServer(function (request, response) {
  let refer = request.headers.referer;
  let matches = refer.match(/test(\d+)\.html/);

  if (matches && matches.length > 1) {
    let num = matches[1];
    if (num > 0 && num < 5) return resp['test' + num](response, request);
  }

  response.write('empty');
  response.end();
}).listen(8091);

