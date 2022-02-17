# DiscordMusicBot


Project: `https://www.figma.com/file/kkUqe75Yc6wUSNeYR2hOtL/DiscordMusicBotRelease`

Start bot:
```
poetry run music_bot
```

Start bot in docker:
```
docker build -f dockers/MainDockerfile -t lev145/music_bot .
docker run --name music_bot -d --rm lev145/music_bot
```

Start lavalink:
```
docker build -f dockers/LavalinkDockerfile -t lev145/lavalink .
docker run --name lavalink -d --rm -p 2333:2333 lev145/lavalink
```
