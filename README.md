# fudan-lit

复旦订阅范围内文献元数据抓取 CLI。按关键词从开放元数据源在线抓取论文的
**标题 / 作者 / 摘要 / DOI / PDF 链接**，也能把复旦订阅库（CNKI、Web of
Science、Scopus）**自己导出的 RIS / EndNote 文件**导入进来，去重后统一导出
CSV / BibTeX / JSON。

> 定位：抓**元数据**，不扒全文。订阅库走「官方导出 → 本工具导入」，不做
> WebVPN 反爬、不做批量全文下载——那既不稳，也违反出版社条款。

## 特性

- 四个**开放数据源**，无需登录即可在线抓取：
  - [Crossref](https://api.crossref.org)（全科，DOI 权威）
  - [OpenAlex](https://api.openalex.org)（全科，含开放获取 PDF 链接）
  - [arXiv](https://arxiv.org)（物理 / 数学 / CS 等预印本）
  - [Semantic Scholar](https://www.semanticscholar.org)（AI 语义检索，含开放 PDF）
- 订阅库（CNKI / 万方 / 维普 / WoS / Scopus）通过 **RIS / EndNote 文件导入**接入，规避反爬与合规风险。
- 按 DOI / 标题+年份**自动去重**，多源结果合并补全缺失字段。
- 导出 **CSV / BibTeX / JSON**，可直接进 Zotero / EndNote / LaTeX。
- 内置**礼貌限速**，填了 `MAILTO`（礼貌池邮箱）配额更宽松。

## 安装

要求 Python 3.9+。

```bash
git clone <你的仓库地址>
cd fudan-lit
pip install -e .
```

（可选）复制配置并填写：

```bash
cp .env.example .env
```

`.env` 里两项都可选：

| 变量 | 作用 |
| --- | --- |
| `MAILTO` | Crossref / OpenAlex 礼貌池邮箱，填复旦邮箱可拿更高配额 |
| `SEMANTIC_SCHOLAR_API_KEY` | 免费 API key，限速从 ~1 req/s 提到 ~100 req/s |

## 快速开始

按关键词在线抓元数据（默认四个开放源全开）：

```bash
fudan-lit search -k "graph neural network" -k "推荐系统" --format csv -o out.csv
```

只跑某几个源、限制条数：

```bash
fudan-lit search -k "transformer" --sources crossref,arxiv --limit 100
```

一次导出三种格式：

```bash
fudan-lit search -k "large language model" --format all -o results.csv
```

## 复旦订阅库怎么接入

订阅库不扒、不爬，用它们自己的导出功能：

1. 在 CNKI / 万方 / 维普 / Web of Science / Scopus 里检索（校园网或 WebVPN 登录）。
2. 勾选结果 → **导出 / Export** → 选 **RIS** 或 **EndNote** 格式，存成文件。
3. 导入本工具：

```bash
fudan-lit import cnki_export.ris wos_export.txt scopus_export.ris --format bibtex -o merged.bib
```

详细步骤和每个库的导出菜单位置见 [docs/FUDAN_ACCESS.md](docs/FUDAN_ACCESS.md)。

## 数据源一览

| 数据源 | 接入方式 | 需要登录？ | 说明 |
| --- | --- | --- | --- |
| Crossref | 在线 API | 否 | 全科元数据，DOI 最权威 |
| OpenAlex | 在线 API | 否 | 全科，含开放 PDF 链接 |
| arXiv | 在线 API | 否 | 预印本 |
| Semantic Scholar | 在线 API | 否（key 可选） | 语义检索，含开放 PDF |
| CNKI / 万方 / 维普 | 导出文件导入 | 是（UIS/WebVPN） | 中文库 |
| Web of Science | 导出文件导入 | 是（订阅） | 引文索引 |
| Scopus | 导出文件导入 | 是（订阅） | 文摘引文库 |

## 命令行参数

```
fudan-lit search -k KEYWORD [--sources S] [--limit N] [-o OUT] [--format F]
fudan-lit import FILES... [-o OUT] [--format F]
```

`--format` 可选 `csv` / `bibtex` / `json` / `all`。

## 合规边界（重要）

- 本工具只抓取**元数据与链接**，不下载订阅库全文 PDF。
- 开放 API 的使用遵守各自服务条款；已内置限速，请保留 `MAILTO`。
- CNKI / WoS / Scopus 的内容通过**官方导出功能**取得，属订阅范围内的正常使用。
- **请勿**改造本项目去批量扒 WebVPN / 订阅库接口：反爬会导致你的账号被封，批量下载还可能连累复旦校园 IP 被出版社限流。

## 目录结构

```
fudan-lit/
├── src/fudanlit/
│   ├── cli.py            # 命令行入口
│   ├── models.py         # Paper / Author 数据模型
│   ├── pipeline.py       # 关键词 × 数据源编排
│   ├── dedupe.py         # 去重合并
│   ├── export.py         # CSV / BibTeX / JSON
│   ├── config.py         # .env 读取
│   ├── importers.py      # RIS / EndNote 文件导入
│   └── sources/          # 四个开放数据源
├── docs/FUDAN_ACCESS.md  # 复旦订阅库导出指引 + 合规说明
├── tests/
└── pyproject.toml
```

## 开发与测试

```bash
pip install -e ".[dev]"
pytest
```

## License

MIT
