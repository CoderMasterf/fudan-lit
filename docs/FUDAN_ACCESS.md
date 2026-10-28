# 复旦订阅库接入指引（附合规说明）

fudan-lit 对订阅库（CNKI / 万方 / 维普 / Web of Science / Scopus）的原则是：
**用它们自己的导出功能拿到 RIS / EndNote 文件，再用 `fudan-lit import` 导入**。
不扒接口、不批量下载全文。

## 前提：先连上复旦的订阅网络

- 在校内：连校园网（FudanNet / 图书馆机房）即可。
- 在校外：用复旦 **WebVPN**（https://webvpn.fudan.edu.cn ）或图书馆校外访问入口，UIS 登录后进入对应数据库。

## 各库导出位置

### CNKI（中国知网）

1. 检索后勾选需要的文献。
2. 点「导出与分析 → 导出文献」。
3. 左侧选 **EndNote** 格式（生成 `%0` 开头的 tagged 文本）。
4. 复制保存为 `.txt`（UTF-8），或直接「导出」下载。

> CNKI 的 EndNote 导出是「tagged」格式（`%0 / %A / %T / %D / %J ...`），
> fudan-lit 的 import 会识别并解析它。

### 万方 / 维普

同样走「导出 / 参考文献导出」，选 **EndNote** 或 **RIS**；能选 RIS 优先选 RIS。

### Web of Science

1. 检索后勾选记录。
2. 「导出 → EndNote Desktop」会生成 tagged 文本，或选「RIS」。
3. 存成文件导入。

### Scopus

1. 勾选记录 → 「Export」。
2. 格式选 **RIS format**（Citation information 至少勾 title / authors / year / DOI）。
3. 下载 `.ris` 导入。

## 导入

```bash
fudan-lit import cnki.txt wos.txt scopus.ris --format bibtex -o merged.bib
```

多个文件一次导入，内部会按 DOI / 标题+年份去重合并。

## 识别规则

import 会按内容自动判断格式：

- 以 `<record` 开头 → EndNote XML
- 含 `%0` 标签行 → EndNote tagged（CNKI / WoS 常见）
- 其余 → RIS（Scopus 常见）

## 合规边界（务必读）

1. **只导出元数据**（题名 / 作者 / 摘要 / DOI / 期刊），不要用脚本批量下载全文 PDF。
2. 订阅库内容受出版社与复旦的授权条款约束，**只用于个人学习研究**，不要二次公开传播导出结果。
3. 反爬是 CNKI 等库的重灾区，自动抓取接口可能导致你的 UIS 账号被限或封禁，且可能连累复旦校园 IP。本项目明确**不提供**这类能力。
4. 若需要稳定、合规的批量元数据，优先用 Web of Science / Scopus 的官方 API（需向图书馆或出版社申请机构 API key），或直接走开放源（Crossref / OpenAlex 已覆盖大部分英文文献的元数据）。
