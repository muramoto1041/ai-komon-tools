# 桐 一括処理コマンド → ヘルプページ対応表

本文の URL は `https://www.kthree.co.jp/kihelp/cmd/stx/<page>.html`。
（`index.html?page=…` の形では本文が取れない。）

この表は `scripts/kiri_scan.py` が読み込んで使う。列の形式を変えないこと：
`| コマンド | 別名 | page | 備考 |`。別名・page が複数あるときは半角スペース区切り。
「コマンド」は行頭に書く形（2語のものは全角/半角スペース1つで区切って書く）。

目次: cg_home（一括処理コマンド 目次）。カテゴリ目次は cg_tbledt / cg_edt / cg_recedt / cg_frm / cg_file / cg_input / cg_total / cg_var / cg_prn / cg_prg / cg_chart / cg_xvw / cg_cond / cg_mail / cg_tblattr / cg_disp / cg_win / cg_etc。
関数は `https://www.kthree.co.jp/kihelp/fnc/fnc_home.html`（後半の「関数」節を参照）。

## 実行制御（cg_prg）

| コマンド | 別名 | page | 備考 |
|---|---|---|---|
| 注釈 | - | cccmtj | `*` 行・`/* */` も注釈（cccmtl, cccmt） |
| 終了 | - | ccsave | 一括処理の終了。イベントでは使用不可 |
| 終了 表 | - | csavetbl | 表を閉じる |
| 中止 | - | cccancel | |
| 中止 表 | - | cdest | |
| 実行終了 | - | ccclose | |
| 会話処理実行 | - | cedtrun | |
| 条件 | - | cccnd | `条件 (<条件式>) <コマンド>` |
| if | - | ccif | `else if ( )` 可。ブロックは end で閉じる |
| else | - | ccif | |
| end | - | ccif ccfor csws | if / for / switch を閉じる |
| ケース開始 | switch | csws | |
| ケース | case default | csws | `ケース その他` = default |
| ケース終了 | - | csws | 別名 end（if / for と共用のため end 行に記載） |
| ケース中止 | - | ccswb | |
| 繰り返し | loop while | ccloop ccwhile ccfor | 無条件 / `( 条件式 )` / `&i = 開始, 終了, 加算` |
| for | - | ccfor | `for … end` |
| 繰り返し終了 | - | ccloop | |
| 繰り返し中止 | break | ccwhileb | |
| 繰り返し継続 | - | cccntn | |
| 名札 | - | cclabel | `<名札名>：` 形式は cclabel2 |
| 分岐 | goto | ccbranch | 条件付きは `分岐 ( 条件式 )，名札` |
| 手続き定義開始 | proc | ceprocs ceprocsh | ハンドラは `<オブジェクト>::<イベント>( )` |
| 手続き定義終了 | - | ceproce | |
| 手続き終了 | - | cproce | |
| 手続き実行 | call | cprocn cprocl cprocrh | 条件付きは `手続き実行 ( 条件式 )，名前( )` |
| エラー処理 | - | cergoto | 手続き内では名札不可、`手続き名=` を使う |
| 遅延 | - | ccwait | |
| 実行制御 | - | cctrl | |
| コマンド | eval | cccmd | 制御構造は文字列で実行できない |
| 一括処理実行 | - | ccruncmd | |
| ライブラリ | load | cclib | イベントではメイン処理でのみ |
| システム | - | ccsys ccsysn | |
| シェル実行 | - | ccshell | |
| プロセス終了 | - | cpwait | |
| ブザー | - | ccbeep | |
| トレース出力 | - | cctracef | |
| トレース | - | cctrace cctracec | |

## 変数（cg_var）

| コマンド | 別名 | page | 備考 |
|---|---|---|---|
| 変数宣言 | - | cvarc | |
| 定数宣言 | - | cvarcns | |
| 代入 | - | cvarset | コマンド名は省略可（`&x = …`） |
| 局所変数代入 | - | cvarsetl | |
| 変数削除 | - | cvard | |
| 変数書き出し | - | cvarw | |
| 変数読み込み | - | cvarr | |

