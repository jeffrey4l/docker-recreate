import json
import unittest
import os

import main


CUR_DIR = os.path.dirname(os.path.abspath(__file__))


class MainTest(unittest.TestCase):

    def get_json_file(self, name):
        path = os.path.join(CUR_DIR, 'fixtures', name)
        with open(path, 'r') as f:
            return json.loads(f.read())

    def test_a(self):
        container_json = self.get_json_file('grafana-container.json')
        image_json = self.get_json_file('grafana-image.json')
        container = main.Container(container_json, image_json)
        cmds = container.get_cmds()
        expected = [
            'docker', 'run', '-d',
            '--name', 'grafana',
            '--network', 'host',
            '--restart', 'always',
            '-v', 'grafana:/var/lib/grafana:rw',
            'grafana/grafana:8.0.3']
        print(cmds)
        self.assertEqual(cmds, expected)
