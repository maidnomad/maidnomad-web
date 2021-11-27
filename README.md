# maidnomad-web

## 必要環境
- python==3.10.*

## 開発環境セットアップ

```console
% python3.10 -m venv venv
% . venv/bin/activate
(venv) $ make pip
```

次に、 `.env` ファイルを作成します。

```console
% cp .env.example .env
```

まずは、ユニットテストが動くことを確認すると良いでしょう。

```console
(venv) % make test
```

## migration

git pull した直後はDBが変更されているかもしれません。
以下のコマンドで migrate しましょう。

```console
(venv) % make migrate
```

## 開発サーバー起動

migtation が正常に行われていれば以下のコマンドでサーバーを起動できます。

```console
(venv) % make runserver
```

サーバーが起動したらブラウザで以下にアクセスできるはずです。

http://localhost:8000/

## formatter, linter and test

PRの前に必ず実施してください。

```console
(venv) % make fmt
(venv) % make lint
(venv) % make test
```

## ライブラリの追加

ライブラリを追加する時は以下の手順で行います。

なお、本番に必要なライブラリか、開発時のみに必要なライブラリかによって編集するファイルが変わります。

- 本番に必要なライブラリの場合:

  - `requirements.txt` を編集してください

- 開発時のみに必要なライブラリ（formatterなど）の場合:

  - `requiremnets_dev.txt` を編集してください

次のコマンドを実行してライブラリをインストールしてください。

```console
(venv) % make pip
```

次に、 `requirements.lock` を更新します。

```console
(venv) % pip freeze > requirements.lock
```

最後に、 `requirements.lock` の変更をSCMで比較し、意図しないライブラリーが入っていないことを確認してください。

### もし、ライブラリのインストールに失敗した場合

ライブラリのインストールに失敗し、仮想環境が壊れてしまった場合は次のコマンドで仮想環境の作成からやり直しましょう。

```console
(venv) % deactivate
% rm -r venv/
% python3.10 -m venv venv
% . venv/bin/activate
(venv) $ make pip
```

## デプロイ方法

`stg` ブランチにマージし、CIがOKの場合は、ステージングサイトにリリースされます。

https://staging.maid-cafe.work/

`main` にマージすると本番にリリースされます。

https://www.maid-cafe.work/

`main` への直接コミットは禁止されています。

必ず Pull Request を出してレビューを受けてからマージしてください。