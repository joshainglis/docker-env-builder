import click

from env_builder.docker_builder import build_docker_image, get_docker_client
from env_builder.utils import get_dependencies


@click.command()
@click.option('--requirements', default=None,
              type=click.Path(exists=True, file_okay=True, dir_okay=False, resolve_path=True))
@click.option('--working-dir', default=None,
              type=click.Path(exists=True, file_okay=True, dir_okay=False, resolve_path=True))
@click.option('--dependency-dir', default=None,
              type=click.Path(exists=True, file_okay=True, dir_okay=False, resolve_path=True))
@click.option('--build-image/--no-build-image', default=False)
def build_env(requirements, working_dir, dependency_dir, build_image):
    get_dependencies(requirements=requirements, working_dir=working_dir, dependency_dir=dependency_dir)
    if build_image:
        build_docker_image(get_docker_client())
