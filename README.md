# RoomSystemBotClient
Firebase Realtime Database上の変更を検知し、スピーカから音を鳴らします。

## 想定環境
- Raspberry Pi 4B
  - オーディオジャック→アンプ→スピーカ

## 機能と設定
`./docker-compose.yml`で一部の設定をしていますが、
不足している環境変数があります。
これは`./.env`ファイルを作成して設定します。
`./template.env`を`./.env`にコピーして編集してください。

### 通知音
botにメッセージが送信されたとき、通知音を鳴らします。

通知音は「開始」と「終了」の2種類必要です。
「開始」は下の各機能を実行する前に、
「終了」は下の各機能を実行した後に再生します。

それぞれ、`./sounds/opening.mp3`、`./sounds/closing.mp3`に配置してください。
再生中に処理はブロックするので、できるだけ短い音声が好ましいです。

想定としては、OtoLogicさんの`チャイム　アナウンス03`で、
順再生を`opening.mp3`、逆再生を`closing.mp3`にします。

- [フリー効果音：アナウンス音｜OtoLogic](https://otologic.jp/free/se/announce01.html)

### 個人サウンド
botにメッセージを送った人固有の音声を再生することができます。

この機能を使用するには、事前に送信者のTeamsアカウントの`aadObjectId`（UUID形式の固有ID）を知っている必要があります。
`aadObjectId`は、`docker-compose logs -f`でログを参照して見つけるか、Teamsをブラウザで開いてDeveloper Toolsを使って調べる方法があります（TODO：詳細説明）。

個人サウンドは、`./sounds/person/*.mp3`に配置します。`*.mp3`の`*`は`aadObjectId`です。
当該ファイルが存在しなかった場合、再生をスキップします（スキップした旨をログに残します）。

この機能は、環境変数`PERSON_SOUND_ENABLED`を`0`で無効化、`1`で有効化します。


### 受信メッセージ読み上げ（音声合成）
OpenJTalkを使ったbot宛てメッセージ読み上げに対応しています。
合成音声のモデルとしてHTS Voiceファイルをダウンロードしてくる必要があります。

- [MMDAgent - Browse /MMDAgent_Example at SourceForge.net](https://sourceforge.net/projects/mmdagent/files/MMDAgent_Example/)

上記リンクからダウンロードできる`mei_normal.htsvoice`の使用を想定しています。
`./voices/mei_normal.htsvoice`に配置してください。

この機能は、環境変数`SPEECH_ENABLED`を`0`で無効化、`1`で有効化します。


### 定型メッセージ読み上げ（音声合成）
OpenJTalkを使った定型メッセージ読み上げに対応しています。
受信メッセージ読み上げと同様、HTS Voiceファイルを配置してください。

この機能は、環境変数`STATIC_SPEECH_ENABLED`を`0`で無効化、`1`で有効化します。
