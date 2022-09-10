<div id="top"></div>

## 使用技術一覧

<!-- シールド一覧 -->
<!-- 該当するプロジェクトの中から任意のものを選ぶ-->
<p style="display: inline">
  <!-- バックエンドのフレームワーク一覧 -->
  <img src="https://img.shields.io/badge/-Django-092E20.svg?logo=django&style=for-the-badge">
  <!-- バックエンドの言語一覧 -->
  <img src="https://img.shields.io/badge/-Python-F2C63C.svg?logo=python&style=for-the-badge">
  <!-- ミドルウェア一覧 -->
  <img src="https://img.shields.io/badge/-Nginx-269539.svg?logo=nginx&style=for-the-badge">
  <img src="https://img.shields.io/badge/-MySQL-4479A1.svg?logo=mysql&style=for-the-badge&logoColor=white">
  <img src="https://img.shields.io/badge/-Gunicorn-199848.svg?logo=gunicorn&style=for-the-badge&logoColor=white">
  <!-- インフラ一覧 -->
  <img src="https://img.shields.io/badge/-Docker-1488C6.svg?logo=docker&style=for-the-badge">
</p>

## 目次

1. プロジェクトについて
2. 環境
3. ディレクトリ構成
4. ER 図
5. 開発環境構築

<!-- READMEの作成方法のesaのリンク -->
<br />
<div align="right">
    <a href="https://pj100.esa.io/posts/4190"><strong>READMEの作成方法 »</strong></a>
</div>
<br />
<!-- Dockerfileのesaのリンク -->
<div align="right">
    <a href="Dockerfileの詳細リンク"><strong>Dockerfileの詳細 »</strong></a>
</div>
<br />
<!-- プロジェクト名を記載 -->

## プロジェクト名

<!-- プロジェクトについて -->

### プロジェクトについて

<!-- プロジェクトの概要を記載 -->

  <p align="left">
    <br />
    <!-- プロジェクト詳細にBacklogのWikiのリンク -->
    <a href="Backlogのwikiリンク"><strong>プロジェクト詳細 »</strong></a>
    <br />
    <br />

<p align="right">(<a href="#top">トップへ</a>)</p>

## 環境

<!-- 言語、フレームワーク、ミドルウェア、インフラの一覧とバージョンを記載 -->

<p align="right">(<a href="#top">トップへ</a>)</p>

## ディレクトリ構成

<!-- Treeコマンドを使ってディレクトリ構成を記載 -->

<p align="right">(<a href="#top">トップへ</a>)</p>

## ER 図

<!-- draw.ioのリンクを記載 -->

<p align="right">(<a href="#top">トップへ</a>)</p>

## 開発環境構築

<!-- コンテナの作成方法、パッケージのインストール方法など、開発環境構築に必要な情報を記載 -->

1. .env ファイルの配置

   <ユーザ名>から.env ファイルをもらい、.env ファイルをルートディレクトリ直下に配置

2. プロジェクトの作成

docker-compose run

3. コンテナの起動

docker-compose up -d

4. コンテナの停止

docker-compose down

5. 動作確認

http://127.0.0.1:8000 にアクセスできるか確認
アクセスできたら成功

6. 本番環境構築

開発環境構築と同様に docker-compose.prod.yml ファイルを使って構築<br>
http://127.0.0.1:80 にアクセスできたら成功

<p align="right">(<a href="#top">トップへ</a>)</p>
