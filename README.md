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
chmod +x /usr/local/bin/docker-recreate
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

```console
$ docker-recreate ceph_osd_2
docker \
    run \
    -d \
    --name ceph_osd_2 \
    --network host \
    --restart unless-stopped \
    --pid host \
    --privileged \
    -e OSD_STORETYPE=filestore \
    -e OSD_BS_FSUUID=e76f38d0-3f34-4771-b099-d26ee063ae01 \
    -e OSD_ID=2 \
    -e KOLLA_CONFIG_STRATEGY=COPY_ALWAYS \
    -e JOURNAL_PARTITION=/dev/disk/by-partuuid/9967b401-ff2b-4ed4-ac15-028e89238bdf \
    -e TCMALLOC_MAX_TOTAL_THREAD_CACHE_BYTES=134217728 \
    -e KOLLA_SERVICE_NAME=ceph-osd-2 \
    -v kolla_logs:/var/log/kolla/:rw \
    -v /etc/localtime:/etc/localtime:ro \
    -v /etc/kolla/ceph-osd/:/var/lib/kolla/config_files/:ro \
    -v /dev/:/dev/:rw \
    -v /var/lib/ceph/osd/e76f38d0-3f34-4771-b099-d26ee063ae01:/var/lib/ceph/osd/ceph-2:rw \
    172.20.140.229:4000/kolla/centos-source-ceph-osd:train
```
