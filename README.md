# ai-komon-tools

業務アプリ（桐・Access・Excel など）の保守や検証を助ける、[Claude Code](https://code.claude.com/) 用のプラグインと VS Code 拡張機能の集まりです。

| 名前 | 種類 | 内容 | 入れ方 |
| --- | --- | --- | --- |
| [kiri-verify](#kiri-verify) | Claude Code プラグイン | 桐の一括処理・イベント処理を、桐オンラインヘルプと照合して検証する | Claude Code のコマンド（[下記](#インストールclaude-code-プラグイン)） |
| [Kiri Syntax](#kiri-syntax) | VS Code 拡張機能 | 桐の一括処理・イベント処理を色分け表示する | vsix ファイルを VS Code に入れる（[下記](#kiri-syntax)） |

2つは別々に入れます。どちらか一方だけでも使えます。

## インストール（Claude Code プラグイン）

Claude Code で次の2行を実行します。

```
/plugin marketplace add muramoto1041/ai-komon-tools
/plugin install kiri-verify@ai-komon-tools
```

2行目を実行すると詳細画面が開くので、入れる範囲（自分だけ／このリポジトリ など）を選ぶとインストールされます。

この手順で入るのは kiri-verify だけです。Kiri Syntax は下の「[VS Code 拡張機能](#vs-code-拡張機能)」の手順で入れてください。

### 更新

- **手動で更新する**：Claude Code で `/plugin` を開き、「Installed」タブで kiri-verify を選んで「Update now」を選びます。シェルからは `claude plugin update kiri-verify@ai-komon-tools` でも更新できます。
- **自動で更新する**：このマーケットプレイスは初期状態では自動更新されません。`/plugin` の「Marketplaces」タブで ai-komon-tools を選び、「Enable auto-update」を選ぶと、次から Claude Code の起動時に自動で更新されます。

更新を取り込んだあとは `/reload-plugins` を実行するか、Claude Code を開き直すと新しい版が使われます。

## 収録プラグイン

### kiri-verify

日本語データベース「桐」の一括処理（`.cmx`）・イベント処理（`.kex`）を書き出したテキストファイルを、[桐オンラインヘルプ](https://www.kthree.co.jp/kihelp/index.html)のコマンド書式と照合して検証します。

**使い方**：桐のファイルがあるフォルダで Claude Code を開き、次のように頼みます。

> この *.txt を検証して

明示的に呼ぶ場合は `/kiri-verify:kiri-verify` です。

**検証の内容**

1. **使用コマンドの洗い出し**：同梱のスクリプトで、ファイルごとに使っているコマンドを集計し、それぞれのヘルプページの URL を付けます。
2. **ヘルプとの照合**：書式が正しいかを確かめます。例：条件付きの `手続き実行` のカンマ抜け、ヘルプに記載のない比較式の書き方、`msgbox` のパラメータ名。
3. **本文のロジック確認**：表の開閉件数の食い違い、到達しない分岐、未定義の手続き、`終了状態=` がない箇所などを確認します。
4. **報告**：「直すべき箇所」「ヘルプに載っていない書き方」「使われないコード」「任意の改善」に分けて報告します。

**前提**

- 対象のファイルは、`<元の名前>_<元の拡張子>.txt`（例：`日次処理_cmx.txt`）という名前で、Shift-JIS で保存されたテキストです。
- スクリプトの実行に Python 3 が必要です。
- 検証のとき、ファイルは読むだけで、書き換えません。修正した `.txt` は、桐に取り込み直すまで動作に反映されません。

## VS Code 拡張機能

### Kiri Syntax

「桐 一括処理 (Kiri Syntax)」は、桐の一括処理（`.cmx`）・イベント処理（`.kex`）を書き出したテキストファイルを、VS Code で色分け表示する拡張機能です。命令・制御構文・変数（`&`）・関数（`#`）・項目（`[ ]`）・文字列・コメントを区別し、`IF`〜`END` や `手続き定義開始`〜`手続き定義終了` を折りたためます。

**インストール**：[kiri-syntax-0.1.1.vsix](vscode/kiri-syntax/kiri-syntax-0.1.1.vsix) をダウンロードし、VS Code の拡張機能ビュー（`Ctrl+Shift+X`）の「…」→「VSIX からのインストール...」で入れます。詳しくは[インストール手順](vscode/kiri-syntax/インストール手順.md)を見てください。

**前提**

- 名前が `_cmx.txt`・`_kex.txt` で終わるファイルは、設定なしで自動的に色が付き、Shift-JIS で開きます。
- それ以外の名前のファイルは、画面右下の言語の表示から「桐 一括処理」に切り替えます。
- ソースは [vscode/kiri-syntax](vscode/kiri-syntax/) にあります。文法は `scripts/build-grammar.js` で生成します。

## 注意

- 検証結果は、ヘルプの記載に基づく指摘です。本番で動いているコードの古い書式を「ヘルプに記載がない」と指摘することがあります。修正するかどうかは、動作を確認したうえで判断してください。
- 桐は株式会社管理工学研究所の製品です。このリポジトリのプラグイン・拡張機能は同社とは関係ありません。