## フォーム連携（cg_frm）・ウィンドウ（cg_win）

| コマンド | 別名 | page | 備考 |
|---|---|---|---|
| オブジェクト操作 | object | cobjset cobjget | |
| 項目値代入 | - | crsetfld | |
| グループ値代入 | - | cgrpset | |
| メソッド呼び出し | method | cmethod | ヘルプ本文はほぼ空（見出しと別名のみ） |
| 使用フォーム | - | cwfmset cwfmuset | |
| ウィンドウ作成 | - | cwcreate | |
| ウィンドウ会話 | - | cwedit | |
| ウィンドウ終了 | - | cwclose | |
| ウィンドウ更新 | - | cwupdate | |
| 表示幅 | - | croww | |
| ウィンドウ位置 | - | cwposm cwposs cwposg | |
| ウィンドウリスト取得 | - | cwlist | |
| ウィンドウ情報取得 | - | cwinfo | |
| 表示位置 | - | cwposds cwposdg cwrel | |
| フォーム呼び出し | - | copenmdl | |

## 表の操作（cg_tbledt）・表の属性（cg_tblattr）

| コマンド | 別名 | page | 備考 |
|---|---|---|---|
| 表作成 | - | ccreatet | |
| 表 | - | copentbl cclsetbl | 引数なしの「表」は全表の終了 |
| 多重化 | - | copend | |
| 編集表 | - | cseltbl | |
| 結合 | - | copenviw | |
| 再抽出 | - | crefresh | |
| 保存表名 | - | csvname | |
| 利用者コード | - | ccuserc ccusercu | |
| 表整理 | - | ctpack | |
| ファイル属性 | - | cfileatr | |
| 項目属性変更２ | - | ctdfset2 | |
| 項目名変更 | - | ctdfname | |
| 属性自動設定 | - | ctdfauto | |
| 項目属性変更 | - | ctdfset | |

## 行の操作（cg_recedt）

| コマンド | 別名 | page | 備考 |
|---|---|---|---|
| 行挿入 | - | crins crinsu | |
| 行追加 | - | crapp crappu | |
| 行訂正 | - | credt credtu | |
| 行削除 | - | crdel crdela crdelu crdutlm | |
| 削除行 | - | crviwd | |
| 行復活 | - | crrcv crrcva crrcvl crrcvt | |
| 行退避 | - | crcopy | |
| 行復旧 | - | crundo | |
| 行番号 | - | crno | |
| ジャンプ | - | crjmpn crjmpm | |
| 行マーク定義 | - | crmark | |
| 行マーク解除 | - | crmarkd | |
| 検索 | - | crfind crfindn | |
| 並べ替え | - | crsort crsorti crsortn | |
| 整列解除 | - | cindcan | |
| 絞り込み | - | crsval crsname crsrep crsrepn crsunq crsunqn crsnum crsrev crsurow crsulmt | |
| 解除 | - | cselcana | |
| 絞り込み解除 | - | crscan | |
| 置換 | - | crrep crrepn crrepu | |
| グループ選択 | - | cgrpon | |
| グループ選択解除 | - | cgrpoff | |
| グループ追加 | - | cgrpapp cgrpappu | |
| グループ値訂正 | - | cgrpupd cgrpupdu | |
| グループ指定 | - | cgrpjmp | |
| グループ検索 | - | cgrpfnd cgrpfndu | |
| ロック | - | crrock crrocka crrocku | |
| ロック解除 | - | crrockc crrockca | |
| トランザクション | - | cctrz | |

## 会話処理（cg_edt）

| コマンド | 別名 | page | 備考 |
|---|---|---|---|
| 表形式編集 | - | cedttbl | |
| フォーム形式編集 | - | cedtwfm | |
| 処理行指定 | - | crselrow | |
| カーソル移動方向 | - | csetretc | |
| 空白文字 | - | cedtsets | |
| 会話検索 | - | cuifinds cuifindn cuifindd cuifindt cuifindu cuifindv | |
| 会話絞り込み | - | cuisels cuiseln cuiseld cuiselt cuiselu cuiselv | |
| ファイル管理 | - | cfileu | |
| 変数管理 | - | cvaru | |

