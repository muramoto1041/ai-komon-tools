// 桐 一括処理の TextMate 文法を生成する
//   node scripts/build-grammar.js
// 正規表現は String.raw で書き、JSON のエスケープはこのスクリプトに任せる
const fs = require('fs');
const path = require('path');

// 名前（変数名・関数名・項目名・命令名）を区切る文字。桐は全角・半角の記号を区別しない
const DELIM = String.raw`\s　,，=＝<>＜＞+＋\-－*＊/／(（)）{｛}｝\[［\]］"”“.:：;；!！?？`;
const NAME = `[^${DELIM}]+`;
const WS = String.raw`[\s　]`;
const WORD_END = `(?![^${DELIM}])`; // 後ろが区切り文字か行末

const CONTROL = [
  '手続き定義終了', '手続き終了',
  'ケース開始', 'ケース終了', 'ケース中止', 'ケース',
  '繰り返し終了', '繰り返し中止', '繰り返し',
  '一括処理実行', 'エラー処理',
].join('|');
const CONTROL_RE = `(?:${CONTROL}|(?i:if|else|end))`;

const TYPES = ['長整数', '整数', '数値', '文字列', '文字', '日時', '通貨', '実数', '論理', 'オブジェクト'].join('|');
const SCOPES = ['共通', '共有', '固有', '局所'].join('|');

const grammar = {
  $schema: 'https://raw.githubusercontent.com/martinring/tmlanguage/master/tmlanguage.json',
  name: '桐 一括処理',
  scopeName: 'source.kiri',
  patterns: [
    { include: '#comment' },
    { include: '#declaration' },
    { include: '#condition' },
    { include: '#procedure-definition' },
    { include: '#label' },
    { include: '#call' },
    { include: '#control' },
    { include: '#command' },
    { include: '#expressions' },
  ],
  repository: {
    // 行頭（字下げ可）の * ／ ＊ はコメント
    comment: {
      name: 'comment.line.asterisk.kiri',
      match: `^${WS}*[*＊].*$`,
    },
    // 変数宣言　共通,文字列{&a,&b}
    declaration: {
      begin: `^(${WS}*)(変数宣言)${WORD_END}`,
      beginCaptures: { 2: { name: 'storage.type.declaration.kiri' } },
      end: '$',
      patterns: [
        { name: 'storage.modifier.kiri', match: `(?:${SCOPES})(?=${WS}*[,，])` },
        { name: 'storage.type.kiri', match: `(?:${TYPES})(?=${WS}*[{｛])` },
        { include: '#expressions' },
      ],
    },
    // 条件（式）命令 … 括弧の後ろの命令も色分けする
    condition: {
      begin: `^(${WS}*)(条件)${WS}*(?=[(（])`,
      beginCaptures: { 2: { name: 'keyword.control.kiri' } },
      end: '$',
      patterns: [
        {
          match: `(?<=[)）])(${WS}*)(手続き実行|分岐)${WS}+([^\\s　&＆#＃,，]+)`,
          captures: {
            2: { name: 'keyword.control.kiri' },
            3: { name: 'entity.name.function.kiri' },
          },
        },
        {
          match: `(?<=[)）])(${WS}*)(${CONTROL_RE})${WORD_END}`,
          captures: { 2: { name: 'keyword.control.kiri' } },
        },
        {
          match: `(?<=[)）])(${WS}*)(${NAME})`,
          captures: { 2: { name: 'keyword.other.command.kiri' } },
        },
        { include: '#expressions' },
      ],
    },
    // 手続き定義開始　名前(引数)
    'procedure-definition': {
      match: `^(${WS}*)(手続き定義開始)${WS}*([^\\s　(（]+)`,
      captures: {
        2: { name: 'keyword.control.kiri' },
        3: { name: 'entity.name.function.kiri' },
      },
    },
    // 名札　名前
    label: {
      match: `^(${WS}*)(名札)${WS}+([^\\s　]+)`,
      captures: {
        2: { name: 'keyword.control.kiri' },
        3: { name: 'entity.name.function.label.kiri' },
      },
    },
    // 手続き実行　名前 ／ 分岐　名札
    call: {
      match: `^(${WS}*)(手続き実行|分岐)${WS}+([^\\s　&＆#＃,，]+)`,
      captures: {
        2: { name: 'keyword.control.kiri' },
        3: { name: 'entity.name.function.kiri' },
      },
    },
    control: {
      match: `^(${WS}*)(${CONTROL_RE})${WORD_END}`,
      captures: { 2: { name: 'keyword.control.kiri' } },
    },
    // 上記以外の行頭の語は命令
    command: {
      match: `^(${WS}*)([^\\s　&＆#＃*＊\\[［"”“(（)）,，=＝<>＜＞{｛}｝]+)`,
      captures: { 2: { name: 'keyword.other.command.kiri' } },
    },
    expressions: {
      patterns: [
        { include: '#string' },
        { include: '#field' },
        { include: '#variable' },
        { include: '#function' },
        { include: '#logical' },
        { include: '#constant' },
        { include: '#number' },
        { include: '#parameter' },
        { include: '#parens' },
        { include: '#operator' },
      ],
    },
    // "…" ”…” “…” は混在可。閉じ忘れても行末で打ち切る
    string: {
      name: 'string.quoted.kiri',
      begin: '["”“]',
      end: '["”“]|$',
      patterns: [{ name: 'constant.character.escape.kiri', match: String.raw`\\n` }],
    },
    // [項目名] ／ ［項目名］ ／ 配列の添字
    field: {
      name: 'entity.name.type.field.kiri',
      begin: '[\\[［]',
      end: '[\\]］]|$',
      patterns: [{ include: '#variable' }, { include: '#function' }, { include: '#number' }],
    },
    variable: {
      name: 'variable.other.kiri',
      match: `[&＆]${NAME}`,
    },
    function: {
      name: 'support.function.kiri',
      match: `[#＃]${NAME}`,
    },
    logical: {
      name: 'keyword.operator.logical.kiri',
      match: '(?i)[.．](?:and|or|not|xor)(?![a-z])',
    },
    constant: {
      name: 'constant.language.kiri',
      match: `(?<=[=＝])(?:する|しない|許可|禁止)${WORD_END}`,
    },
    number: {
      name: 'constant.numeric.kiri',
      match: `(?<![^${DELIM}])[0-9０-９]+(?:[.．][0-9０-９]+)?${WORD_END}`,
    },
    // 終了状態=&確認 のようなパラメータ名
    parameter: {
      name: 'entity.other.attribute-name.kiri',
      match: `${NAME}(?=${WS}*[=＝])`,
    },
    // 括弧は入れ子に対応。閉じ忘れても行末で打ち切る
    parens: {
      begin: '[(（]',
      end: '[)）]|$',
      patterns: [{ include: '#expressions' }],
    },
    operator: {
      name: 'keyword.operator.kiri',
      match: '[=＝<>＜＞+＋\\-－*＊/／]',
    },
  },
};

const out = path.join(__dirname, '..', 'syntaxes', 'kiri.tmLanguage.json');
fs.mkdirSync(path.dirname(out), { recursive: true });
fs.writeFileSync(out, JSON.stringify(grammar, null, 2) + '\n', 'utf8');
console.log('wrote', out);
