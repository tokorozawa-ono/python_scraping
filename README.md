# python_scraping

## コンテナ起動
```commandline
docker-compose up -d
```

## コンテナへのログイン
```commandline
docker exec -it python3 /bin/bash
```

#### pingのインストール
```commandline
apt-get update
apt-get install iputils-ping net-tools
```

## VNCでアクセス

for mac
```commandline
open vnc://127.0.0.1:5900
```

for windows

https://uvnc.com/downloads/ultravnc.html
```commandline
localhost:5900
```

passwordは初期値はsecret

## selenium管理画面

```commandline
http://localhost:4444
```

