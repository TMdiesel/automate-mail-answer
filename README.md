# 体調確認メール回答自動化ツール

## ツールについて

体調確認メールへの回答を自動化するツールである。

### 回答手順

回答の手順は以下のとおりである。

1. IMAP を使って、Gmail に届いた体調確認メールに書かれた URL を取得する。
1. Selenium で GoogleChrome を自動操作する。
1. 回答結果のスクリーンショットを`img`ディレクトリに保存する。  
   `logger.log`を`log`ディレクトリに出力する。

### 備考

- 回答は朝 6:30 に自動で行われる。
- 回答内容は以下のようになっているので、それ以外の場合(体調不良、年次休暇、出社など)は手動で入力する必要がある。

  ```text
  1. いいえ
  2. いいえ
  3. 営業日：テレワーク
     休日：休み
  4. オフィス在籍
  5. 自宅(テレワーク)
  ```

- 祝日判定は[jpholiday](https://pypi.org/project/jpholiday/)を使っているので必ずしも会社の休日と一致するとは限らない。

## 使い方

1. Gmail で IMAP 機能を有効にする。([Gmail ヘルプ](https://support.google.com/mail/answer/7126229?hl=ja)参照)

1. [Google ログインページ](https://myaccount.google.com/u/1/?tab=kk)から
   2 段階認証プロセスを有効にして、アプリパスワードを発行する。

1. [ChromeDriver](http://chromedriver.chromium.org/downloads)
   から、GoogleChrome のバージョンに合った
   `chromedriver.exe`をダウンロードして、`driver`ディレクトリに格納する。

1. `sample.env`をコピーして、`.env`に名前変更する。作成した`.env`内で環境変数を指定する。

## 参考

- [IMAP 公式ドキュメント](https://docs.python.org/ja/3/library/imaplib.html)
- [Selenium 公式ドキュメント](https://kurozumi.github.io/selenium-python/locating-elements.html)
