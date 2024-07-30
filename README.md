# 搜书吧自动签到

使用 GitHub Actions 每天凌晨自动签到搜书吧。

## 配置

为了能够自动签到，需要设置几个 Actions secrets，如下：

| secrets           | 说明           | 例子                 |
| ----------------- | -------------- | -------------------- |
| SOUSHUBA_HOSTNAME | 搜书吧永久地址 | `www.soushu2030.com` |
| SOUSHUBA_USERNAME | 搜书吧用户名   |                      |
| SOUSHUBA_PASSWORD | 搜书吧密码     |                      |
