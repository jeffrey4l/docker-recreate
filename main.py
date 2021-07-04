#!/usr/bin/env python

import argparse
import json
import subprocess

try:
    import yaml
    has_yaml = True
except ImportError:
    has_yaml = False


def get_inspect_json(resource):
    output = subprocess.check_output(['docker', 'inspect', resource])
    return json.loads(output)


def get_container(name):
    return get_inspect_json(name)[0]


def get_image(name):
    return get_inspect_json(name)[0]


class BaseFormatter(object):
    def __init__(self, cmds):
        self.cmds = cmds

    def format(self):
        return

    @classmethod
    def name(cls):
        class_name = cls.__name__
        return class_name[:-len('Formatter')].lower()


class CSVFormatter(BaseFormatter):
    def format(self):
        return ','.join(self.cmds)


class JsonFormatter(BaseFormatter):
    def format(self):
        return json.dumps(self.cmds, indent=4)


class OneLineFormatter(BaseFormatter):
    def format(self):
        return ' '.join(self.cmds)


class StringFormatter(BaseFormatter):
    def format(self):
        line = []
        is_param = False
        for idx, cmd in enumerate(self.cmds):
            if is_param and not cmd.startswith('-'):
                line.append(cmd)
            else:
                if idx != 0:
                    line.append('\\\n')
                    line.append(' ' * 2)
                line.append(cmd)

            is_param = cmd.startswith('-')
        return ' '.join(line)


class YamlFormatter(BaseFormatter):

    def format(self):
        if not has_yaml:
            raise ValueError('Need YAML module for yaml formatter')
        return yaml.dump(self.cmds)


class Container:

    def __init__(self, container, image=None):
        self.container = container
        self._config = container['Config']
        self._host_config = container['HostConfig']
        self.image = image
        self._image_config = image['Config']
        self._image_host_config = image['ContainerConfig']

    def get_container_name(self):
        name = self.container['Name']
        if name and name[0]:
            name = name[1:]
        return name

    def get_cmds(self):
        cmds = ['docker', 'run']
        if self._config['AttachStdin']:
            cmds.append('-i')
        if self._config['AttachStdout'] or self._config['AttachStderr']:
            cmds.append('-t')
        else:
            cmds.append('-d')
        if self._host_config['AutoRemove']:
            cmds.append('--rm')
        cmds.extend(['--name', self.get_container_name()])

        if self._config['Entrypoint'] != self._image_config['Entrypoint']:
            cmds.extend(['--entrypoint', self._config['Entrypoint']])
        if self._config['User'] != self._image_config['User']:
            cmds.extend(['--user', self._config['User']])

        # network mode
        network_mode = self._host_config['NetworkMode']
        if network_mode != 'default':
            cmds.extend(['--network', network_mode])

        port_bindings = self._host_config['PortBindings'] or {}
        # port mapping
        for target, source in port_bindings.items():
            host_port = source[0]['HostPort']
            target_port, protocol = target.split('/', 1)
            if protocol == 'tcp':
                target = target_port
            cmds.extend(['--publish', "%s:%s" % (host_port, target)])

        # restart policy
        cmds.extend(['--restart', self._host_config['RestartPolicy']['Name']])

        if self._host_config['IpcMode'] != 'private':
            cmds.extend(['--ipc', self._host_config['IpcMode']])
        if self._host_config['PidMode']:
            cmds.extend(['--pid', self._host_config['PidMode']])
        if self._host_config['Privileged']:
            cmds.append('--privileged')

        # environment
        container_envs = self._config['Env'] or {}
        image_envs = self._image_config['Env'] or {}

        for env in set(container_envs) - set(image_envs):
            cmds.extend(['-e', env])

        for bind in self._host_config['Binds'] or []:
            cmds.extend(['-v', bind])

        image_name = self._config['Image']
        cmds.append(image_name)
        if self._config['Cmd'] != self._image_config['Cmd']:
            cmds.extend(self._config['Cmd'])
        return cmds


def get_formatters():
    formatters = {}

    for clazz in BaseFormatter.__subclasses__():
        formatters[clazz.name()] = clazz
    return formatters


def check_container(value):
    output = subprocess.check_output(
        ['docker', 'ps', '-q', '--filter',
         'name=%s' % value, '--format', '{{.Names}}'])
    if not output:
        raise argparse.ArgumentTypeError(
                'Can not found container name "%s"' % value)
    containers = output.decode('utf8').split()
    if len(containers) > 1:
        msg = 'Found multi container for name "%s": %s' % (value, containers)
        raise argparse.ArgumentTypeError(msg)
    container_name = containers[0]
    return container_name


def main():
    formatters = get_formatters()
    parser = argparse.ArgumentParser()
    parser.add_argument('container', nargs='+', type=check_container)
    parser.add_argument(
            '--format',
            '-f',
            choices=formatters.keys(),
            default='string',
            help='Output format')

    conf = parser.parse_args()

    for container_name in conf.container:
        container = get_container(container_name)
        image_name = container['Config']['Image']
        image = get_image(image_name)
        container_obj = Container(container, image)
        print(formatters[conf.format](container_obj.get_cmds()).format())


if __name__ == "__main__":
    main()
