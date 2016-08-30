import re

from distlib.version import NormalizedMatcher


class GenFromPat(object):
    PATTERN = re.compile(r'^$')

    @classmethod
    def from_str(cls, s):
        m = cls.PATTERN.search(s)
        if m is not None:
            return cls(**m.groupdict())
        else:
            raise ValueError("Could not parse {} as valid {}".format(s, cls.__name__))


class BasicRepoContainer(object):
    def __init__(self):
        self._cont = {}

    def add(self, repo):
        repo = NormalizedMatcher(repo)
        if repo.name not in self._cont:
            self._cont[repo.name] = repo
        else:
            if repo > self._cont[repo.name]:
                self._cont[repo.name] = repo

    def __str__(self):
        return '\n'.join(str(x) for x in self._cont.values())


class SSHRepo(GenFromPat):
    PATTERN = re.compile(
        r'(?P<repo>ssh://(?P<vcs>hg|git)@.+?/(?P<owner>[\w\d_-]+)/(?P<name>[\w\d_-]+))(?:@(?P<version>.+?))?(?:@|#|$)')

    def __init__(self, repo, vcs, owner, name, version):
        self.repo = repo
        self.vcs = vcs
        self.version = version
        self.owner = owner
        self.name = name

    def __eq__(self, other):
        return self.repo == other.repo

    def __hash__(self):
        return self.repo.__hash__()

    def to_tuple(self):
        return self.repo, self.vcs, self.owner, self.name, self.version
