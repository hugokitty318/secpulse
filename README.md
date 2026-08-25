# SecPulse

QA 資安/科技新聞聚合器。單一 HTML 檔案，GitHub Pages 部署，零依賴、零 token、零 Actions。

## 功能

- 5 個分類：資安動態 / 科技前沿 / Security / Tech & AI / Product Advisories
- Product Advisories 來源：HKCERT Security Bulletin（產品名 + 風險級別 + CVE 編號）
- 中文/英文新聞自動去重（跨 tab 同標題只保留一次）
- 每日重點（top 5，CVE 優先）
- 關鍵字即時搜尋
- 深色/淺色主題
- 繁中/EN 語言切換

## CORS 怎麼解決？

瀏覽器不允許 GitHub Pages 直接抓外部 RSS，所以頁面透過 **3 個公開 CORS 代理並行競速** 取回資料：

1. `rss2json` — JSON 格式，最快
2. `allorigins.win` — 原始 RSS XML，前端解析
3. `corsproxy.io` — 備援代理

任一代理成功即用其結果，無需手動更新資料檔、無需 GitHub Actions 或 token。

## 部署

1. 建 GitHub repo，push `index.html`（只需這一個檔案）
2. Repo → **Settings → Pages** → Source 選 `main` branch、root `/`
3. 開啟 `https://<username>.github.io/<repo>/` 給 QA 查看

每次 QA 開啟或按刷新，頁面會自動從新聞源拉最新資料。本機 `localStorage` 快取 10 分鐘以加速重複瀏覽。

## 新聞源

| Tab | 來源 |
|-----|------|
| 資安動態 | iThome 資安、iThome |
| 科技前沿 | iThome、TechOrange |
| 國際資安 | The Hacker News、BleepingComputer |
| 國際科技 | TechCrunch、The Verge |
| 漏洞公告 | HKCERT Security Bulletin |

## 檔案結構

```
├── index.html          # 前端（唯一必要檔案）
└── README.md
```

## 注意事項

- 代理服務為第三方免費服務，偶爾可能不穩定；按「刷新」可重試
- 若公司網路封鎖外部代理，可能無法載入；可改用本機 `python -m http.server` 測試
