# RoomSystemBotClient
Firebase Realtime Database上の変更を検知し、スピーカから音を鳴らします。

[aoirint/room-system-firebase](https://github.com/aoirint/room-system-firebase)と同時に使うことを想定しています。
room-system-firebaseは、Microsoft TeamsからのOutgoing Webhookを受け取り、このソフトウェアに対応した形でRealtime Databaseに保存します。
このソフトウェアは、この変更を検知し、スピーカを鳴らしたあと、当該メッセージをRealtime Database上から削除します。


## 想定環境
- Raspberry Pi 4B
  - オーディオジャック→アンプ→スピーカ


## 機能
### 通知音
botにメッセージが送信されたとき、通知音を鳴らします。

### 個人サウンド
botにメッセージを送った人固有の通知音（個人サウンド）を再生することができます。
共通の通知音だけでは誰がメッセージを送ったかわかりませんが、
個人サウンドに対応する人を知っていれば誰が送ったか判断することができます。

### 受信メッセージ読み上げ
OpenJTalkを使ったbot宛てメッセージ読み上げに対応しています。
botに送られたメッセージをそのまま読み上げます。

### 定型メッセージ読み上げ（音声合成）
OpenJTalkを使った定型メッセージ読み上げに対応しています。
あらかじめ設定した定型文をそのまま読み上げます。

bot（Outgoing Webhook）に対するメンションを送るだけで
定型メッセージを読み上げさせることができるため、
素早いコミュニケーションができます。


## 設定
`./docker-compose.yml`で一部の設定をしていますが、
不足している環境変数があります。
これは`./.env`ファイルを作成して設定します。
`./template.env`を`./.env`にコピーして編集してください。

`HTTP_PROXY`、`HTTPS_PROXY`は、プロキシ設定が必要な場合の設定です。
不要ならば削除してください（非プロキシ環境での動作確認はしてないです）。

`FIREBASE_DATABASE_URL`は、Firebase Realtime DatabaseのURLです。
データベースのデータ閲覧ページから確認できると思います。
`*.firebaseio.com`の形式のはずです。

`OPENJTALK_HTSVOICE_PATH`は、音声合成に使うHTS Voiceファイルのパスです。
Dockerコンテナ内のパスなので注意してください。マウントは`docker-compose.yml`内で設定しています。

`SPEECH_ENABLED`、`PERSON_SOUND_ENABLED`、`STATIC_SPEECH_ENABLED`は各機能の有効化/無効化を切り替えます。
`0`で無効化、`1`で有効化です。

`STATIC_SPEECH_TEXT`は定型メッセージ読み上げに使う定型文です。


### 通知音
通知音は「開始」と「終了」の2種類必要です。
「開始」は下の各機能を実行する前に、
「終了」は下の各機能を実行した後に再生します。

それぞれ、`./sounds/opening.mp3`、`./sounds/closing.mp3`に配置してください。
再生中に処理はブロックするので、できるだけ短い音声が好ましいです。

想定としては、OtoLogicさんの`チャイム　アナウンス03`で、
順再生を`opening.mp3`、逆再生を`closing.mp3`にします。
逆再生はAudacityなどで作成してください。

- [フリー効果音：アナウンス音｜OtoLogic](https://otologic.jp/free/se/announce01.html)

### 個人サウンド
この機能を使用するには、事前に送信者のTeamsアカウントの`aadObjectId`（UUID形式の固有ID）を知っている必要があります。
`aadObjectId`は、`docker-compose logs -f`でログを参照して見つけるか、Teamsをブラウザで開いてDeveloper Toolsを使って調べる方法があります。

ブラウザで開いたTeamsにおいて、
一部の要素の`data-tid`属性にこの`aadObjectId`が含まれています。
右上に表示されている自分のアイコンのうち、オンライン状態を示す部分では、`presence-8:orgid:{aadObjectId}`の形式で読み取れます。
また、投稿のアイコン画像部分の`profile-picture`要素では、`personCardTrigger-8:orgid:{aadObjectId}`の形式で読み取れます。

個人サウンドは、`./sounds/person/{aadObjectId}.mp3`に配置します。`{}`は不要です。
当該ファイルが存在しなかった場合、再生をスキップします（スキップした旨をログに残します）。

この機能は、環境変数`PERSON_SOUND_ENABLED`を`0`で無効化、`1`で有効化します。


### 受信メッセージ読み上げ（音声合成）
合成音声のモデルとしてHTS Voiceファイルをダウンロードしてくる必要があります。

- [MMDAgent - Browse /MMDAgent_Example at SourceForge.net](https://sourceforge.net/projects/mmdagent/files/MMDAgent_Example/)

上記リンクからダウンロードできる`mei_normal.htsvoice`の使用を想定しています。
`./voices/mei_normal.htsvoice`に配置してください。

この機能は、環境変数`SPEECH_ENABLED`を`0`で無効化、`1`で有効化します。


### 定型メッセージ読み上げ（音声合成）
OpenJTalkを使った定型メッセージ読み上げに対応しています。
受信メッセージ読み上げと同様、HTS Voiceファイルを配置してください（同じファイルを使用します）。

この機能は、環境変数`STATIC_SPEECH_ENABLED`を`0`で無効化、`1`で有効化します。
