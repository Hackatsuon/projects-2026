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
| `team`, `members`, `title` | フォームの提出内容 |
| `description_ja`, `description_en` | 説明文。ページ右上の切り替えで表示言語が変わる |
| `generated` | `"ja"` か `"en"`: その言語の説明文は運営が翻訳したもの（カードに注記が出る）。両方とも提出者本人の文なら `null` |
| `demo_url`, `source_url`, `slides_url`, `other_url` | リンク。ないものは `null` |
| `thumbnail` | サムネ画像のパス。デモ画面は `thumbs/<id>.jpg`、スライド 1 枚目は `thumbs/slides/<id>.jpg`。どちらを使うかはこのパスで切り替える |
| `thumbnail_source` | サムネを撮った URL（`demo_url` と違う場合のため） |
| `award` | 受賞名の文字列。`null` なら非表示。値があるとカード内のチーム名の右に黄色いバッジで表示され、受賞プロジェクトが先頭に並ぶ（JSON の順序どおり） |

例: `"award": "最優秀賞 / Grand Prize"`

`event.links` はヘッダーとフッターに出るリンク（`label`, `label_en`, `url`）。

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
