# openfga-practice
Let's learn openfga

## fgaコマンドの叩き方
参考
https://github.com/openfga/cli

```sh
docker pull openfga/cli; docker run -it openfga/cli
```

```sh
# --rmオプションをつけてコンテナが増えないようにする
 docker run -it --rm openfga/cli --version
```

- model.fga を model.json に変換
```sh
docker run --env NO_COLOR=yes -it --rm openfga/cli model transform "$(cat model.fga)" > model.json
```