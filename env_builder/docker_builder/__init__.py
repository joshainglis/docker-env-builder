import json
from os import getenv
from os.path import join, expanduser, split

# noinspection PyPackageRequirements
import docker
# noinspection PyPackageRequirements
from docker.tls import TLSConfig

from env_builder.utils import get_curdir

DOCKER_MACHINE = getenv('DOCKER_MACHINE', 'default')
DOCKER_MACHINE_JSON = join(expanduser('~'), '.docker', 'machine', 'machines', DOCKER_MACHINE, 'config.json')


def get_docker_client(docker_machine_config=DOCKER_MACHINE_JSON):
    with open(docker_machine_config, 'r') as f:
        config = json.load(f)

    tls_config = TLSConfig(
        client_cert=(
            config['HostOptions']['AuthOptions']['ClientCertPath'],
            config['HostOptions']['AuthOptions']['ClientKeyPath']
        ),
        ca_cert=config['HostOptions']['AuthOptions']['CaCertPath'],
        verify=True
    )
    return docker.Client(base_url='tcp://{}:2376'.format(config['Driver']['IPAddress'], ), tls=tls_config)


def build_docker_image(client, tag=None):
    if tag is None:
        tag = 'biarrioptimisation/{}_env:latest'.format(split(get_curdir())[-1])
    for line in client.build(
            path=get_curdir(),
            tag=tag,
            rm=True,
            nocache=True,
            stream=True,
            pull=True,
            decode=True
    ):
        print(line)
