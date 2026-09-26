/*
 * 12306 广告请求拦截（Surge）
 * 自托管：避免运行时依赖 kelee.one；后者目前对本网络返回 Cloudflare 403。
 * 来源逻辑：RuCu6 / 可莉 12306 去广告规则；适配 Surge 原生 response。
 */

const headers = $request.headers || {};
const operation = headers["Operation-Type"] || headers["operation-type"] || "";

const blockedOperations = new Set([
  "com.cars.otsmobile.integration.activityBanner", // 活动横幅
  "com.cars.otsmobile.memberInfo.getMemberQa", // 铁路会员常见问题推广
  "com.cars.otsmobile.newHomePage.initData", // 首页热门资讯
  "com.cars.otsmobile.newHomePageBussData", // 商品信息流
  "com.cars.otsmobile.paySuccBuss.bussEntryShow", // 支付成功页商业推广
]);

if (blockedOperations.has(operation)) {
  // 对这些独立广告/推广请求直接返回空成功响应，避免影响同一 MGW 地址上的购票业务请求。
  $done({
    response: {
      status: 204,
      headers: { "Content-Type": "application/json" },
      body: "",
    },
  });
} else {
  $done({});
}
