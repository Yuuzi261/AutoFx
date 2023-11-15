<div align="center">

<img alt="LOGO" src="https://i.imgur.com/pD5bowS.png" width="300" height="300" />
  
# AutoFx

恢復 Discord 的 Twitter 嵌入功能

[**English**](./README.md) | [**繁體中文**](./README_zh.md)

</div>

## 📝簡介

一個自動修復Twitter連結嵌入的Discord機器人，使用FixTweet。

## ✨功能

![](https://raw.githubusercontent.com/Yuuzi261/AutoFx/main/demo.gif)

## 🔗邀請至Discord

👉 [點擊這裡邀請機器人到你的伺服器](https://discord.com/api/oauth2/authorize?client_id=1173685781265649745&permissions=292594658304&scope=bot)

## 🛠️自己建置一台

### 📥安裝

在運行機器人之前，你需要安裝必要的模組。

```shell
pip install -r requirements.txt
```

在某些作業系統中，你可能需要使用 `pip3` 而不是 `pip` 來進行安裝。

### ⚡使用

#### 1. 創建並配置.env文件

```env
TOKEN=YourDiscordBotToken
```

#### 2. 配置configs.yml文件

```yml
prefix: ''                          # 機器人命令的前綴。
activity_name: ''                   # 機器人顯示的活動名稱。
```

#### 3. 運行機器人並邀請至你的伺服器

```shell
python bot.py
```

在某些操作系統中，你可能需要使用 `python3` 而不是 `python`。

🔧機器人權限設定 `292594658304`

- [x] 管理 Webhooks
- [x] 讀取訊息
- [x] 發送訊息
- [x] 在討論串中傳送訊息
- [x] 管理訊息
- [x] 管理討論串

#### 4. 玩得開心

不必設定，直接開始使用！
