# 体調確認メール回答自動化システム

## ツールについて

GitHub Actions を用いて体調確認メールへの回答を自動化します。

### 回答手順

回答の手順は以下の通りです。

1. IMAP を使って、Gmail に届いた体調確認メールに書かれた URL を取得する。
1. Selenium で GoogleChrome を自動操作する。

### 備考

- 回答は朝 6:30 に自動で行われます。
- 回答内容は以下のようになっているので、それ以外の場合(体調不良、年次休暇、出社など)は手動で入力する必要があります。

  ```text
  1. いいえ
  2. いいえ
  3. 営業日：テレワーク
     休日：休み
  4. オフィス在籍
  5. 自宅
  ```

- 祝日判定は[jpholiday](https://pypi.org/project/jpholiday/)を使っているので必ずしも会社の休日と一致するとは限りません。

## 使い方

1. 本リポジトリをフォークします。

1. GitHub Actions を有効化します。

1. Gmail で IMAP 機能を有効にします。([Gmail ヘルプ](https://support.google.com/mail/answer/7126229?hl=ja)参照)

1. [Google ログインページ](https://myaccount.google.com/u/1/?tab=kk)から
   2 段階認証プロセスを有効にして、アプリパスワードを発行します。

1. GitHub の Settings/Secrets から下記の変数を設定します。

   ```text
   USERNAME=Gmailアドレス
   PASSWORD=4で発行したパスワード
   COMPANYEMAIL=会社アドレス
   ```

## 参考

- [IMAP 公式ドキュメント](https://docs.python.org/ja/3/library/imaplib.html)
- [Selenium 公式ドキュメント](https://kurozumi.github.io/selenium-python/locating-elements.html)
