# docker recreate tools

This is a small tool to print re-create existance docker container run commands.

# Install

```bash
# through pip
pip install docker-recreate


# using curl
curl https://raw.githubusercontent.com/jeffrey4l/docker-recreate/master/main.py \
    -o /usr/local/bin/docker-recreate
chmod +x /usr/local/bin/docker-recreate


# for China
curl https://raw.fastgit.org/jeffrey4l/docker-recreate/master/main.py \
    -o /usr/local/bin/docker-recreate
chmod + /usr/local/bin/docker-recreate
```

# Usage

```console
$ docker-recreate -h
usage: docker-recreate [-h] [--format {csv,json,oneline,string,yaml}] container [container ...]

positional arguments:
  container

optional arguments:
  -h, --help            show this help message and exit
  --format {csv,json,oneline,string,yaml}, -f {csv,json,oneline,string,yaml}
```

```console
$ docker-create grafana
docker \
    run \
    -d \
    --name grafana \
    --network host \
    --restart always \
    -v grafana:/var/lib/grafana:rw \
    grafana/grafana:8.0.3
```
