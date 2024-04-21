# AI-Elderly-Emergency-Alert-System  


**![](https://lh7-us.googleusercontent.com/Dtkq6wnDS8QQn93AcJd_wP4oDmzrfZfXeLC_-vwLTux5sFtIHBjO5F8Bh1dJHjjfqTx0EH8ph4T3ezxOpiUFoYFp0ke1NlF7gypYD5zttpEnXMx_KzK41EYewPRahTaAlnkMIwdI4SrotIF0Hbkb8bs)**

### システム名　mimamoru ai(みまもるあい)

ひとり暮らしの高齢者向け見守りカメラシステム

高齢者が倒れたことをAIが検知し、あらかじめ登録しているメールアドレスに通知(写真)を送信

*※このプロジェクトは進行中です*

## DEMO

追加予定





# 1. プログラムの概要

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)[![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org/)[![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)[![Keras](https://img.shields.io/badge/Keras-D00000?style=for-the-badge&logo=keras&logoColor=white)](https://keras.io/)[![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)](https://www.tensorflow.org/)[![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)](https://numpy.org/)[![PIL](https://img.shields.io/badge/PIL-512BD4?style=for-the-badge&logo=pillow&logoColor=white)](https://pillow.readthedocs.io/en/stable/)[![asyncio](https://img.shields.io/badge/asyncio-00C49F?style=for-the-badge&logo=python&logoColor=white)](https://docs.python.org/3/library/asyncio.html)[![SMTP](https://img.shields.io/badge/SMTP-0072C6?style=for-the-badge&logo=mail.ru&logoColor=white)](https://en.wikipedia.org/wiki/Simple_Mail_Transfer_Protocol)[![Gmail](https://img.shields.io/badge/Gmail-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](https://www.gmail.com/)

AI画像認識による見守りカメラ
ひとり暮らしの高齢者が倒れたことを検知してメールアドレスに通知が行く。

i. 画像背景‘白化’のための準備プログラム

ii.WEB公開プログラム

iii.緊急時のメールアドレス設定

ⅳ.写真撮影プログラム

ⅴ.背景‘白化’プログラム

ⅵ.AIによる異常検知プログラム

ⅶ.判定結果送信プログラム


# 2. 使用方法
1,コード上のファイルパスを正しく入力

2,送信元のgmailを設定

　(設定後コードにアドレスとアプリパスワードを入力)

　※詳しい設定方法は[アプリ パスワードでログインする - Gmail ヘルプ (google.com)](https://support.google.com/mail/answer/185833?hl=ja)を確認

3,プログラムを実行する(execution code.py)

4,表示されたURLにアクセス

5,ウェブぺージにメールアドレスを入力

# 3. 必要ライブラリのインストール
動作確認　python3.11

必要ライブラリ

opencv-python

Flask

keras

numpy

Pillow

tensorflow

```
pip install opencv-python Flask keras numpy Pillow tensorflow

```
※OSによって異なる場合がある

# 4. セキュリティに関する注意事項

このプロジェクトはセキュリティの検証が行われていません。
