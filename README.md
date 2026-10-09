# hackatsuon2026-projects

Hackatsuon 2026（気仙沼）で提出されたプロジェクトをまとめた 1 枚のサイト。

- `index.html` – ページ本体（ビルド不要、依存なし）
- `projects.json` – プロジェクトデータ（ここが正）
- `thumbs/` – 各プロジェクトのサムネイル
- `tools/make_thumbs.py` – サムネイル生成スクリプト

## データの更新

`projects.json` を直接編集してコミットすれば反映される。

| フィールド | 内容 |
|---|---|
| `id` | 英数字の識別子。サムネのファイル名とページ内アンカー（`#id`）に使う |
| `team`, `members`, `title`, `description` | フォームの提出内容。説明文は提出された言語のまま |
| `demo_url`, `source_url`, `slides_url`, `other_url` | リンク。ないものは `null` |
| `thumbnail` | サムネ画像のパス |
| `thumbnail_source` | サムネを撮った URL（`demo_url` と違う場合のため） |
| `award` | 受賞名。`null` なら非表示。値があるとカード左上に赤バッジが付き、先頭に並ぶ |

例: `"award": "最優秀賞 / Grand Prize"`

Final Submission Form のスプシからの取り込みは最初の 1 回だけ行い、以後はこの JSON で管理する。
（スプシ側の重複提出や表記ゆれはここで整理済み）

## サムネイルの更新

```sh
pip install playwright pillow
playwright install chromium
python3 tools/make_thumbs.py            # 無いものだけ生成
python3 tools/make_thumbs.py --force    # 全部撮り直し
python3 tools/make_thumbs.py --only gyoseki,galaxsi
```

撮影に失敗した URL は、タイトルから生成したカード画像で代替される。

## ローカルで見る

`fetch` で JSON を読むので、`file://` では開けない。

```sh
python3 -m http.server 8000
# http://localhost:8000/
```

## 公開

GitHub リポジトリの Settings → Pages → Branch: `main` / `(root)` で公開。
