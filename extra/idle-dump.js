// 闲鱼 mtop 响应体回传（诊断用，不修改响应）
// v2：无论有没有 body 都回传一条心跳，便于判断脚本到底有没有跑
const RECEIVER = "http://192.168.31.79:8099/dump";
const CAP = 900000;

let finished = false;
function finish() { if (!finished) { finished = true; $done({}); } }

function post(payload, cb) {
  try {
    $httpClient.post({
      url: RECEIVER,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    }, function () { if (cb) cb(); });
  } catch (e) { if (cb) cb(); }
}

try {
  const url = ($request && $request.url) || "";
  let body = "";
  let note = "";
  if (typeof $response === "undefined" || $response === null) {
    note = "no $response object";
  } else {
    body = $response.body || "";
    if (!body) note = "response.body empty (requires-body not effective?)";
  }
  const payload = {
    url: url,
    len: body.length,
    status: (typeof $response !== "undefined" && $response && $response.status) || 0,
    note: note,
    body: body.slice(0, CAP)
  };
  try { if (typeof setTimeout === "function") setTimeout(finish, 3000); } catch (e) {}
  post(payload, finish);
} catch (e) {
  post({ url: "", len: 0, note: "script error: " + (e && e.message) }, finish);
  finish();
}
