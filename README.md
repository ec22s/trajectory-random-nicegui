# trajectory-random-nicegui

- PythonのWebフレームワーク `NiceGUI` でランダムな軌跡を `leaflet` 地図に描画

- Docker compose 使用

- アプリソースは `main.py` のみ、これ一つでWebサーバとフロントエンドを実装

- NiceGUI の Leaflet 利用のテストを兼ねた[（ ↗ 公式ドキュメント）](https://nicegui.io/documentation/leaflet)

  - 全面表示、カスタムボタン設置、地物オーバレイ、地物のある範囲に自動ズームができた

  - `Map` , `Polyline` の二つのクラスを作成

  - 軌跡の実データをサクッと表示する土台になる

<br>

### 主要動作

- Dockerコンテナ起動後 `http://localhost:8888` に衛星地図とランダムな軌跡が表示される

- 軌跡は一定の経緯度範囲で作成したランダムな点を繋げたもの

- 軌跡の範囲に地図が連動して移動・ズームする

- 地図上に以下のボタンあり

  - 背景地図の切り替え（衛星写真 ↔ 通常地図、ともにタイルは国土地理院）

  - 新しいランダムな軌跡の生成

  - 点の位置はそのままで軌跡の繋げ方を変更

  - 軌跡の経緯度情報表示

<br>

### 使い方

- コンテナ起動

  ```shell
  make dev
  ```

- コンテナ終了

  ```shell
  make down
  ```

- ランダムな点の生成数と範囲はソースコードにあり

  ```python
  POINTS_RANGE = [16, 64]
  LAT_RANGE = [33.2, 33.3]
  LON_RANGE = [130.1, 130.2]
  ```

  - TODO: 地図上での変更UIを追加したい

<br>

### 動作確認環境

- GNU bash, version 5.3.9(1)-release (x86_64-apple-darwin23.6.0)

- GNU Make 3.81

- Docker version 29.3.1, build c2be9ccfc3

- Docker Compose version v5.1.0

<br>

### 補足：軌跡の繋げ方について

- ランダムな点を生成した順に繋げると、あちこちに飛んでまともな軌跡にならない

- 自然な軌跡を作れるライブラリは何らかあると思うが今回は拘らず、ランダムに始点を決めて次々に最近傍点を繋いだ

- 点が増えると交差が増え不自然な軌跡になる。交差の低減だけでもそのうちやりたい

<br>

---
