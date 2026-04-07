# trajectory-random-nicegui

<img height="256" src="https://github.com/user-attachments/assets/8796a654-1735-4c09-b085-7186860a4c55" />

- PythonのWebフレームワーク `NiceGUI` でランダムな軌跡を `leaflet` 地図に描画

- Docker compose 使用

- アプリソースは `main.py` のみ、これ一つでWebサーバとフロントエンドを実装

- NiceGUI の Leaflet 利用のテストを兼ねた[（ ↗ 公式ドキュメント）](https://nicegui.io/documentation/leaflet)

  - 全面表示、カスタムボタン設置、地物オーバレイ、地物のある範囲に自動ズームができた

  - `Map` , `Polyline` の二つのクラスを作成

  - 既存の軌跡データをサクッと表示する土台にもなる

<br>

### 主要動作

- Dockerコンテナ起動後 `http://localhost:8888` に衛星地図とランダムな軌跡が表示される

- 軌跡は一定の経緯度範囲で作成したランダムな点を繋げたもの

- 軌跡の描画時、その範囲に地図が自動ズーム・移動する

- 地図上に以下のボタンあり

  - 背景地図の切り替え（衛星写真 ↔ 通常地図、ともにタイルは国土地理院）

  - 新しいランダムな軌跡の生成

  - 点の位置はそのままで軌跡の繋げ方を変更

  - 軌跡の経緯度情報表示

    <img height="192" src="https://github.com/user-attachments/assets/54770e66-2fcf-44fc-bf68-c2c55a5c967f" />
    　<img height="192" src="https://github.com/user-attachments/assets/84bb31a5-0710-4855-b04b-ab24de75d991" />
    　<img height="192" src="https://github.com/user-attachments/assets/aff4d273-3428-4539-b9c2-7cd3c6a0e867" />
    　<img height="192" src="https://github.com/user-attachments/assets/d8f8b78c-27c5-41f4-ae6b-967ea1bbb7ea" />

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

- Chrome 146.0

- Firefox 149.0

<br>

### 補足：軌跡の繋げ方について

- ランダムな点を生成した順に繋げると、あちこちに飛んでまともな軌跡にならない

- 自然な軌跡を作れるライブラリは何らかあると思うが今回は拘らず、ランダムに始点を決めて次々に最近傍点を繋いだ

- 点が増えると交差が増え不自然な軌跡になる。交差の低減だけでもそのうちやりたい

<br>

---
