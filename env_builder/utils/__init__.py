import subprocess
from os import chdir, mkdir
from os.path import join, exists, realpath, curdir, abspath

from env_builder.managers import SSHRepo, BasicRepoContainer


def get_curdir():
    return realpath(curdir)


def make_dep_dir(project_directory):
    dependency_dir = join(project_directory, "dependencies")
    if not exists(dependency_dir):
        mkdir(dependency_dir)
    return dependency_dir


def get_reqs(f, base, ssh):
    for line in f:
        line = line.strip().replace(' ', '')
        if line:
            try:
                ssh.add(SSHRepo.from_str(line))
            except ValueError:
                if line and not line.startswith("#") and not line.startswith("-e"):
                    base.add(line)


def pull_ssh_repo(ssh_repo, dependency_directory, ssh_reqs, base_reqs, pulled):
    d = join(dependency_directory, ssh_repo.name)
    if exists(d):
        chdir(d)
        if ssh_repo.version:
            if subprocess.call([ssh_repo.vcs, 'checkout', ssh_repo.version]) != 0:
                subprocess.call([ssh_repo.vcs, 'pull'])
        else:
            subprocess.call([ssh_repo.vcs, 'pull'])
    else:
        chdir(dependency_directory)
        subprocess.call([ssh_repo.vcs, 'clone', ssh_repo.repo])
    if ssh_repo.version:
        chdir(d)
        subprocess.call([ssh_repo.vcs, 'checkout', ssh_repo.version])
    pulled.add(ssh_repo)
    try:
        with open(join(d, 'requirements.txt')) as f:
            get_reqs(f, base_reqs, ssh_reqs)
    except IOError:
        pass


def pull_in_ssh_dependencies(ssh_deps, ssh_reqs, base_reqs, pulled, working_directory, dependency_dir):
    try:
        for ssh_dep in ssh_deps:
            pull_ssh_repo(ssh_dep, dependency_dir, ssh_reqs, base_reqs, pulled)
        remaining = ssh_reqs - pulled
        if remaining:
            pull_in_ssh_dependencies(ssh_reqs - pulled, ssh_reqs, base_reqs, pulled, working_directory, dependency_dir)
    finally:
        chdir(working_directory)


def get_dependencies(requirements=None, working_dir=None, dependency_dir=None, ssh_reqs=None, base_reqs=None,
                     pulled=None):
    if ssh_reqs is None:
        ssh_reqs = set()
    if base_reqs is None:
        base_reqs = BasicRepoContainer()
    if pulled is None:
        pulled = set()
    if working_dir is None:
        working_dir = get_curdir()
    if dependency_dir is None:
        dependency_dir = make_dep_dir(working_dir)
    if requirements is None:
        requirements = abspath(join(working_dir, 'requirements.txt'))
    with open(requirements, 'r') as f:
        get_reqs(f, base_reqs, ssh_reqs)
    pull_in_ssh_dependencies(ssh_reqs, ssh_reqs, base_reqs, pulled, working_dir, dependency_dir)
    with open('external_requirements.txt', 'w') as f:
        f.writelines(str(base_reqs))