## 入力（cg_input）・画面（cg_disp）・その他（cg_etc）

| コマンド | 別名 | page | 備考 |
|---|---|---|---|
| メッセージボックス | msgbox | cmsg | 正式パラメータ名は アイコン= / ボタン指定= / 制御文字展開= |
| 確認 | - | cmsgok | |
| キー入力 | - | cinkey | |
| 文字入力 | - | cinchar | |
| 機能キー入力 | - | cinakey | |
| ファイル名入力 | - | cinfname | |
| フォルダ名入力 | - | cdirun | |
| 値集合入力 | - | cindset | |
| 簡易メニュー | - | cqikmnu | |
| メニュー２ | - | cdspmnu2 | |
| メニュー３ | - | cdspmnu3 | |
| 表示制御 | - | cdspset | |
| 表示属性 | - | cdspatr | |
| 画面表示 | - | cdspput | |
| 画面消去 | - | cdspclr | |
| 表表示 | - | cdsptbl | |
| フォーム表示 | - | cdspwfm | |
| 行表示 | - | crviw | |
| 図形表示 | - | cdsppct | |
| メニュー | - | cdspmnu1 | |
| クリップボード | - | cgetclip csetclip | |
| サウンド | - | ccsnd ccsnde | |

## ファイル操作（cg_file）

| コマンド | 別名 | page | 備考 |
|---|---|---|---|
| データパス名 | - | cpathdat | |
| 画像パス名 | - | cpathpct | |
| 読み込み | - | crrtbl crrtxt crrk3 crrcsv crrpdf crrn | |
| 書き出し | - | crwt crwx crwk crwc crwr crwta crwn crwd | |
| 併合 | - | crmge crmgen | |
| ファイル変換 | - | ccnvcsvt ccnvtxtt ccnvodbc | |
| エクセル | - | cxlcnv | |
| エクセル書き出し | - | cxlw | |
| 印字開始 | - | couts | |
| 印字 | - | cout | |
| 印字終了 | - | coute | |
| ファイル入力開始 | - | cfileins | |
| ファイル入力 | - | cfilei | |
| ファイル入力終了 | - | cfileine | |
| ファイル削除 | - | cfiledel | |
| ファイル複写 | - | cfilecpy | |
| ファイル更新 | - | cfileupd | |
| ファイル移動 | - | cfilemov | |
| ファイル名変更 | - | cfileren | |
| フォルダ作成 | - | cdircre | |
| フォルダ削除 | - | cdirdel | |
| 表検査 | - | ctchk | |
| 表修復 | - | ctrcv | |
| 定義書き出し | - | cdoutviw cdoutxvw cdoutwfm cdoutrpt | |
| 一括書き出し | - | ccwc | |
| 一括読み込み | - | ccrc | |
| テキスト入力 | - | ctin | |
| テキスト出力 | - | ctout | |

## 集計（cg_total）・印刷（cg_prn）・グラフ（cg_chart）

| コマンド | 別名 | page | 備考 |
|---|---|---|---|
| 項目集計 | - | crttlrow | |
| 行集計 | - | crttl crttlr crttln | |
| データ行 | - | crviwt | |
| 行集計解除 | - | crttlc | |
| 転置集計 | - | crcrs crcrsn | |
| プリンタ | - | cprdrv | |
| 一覧表印刷 | - | cprtbl cprtblp cprtblh cprtblf | |
| 一覧表削除 | - | cprtbldn | |
| 一覧表印刷条件開始 | - | clprns | |
| 一覧表印刷条件 | - | clprnt clprnl clprnlg clprnn clprnd clprnr clprnh clprnfh clprnph clprnpf clprnff | |
| 一覧表印刷条件終了 | - | clprne | |
| レポート印刷 | - | cprrpt cprrptp cprrptm cprrpth cprrptf | |
| グラフ条件実行 | - | cgraphnv cgraphnp cgraphns | |
| グラフ条件削除 | - | cgraphnd | |
| グラフ条件開始 | - | cdgrpst | |
| グラフ条件 | - | cdgrpf cdgrpx cdgrpy cdgrpsy cdgrps cdgrpt cdgrpc1 cdgrpc2 cdgrpmf cdgrpsf | |
| グラフ条件終了 | - | cdgrpe | |

