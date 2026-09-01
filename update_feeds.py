"""Fetch RSS feeds and write data.json for GitHub Pages."""
import html, json, os, re, urllib.request, xml.etree.ElementTree as ET
from datetime import datetime, timezone

FEEDS = [
    ("iThome資安", "https://www.ithome.com.tw/rss/security", "cn_sec"),
    ("iThome", "https://www.ithome.com.tw/rss/", "cn_sec"),
    ("iThome", "https://www.ithome.com.tw/rss/", "cn_tech"),
    ("TechOrange", "https://feeds.feedburner.com/techorange", "cn_tech"),
    ("TheHackerNews", "https://feeds.feedburner.com/TheHackersNews", "en_sec"),
    ("BleepingComputer", "https://www.bleepingcomputer.com/feed/", "en_sec"),
    ("TechCrunch", "https://techcrunch.com/feed/", "en_tech"),
    ("TheVerge", "https://www.theverge.com/rss/index.xml", "en_tech"),
    ("HKCERT", "https://www.hkcert.org/getrss/security-bulletin", "cve"),
]

def fetch_feed(name, url, timeout=15):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 SecPulse/1.0"})
        data = urllib.request.urlopen(req, timeout=timeout).read().decode("utf-8", errors="replace")
        if not re.search(r"<rss|<feed|<item|<entry", data, re.I):
            print(f"  SKIP {name}: not XML")
            return []
        root = ET.fromstring(data)
        items = []
        for item in root.iter("item"):
            t = (item.findtext("title") or "").strip()
            l = (item.findtext("link") or "").strip()
            d = (item.findtext("pubDate") or "").strip()
            dr = (item.findtext("description") or "").strip()
            desc = html.unescape(re.sub(r"<[^>]*>", "", dr)).strip()[:250]
            if t:
                items.append({"title": t, "link": l, "pubDate": d, "description": desc, "source": name})
        if not items:
            ns = {"a": "http://www.w3.org/2005/Atom"}
            for e in root.findall(".//a:entry", ns):
                t = (e.findtext("a:title", namespaces=ns) or "").strip()
                le = e.find("a:link[@rel='alternate']", ns)
                if le is None:
                    le = e.find("a:link", ns)
                l = (le.get("href") or "").strip() if le is not None else ""
                d = (e.findtext("a:published", namespaces=ns) or e.findtext("a:updated", namespaces=ns) or "").strip()
                dr = (e.findtext("a:summary", namespaces=ns) or e.findtext("a:content", namespaces=ns) or "").strip()
                desc = html.unescape(re.sub(r"<[^>]*>", "", dr)).strip()[:250]
                if t:
                    items.append({"title": t, "link": l, "pubDate": d, "description": desc, "source": name})
        if name == "HKCERT":
            for it in items:
                x = it.get("description", "")
                s = "medium"
                if re.search(r"critical|極高", x, re.I):
                    s = "critical"
                elif re.search(r"high risk|高度", x, re.I):
                    s = "high"
                cves = re.findall(r"CVE-\d{4}-\d+", x)
                it["severity"] = s
                it["cveIds"] = ", ".join(dict.fromkeys(cves))
                it["products"] = it["title"].replace("Multiple Vulnerabilities", "").strip()
        print(f"  OK {name}: {len(items)} items")
        return items[:15]
    except Exception as ex:
        print(f"  FAIL {name}: {type(ex).__name__}: {ex}")
        return []

def main():
    tabs = {"cn_sec": [], "cn_tech": [], "en_sec": [], "en_tech": [], "cve": []}
    for name, url, tab in FEEDS:
        tabs[tab].extend(fetch_feed(name, url))
    for key in tabs:
        seen = set()
        unique = []
        for it in sorted(tabs[key], key=lambda x: x.get("pubDate", ""), reverse=True):
            k = (it.get("title", "") or "").strip().lower()
            if not k or k in seen:
                continue
            seen.add(k)
            unique.append(it)
        tabs[key] = unique[:20]
    cn_sec_titles = {it.get("title", "").strip().lower() for it in tabs["cn_sec"]}
    tabs["cn_tech"] = [it for it in tabs["cn_tech"] if (it.get("title", "") or "").strip().lower() not in cn_sec_titles]
    data = {"ts": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"), "tabs": tabs}
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Wrote {out} ({sum(len(v) for v in tabs.values())} items)")

if __name__ == "__main__":
    main()
