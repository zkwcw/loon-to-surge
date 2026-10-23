# enhanced/ — 手工维护的增强模块

这个目录**不受每日自动转换流水线影响**：`scripts/` 里的 cron 只重建 `modules/` 和根目录 `README.md`，改不到这里。

## xianyu-enhanced.sgmodule — 闲鱼去广告（增强版）

基线是上游 [可莉 FleaMarket_remove_ads](https://github.com/luestr/ProxyResource)（2026-10-02）的
**17 条 Body Rewrite + 7 条 Map Local**，原样保留；相对上游只做三处增强：

| 增强点 | 原因 |
|---|---|
| `[MITM] hostname = %APPEND% *.goofish.com` | 上游只 MITM 了 `acs.` / `g-acs.` 两个域名，接口换子域就会绕过改写 |
| `[Rule]` 追加阿里广告联盟域名 REJECT | `tanx` / `alimama` / `amdc` / `adash` / `danuoyi` / `mmstat` 是广告投放与统计，非闲鱼自有域名 |
| `[Rule]` 顺带止噪 | `qiezibenpao` / `comfylink` / `tianwenca` 长期重试超时 |

### 与 `modules/闲鱼去广告.sgmodule` 的关系

**二选一启用，不要同时开**（两条改写链会重复处理同一响应）。

- `modules/闲鱼去广告.sgmodule`：每日由上游自动转换，跟上游走，不含增强
- `enhanced/xianyu-enhanced.sgmodule`：本文件，手工维护，含增强

### 安装

`raw.githubusercontent.com` 在国内时通时断，**优先用 jsDelivr**：

```
https://cdn.jsdelivr.net/gh/zkwcw/loon-to-surge@main/enhanced/xianyu-enhanced.sgmodule
```

一键安装：

```
surge:///install-module?url=https%3A%2F%2Fcdn.jsdelivr.net%2Fgh%2Fzkwcw%2Floon-to-surge%40main%2Fenhanced%2Fxianyu-enhanced.sgmodule
```

备用镜像（jsDelivr 不通时）：`fastly.jsdelivr.net` / `gcore.jsdelivr.net`，路径相同。

### 可选：拦截广告上报接口

文件末尾有两条**注释掉**的 Map Local 规则，作用于：

- `mtop.idle.idleadv.app.launch.report` — 开屏广告曝光回执
- `mtop.idle.idleadv.scene.restore` — 广告场景恢复

只做回执，拦掉不影响界面；长期可能降低开屏广告填充率。需要时把 `[Map Local]` 段里对应注释行取消即可。

### 变更记录

- `2026-10-24` 整理结构；与上游对比差异写入注释；移除临时诊断脚本；标注可选的上报拦截
