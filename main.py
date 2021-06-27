#!/usr/bin/env python

import argparse
import io
import json
import pprint
import subprocess
import sys


def get_inspect_json(resource):
    output = subprocess.check_output(['docker', 'inspect', resource])
    return json.loads(output)


def print_pretty_cmd2(cmds):
    max_length = 50
    line_cmds = []
    line_width = 0
    first_line = True
    total = len(cmds)
    for idx, cmd in enumerate(cmds):
        line_cmds.append(cmd)
        line_width += len(cmd)
        if line_width > max_length or idx == total - 1:
            if idx < total - 1:
                line_cmds.append('\\')
            if not first_line:
                sys.stdout.write('    ')
            print(' '.join(line_cmds))
            line_cmds = []
            line_width = 0
            first_line = False


def print_pretty_cmd3(cmds):
    line = []
    for idx, cmd in enumerate(cmds):
        if line and cmd.startswith('-'):
            line.append('\\\n')
            if idx != 0:
                line.append(' ' * 2)
        line.append(cmd)
    print(' '.join(line))


def format_csv(cmds):
    return ','.join(cmds)


def format_list(cmds):
    output = io.StringIO()
    pprint.pprint(cmds, stream=output)
    return output.getvalue()


def format_json(cmds):
    return json.dumps(cmds, indent=4)


def format_string(cmds):
    line = []
    is_param = False
    for idx, cmd in enumerate(cmds):
        if is_param and not cmd.startswith('-'):
            line.append(cmd)
        else:
            if idx != 0:
                line.append('\\\n')
                line.append(' ' * 2)
            line.append(cmd)

        is_param = cmd.startswith('-')
    return ' '.join(line)


def parse_container(container):
    inspect = get_inspect_json(container)
    data = inspect[0]

    image_name = data['Config']['Image']

    image = get_inspect_json(image_name)
    image = image[0]

    cmds = ['docker', 'run']
    config = data['Config']
    host_config = data['HostConfig']
    if config['AttachStdin']:
        cmds.append('-i')
    if config['AttachStdout'] or config['AttachStderr']:
        cmds.append('-t')
    else:
        cmds.append('-d')
    if host_config['AutoRemove']:
        cmds.append('--rm')
    container_name = data['Name']
    if container_name[0] == '/':
        container_name = container_name[1:]
    cmds.extend(['--name', container_name])
    if config['Entrypoint'] != image['Config']['Entrypoint']:
        cmds.extend(['--entrypoint', config['Entrypoint']])
    if config['User'] != image['Config']['User']:
        cmds.extend(['--user', config['User']])
    # network mode
    network_mode = host_config['NetworkMode']
    if network_mode != 'default':
        cmds.extend(['--network', network_mode])

    port_bindings = host_config['PortBindings'] or {}
    # port mapping
    for target, source in port_bindings.items():
        host_port = source[0]['HostPort']
        target_port, protocol = target.split('/', 1)
        if protocol == 'tcp':
            target = target_port
        cmds.extend(['--publish', "%s:%s" % (host_port, target)])

    # restart policy
    cmds.extend(['--restart', host_config['RestartPolicy']['Name']])

    if host_config['IpcMode'] != 'private':
        cmds.extend(['--ipc', host_config['IpcMode']])
    if host_config['PidMode']:
        cmds.extend(['--pid', host_config['PidMode']])
    if host_config['Privileged']:
        cmds.append('--privileged')

    # environment
    container_envs = config['Env'] or {}
    image_envs = image['Config']['Env'] or {}

    for env in set(container_envs) - set(image_envs):
        cmds.extend(['-e', env])

    for bind in host_config['Binds'] or []:
        cmds.extend(['-v', bind])

    image_name = data['Config']['Image']
    cmds.append(image_name)
    if config['Cmd'] != image['Config']['Cmd']:
        cmds.extend(config['Cmd'])
    return cmds


FORMATER = {
    'string': format_string,
    'list': format_list,
    'json': format_json,
    'csv': format_csv,
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('container', nargs='+')
    parser.add_argument('--format', '-f', choices=FORMATER.keys(), default='string')
    conf = parser.parse_args()
    for container in conf.container:
        cmds = parse_container(container)
        print(FORMATER[conf.format](cmds))


if __name__ == "__main__":
    main()
