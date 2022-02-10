# DiscordMusicBot


Project: `https://www.figma.com/file/kkUqe75Yc6wUSNeYR2hOtL/DiscordMusicBotRelease`

Start lavalink:
```
docker build -f dockers/LavalinkDockerfile -t lev145/lavalink .
docker run --name lavalink -d --rm -p 2333:2333 lev145/lavalink
```