## 外部データベース（cg_xvw）・メール（cg_mail）

| コマンド | 別名 | page | 備考 |
|---|---|---|---|
| 外部DB | - | codbcc codbcuc codbcu | |
| 外部DB接続 | - | codbc | |
| メール設定 | - | cmlset | |
| メール受信 | - | cmlrcv | |
| メール送信 | - | cmlsnd | |
| メール切断 | - | cmloff | |
| メール解析 | - | cmlinf cmlgfile | |

## 処理条件（cg_cond）

| コマンド | 別名 | page | 備考 |
|---|---|---|---|
| 索引定義 | - | cindc | |
| 索引削除 | - | cindd | |
| 索引名変更 | - | cindren | |
| 並べ替え条件登録 | - | crsortia crsortna | |
| 並べ替え条件削除 | - | crsortnd | |
| 検索条件登録 | - | crfindna | |
| 検索条件削除 | - | crfindnd | |
| 絞り込み条件登録 | - | crsrepa crsunqa | |
| 絞り込み条件削除 | - | crsrepd crsunqd | |
| 置換条件登録 | - | crrepna | |
| 置換条件削除 | - | crrepnd | |
| 行集計条件登録 | - | crttlnad crttlna | |
| 行集計条件削除 | - | crttlnd crttlndd crttlnda | |
| 転置集計条件登録 | - | crcrsna | |
| 転置集計条件削除 | - | crcrsnd | |
| 読み込み条件登録 | - | crrntbl crrntxt crrnk3 crrncsv crrnpdf | |
| 読み込み条件削除 | - | crrnd | |
| 書き出し条件登録 | - | crwnat crwnatxt crwnak3 crwnacsv crwnarev crwnata crwnao | |
| 書き出し条件削除 | - | crwnd | |
| 併合条件登録 | - | crmgena | |
| 併合条件削除 | - | crmgend | |
| 表示条件開始 | - | cddspss | |
| 表示条件 | - | cddspsf | |
| 表示条件終了 | - | ctscae | |
| 表示条件読み込み | - | ctscr | |
| 表示条件書き出し | - | ctscw | |
| 表示条件削除 | - | ctscd | |
| 条件名変更 | - | ccndren | |
| 道具箱 | - | ctooladd ctooldel ctoolda | |
| 条件印字 | - | ccndprn | |
| 一括処理条件登録 | - | ccna | |
| 一括処理条件削除 | - | ccnd | |

## 関数（fnc_home）

関数は `https://www.kthree.co.jp/kihelp/fnc/<page>.html`。目次はカテゴリまでで、
個々の関数ページ名はカテゴリ目次を開いて確認する。

| カテゴリ | page |
|---|---|
| データ型変換 | fhome_cnv |
| 表の属性 | fhome_tblprop |
| 算術 | fhome_num |
| 表の状態 | fhome_tblstate |
| 文字列操作 | fhome_str |
| フォーム・レポート | fhome_frm |
| 文字種 | fhome_chrset |
| システム | fhome_sys |
| 日時 | fhome_date |
| ネットワーク | fhome_net |
| 集計 | fhome_au |
| 変数操作 | fhome_var |
| 比較・判定 | fhome_cond |
| 外部関数 | fhome_ext |
| 置換 | fhome_rep |
| ODBC（外部DB） | fhome_odbc |
| ファイル | fhome_file |
| その他 | fhome_other |
| レコードの属性 | fhome_recprop |
