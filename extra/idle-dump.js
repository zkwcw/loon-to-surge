// 闲鱼 mtop 响应体回传（诊断用，不修改响应）
// 目标：局域网 Mac 上的接收端，保存 JSON 供离线分析
const RECEIVER = "http://192.168.31.79:8099/dump";
const CAP = 300000; // 最多回传 300KB

let finished = false;
function finish() {
  if (!finished) { finished = true; $done({}); }
}

try {
  const url = ($request && $request.url) || "";
  const body = ($response && $response.body) || "";
  if (!body) { finish(); }
  else {
    try { if (typeof setTimeout === "function") setTimeout(finish, 3000); } catch (e) {}
    $httpClient.post({
      url: RECEIVER,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: url, len: body.length, body: body.slice(0, CAP) })
    }, function () { finish(); });
  }
} catch (e) {
  finish();
}
