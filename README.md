# SecPulse

QA 資安/科技新聞聚合器。單一 HTML 檔案，GitHub Pages 部署，零依賴。

## 功能

- 5 個分類：資安動態 / 科技前沿 / Security / Tech & AI / Product Advisories
- Product Advisories 來源：HKCERT Security Bulletin（產品名 + 風險級別 + CVE 編號）
- 中文/英文新聞自動去重（跨 tab 同標題只保留一次）
- 每日重點（top 5，CVE 優先）
- 關鍵字即時搜尋
- 深色/淺色主題
- 繁中/EN 語言切換
- 1080p 無滾動

## 部署

1. 建一個 GitHub repo（例如 `testdatagen` 旁邊建 `secpulse`）
2. 將呢個資料夾所有內容 push 上去
3. 去 repo Settings → Pages → Source 選 `main` branch, root `/`
4. 等第一次 GitHub Actions 跑完（約 1-2 分鐘），`data.json` 就會有數據
5. 之後每 15 分鐘自動更新

## 新聞源

| Tab | 來源 |
|-----|------|
| 資安動態 | iThome 資安、iThome |
| 科技前沿 | iThome、INSIDE、TechOrange |
| Security | The Hacker News、BleepingComputer |
| Tech & AI | TechCrunch、The Verge |
| Product Advisories | HKCERT Security Bulletin |

## 技術

- 前端：單一 `index.html`（零依賴、零 build）
- 數據：GitHub Actions 每 15 分鐘抓 RSS → 寫入 `data.json` → commit
- CORS 問題：由 Actions server-side curl 解決，前端只 fetch 同域 JSON

## 檔案結構

```
├── index.html          # 前端
├── data.json           # 數據（Actions 自動更新）
└── .github/
    └── workflows/
        └── fetch-feeds.yml  # Actions workflow
```
