# SecPulse

QA 資安/科技新聞聚合器。GitHub Pages 部署。

## 運作方式

```
GitHub Actions 排程 → data.json（同域讀取，無 CORS）
         ↓（若 data.json 超過 30 分鐘未更新）
    開啟頁面時自動透過 jina.ai 補抓
```

## 部署檔案

```
index.html
data.json
favicon.svg
update_feeds.py
.github/workflows/update-data.yml
```

## 定時更新排程

### 排程時間

Workflow **Update News Data** 在 **UTC 每小時第 12、42 分**執行（香港時間約 **:12、:42**）。

### 若排程沒有自動跑（schedule = 0 次）

已確認你的 repo 是 **Public**，但 GitHub API 顯示 `schedule` 事件 **從未觸發過**（只有手動 `workflow_dispatch` 成功）。請依序檢查：

**① 啟用 Workflow**

1. 打開 **Actions** → **Update News Data**
2. 若看到黃色橫幅「This workflow was disabled」→ 點 **Enable workflow**
3. 右上角 **⋯** → 確認沒有被 Disable

**② 確認 Actions 權限**

**Settings → Actions → General → Workflow permissions**  
選 **Read and write permissions** → Save

**③ 重新註冊排程（建議）**

Push 新版 `.github/workflows/update-data.yml`（已取代舊的 `fetch-feeds.yml`），然後：

1. 到 Actions 手動 **Run workflow** 一次
2. 等下一個 **:12 或 :42（UTC）** 看是否出現 `schedule` 觸發紀錄

**④ 驗證是否成功**

Actions 篩選 Event = **schedule**，或看 `data.json` 的 `ts` 是否更新。

### 排程仍不行時的備援

即使 Actions 排程失敗，**QA 開啟頁面時**：

- 先快速顯示 `data.json`
- 若超過 30 分鐘未更新，自動背景補抓最新新聞

也可手動 **Run workflow** 更新 `data.json`。

## 本機手動更新

```bash
python update_feeds.py
git add data.json && git commit -m "Update feeds" && git push
```
