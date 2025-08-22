---
created: 2025-08-20
date: 2025-08-20T22:53:23
author: shindy
tags:
  - Hugo
  - GitHub
  - GitHub-Actions
  - GitHub-Pages
---
# HugoとGitHubでObsidianで書いたメモを公開してみた

ObsidianのVault内ドキュメントの一部を[Hugo](https://gohugo.io/)という静的サイトジェネレータを用いてGitHub Pagesで公開してみました。

## 使用するもの
- MacBook Air M3
- VS Code ... Hugo環境デバッグ
- Obsidian ... ドキュメントの更新
- [Homebrew](https://brew.sh/ja/) ... パッケージマネージャ（Hugoインストール用）
- Git ... ファイルバージョン管理（`brew install git`でインストール可能）
- GitHubアカウント ... GitHubのサービスをフル活用するので必要
- （任意）Gitクライアント ... GitHub Desktop、VS Codeの拡張機能、SourceTree等使いやすいもの

## ObsidianのVault構成と命題
ObsidianのVaultはGitHubのプライベートリポジトリで現在管理しています。私の場合、技術系ドキュメントと日記をひとつのVaultで管理しているので、技術系ドキュメントのみを公開する方法を模索していました。
```text
├── .git/                  # git
├── .obsidian/         # Obsidianの設定
├── diary/               # 日記
├── docs/               # 技術系のドキュメント
├── assets/             # 画像や資料アセット（docs用）
├── LICENSE           # リポジトリのライセンスファイル
└── README.md     # リポジトリのREADMEファイル
```

## 今回の方針
Vault内の「docs」や「assets」フォルダの内容だけを公開するために、以下の手順を実施します。以降登場するリポジトリ名やブランチ名は任意になります。
1. Publicリポジトリ`shindys-note`を作成する
   └ Hugo環境をデフォルトブランチに構築する
2. GitHub Pages公開用ブランチ`gh-pages`を構築する
3. Vault内対象フォルダの内容を`master`へ同期する
4. `gh-pages`ブランチをGitHub Pagesで公開する

## 1. Publicリポジトリ`shindys-note`を作成する
### Hugoインストール
[macOS](https://gohugo.io/installation/macos/)
```bash
brew install hugo
```
### Hugo siteの作成 & 空ディレクトリ内に.gitkeepを作成
任意のディレクトリに移動してから以下コマンドを実行してください。
```bash
# Hugo siteの作成
hugo new site shindys-note
cd shindys-note

# 空ディレクトリ内に.gitkeep（中身のないファイル）を作成（空のディレクトリはGitの追跡対象外となるため）
find . -type d -empty -exec touch {}/.gitkeep \;
```
### Gitの初期化
```bash
# デフォルトブランチである`master`や`main`が作成される
git init
```
### （任意）.gitignoreのおすすめ設定
.gitignoreファイルは格納しておくと中に記述したパスをGitが自動で追跡対象外してくれます。
```.gitignore
# Hugo build output
/public/
/resources/_gen/
/hugo_stats.json
/.hugo_build.lock

# Logs and OS files
*.log
.DS_Store
Thumbs.db

# VSCode settings
.vscode/
.history/

# Node stuff (もしnpmでテーマ管理する場合は必要)
node_modules/

# Env files
.env
.env.* 

# Backup files
*~
```

### サイトの基本情報やテーマ変更やローカルでのテスト方法
GitHubへpushする前にちゃんと自分の好きなテーマで記事がちゃんと表示されるかテストしましょう。

#### 基本情報（URLや言語、タイトル等）
hugo.toml内で設定できます。
```toml
# github pagesのURLは基本は以下の形式です
# https://<githubユーザ名>.github.io/リポジトリ名/
baseURL = 'https://shindy-dev.github.io/shindys-note/'

languageCode = 'ja-JP'
title = 'My New Hugo Site'
```

#### テーマ変更
テーマは[Hugo Themes](https://themes.gohugo.io/)に一覧があります。今回は`ananke`に変更する例
```bash
git submodule add https://github.com/theNewDynamic/gohugo-theme-ananke.git themes/ananke
# 設定ファイルのthemeを設定できればOK
echo 'theme = "ananke"' >> hugo.toml
```
#### post追加
以下のコマンドで`/archetypes/default.md`をテンプレートとして`/content/posts/hello.md`を作成します。あくまでテスト用なので、自分であらかじめ作成したドキュメントを`/content/posts`へ格納してテストしていただいても構いません。テスト用のドキュメントをコミット時に対象とするかは自己判断でお願いします。
```bash
hugo new posts/hello.md
```
#### ローカルサーバー起動
```bash
hugo server -D
```
- `-D` は下書き（draft = trueの記事）も表示するオプションです。  
- 起動後ブラウザで確認 → デフォルトURL：[http://localhost:1313](http://localhost:1313)  
- 保存するたびに自動でリロードしてくれます。


好みのテーマで作成した記事が表示されたら確認は終わりです。今回は細かなレイアウトの修正は割愛します。
![](../assets/Pasted%20image%2020250821215604.png)

### `shindys-note`をGitHub へ Publicリポジトリとして公開
GitHubのリモートリポジトリの作成方法は多種多様なので、ご自身に合うやり方で公開してください。
- Gitクライアント（GitHub Desktop等）
- GitHub CLI
- GitHub

.gitignoreの内容にもよりますが、GitHubへは以下の構成がpushされるはずです。
```text
├── .git
├── archetypes
├── data
├── i18n
├── layouts
├── static
├── themes
├── .gitignore
├── .gitmodules
├── hugo.toml
├── LICENSE
└── README.md
```

### 2. GitHub Pages公開環境を`gh-pages`ブランチに構築する
ここでは、GitHub Actionsを使用して`shindys-note`のデフォルトブランチに更新があった際に、自動でHugoによるビルドを行い成果物をgh-pagesへ反映する仕組みを構築します。手順としては以下の内容を記述した`.github/workflows/deploy.yml`を`shindys-note`のデフォルトブランチで作成し、pushするだけです。以下テキストのコメント部分は適宜修正してください。
```yml
name: Deploy Hugo site to GitHub Pages

on:
  push:
    branches:
      - master  # mainの場合はここを書き換える

jobs:
  build-deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3
        with:
          submodules: true # テーマをサブモジュールにしてる場合

      - name: Setup Hugo
        uses: peaceiris/actions-hugo@v3
        with:
          hugo-version: '0.148.2'  # 好きなHugoバージョンに変更可
          extended: true           # SCSS/SASSをビルドするテーマの場合はtrueにしないとエラーになる
          
      - name: Build Hugo site
        run: hugo --minify

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v4
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./public
          publish_branch: gh-pages
```

GitHubリポジトリのActionsタブを見ると成否が伺えます。
![](../assets/Pasted%20image%2020250822001228.png)

ここまでで、`shindys-note`の環境は整いました。あとはObsidianのVault内の更新があれば`shindys-note`へ同期を行う仕組みを構築すれば、GitHub Pagesへの公開設定を実施して完了です。

### 3. Vault内対象フォルダの内容を`master`へ同期する
プライベートリポジトリで管理しているObsidianのVaultの技術系ドキュメントに関する資材に変更があった場合に、Vault内対象フォルダの「docs」や「assets」で`shindys-note`の`master`ブランチの「content」や「assets」を置換する仕組みを構築します。

#### 3.1 Personal Access Token (PAT)の作成
リポジトリ間の操作になりますので、以下の手順でリポジトリ操作権限を持ったPATを作成します。
- GitHub から `Settings > Developer settings > Personal access tokens > Tokens (classic)`
- scope: `repo` にチェックを入れる
- トークンをコピーする
#### 3.2 PATをVaultリポジトリに設定
- Vaultリポジトリ → `Settings > Secrets and variables > Actions > New repository secret`
- 名前：`NOTE_REPO_TOKEN`
- 値：上でコピーしたPAT

#### 3.3 Vaultリポジトリ内にGitHub Actions用のスクリプトを作成
以下の内容を記述した`.github/workflows/sync-to-note.yml`を作成し、pushしてください。
pushすると、Actionsが動作し、`shindys-note`へ同期が行われます。
```yml
name: Sync Vault to shindys-note

on:
  push:
    branches:
      - master   # Vaultのメインブランチに合わせる
    paths:
      - "docs/**"
      - "assets/**"

jobs:
  sync:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Vault repo
        uses: actions/checkout@v3

      - name: Checkout shindys-note repo
        uses: actions/checkout@v3
        with:
          repository: shindy-dev/shindys-note
          path: shindys-note
          token: ${{ secrets.NOTE_REPO_TOKEN }}

      - name: Sync folders
        run: |
          rsync -av --delete docs/ shindys-note/content/
          rsync -av --delete assets/ shindys-note/static/assets/

      - name: Commit and push changes
        run: |
          cd shindys-note
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add .
          git commit -m "Sync from Vault: $(date '+%Y-%m-%d %H:%M:%S')" || echo "No changes to commit"
          git push origin master   # Vaultのメインブランチに合わせる
```

### 4. `gh-pages`ブランチをGitHub Pagesで公開する
最後に構築した公開用環境をGitHub Pagesに公開する設定を行います。
1. GitHubリポジトリのSettingsタブのPagesを選択
![](../assets/Pasted%20image%2020250822010141.png)
2. Build and deploymentのSourceに「Deploy from a branch」を選択
3. Branchには`gh-pages`、`/(root)`を設定
![](../assets/Pasted%20image%2020250822010523.png)

ローカル実行したときと同じ内容が表示されれば、公開完了です🎵