import yaml, re, os, sys

from string import Template


def path_constructor(loader, node):
    try:
        return Template(node.value).substitute(os.environ)
    except KeyError as e:
        print("Environment variable {} not defined".format(str(e)))
        sys.exit(1)


class EnvVarLoader(yaml.SafeLoader):
    pass


class Config:

    config = None
    __PATH_MATCHER = re.compile(r'.*\$\{([^}^{]+)\}.*')

    def __init__(self):
        EnvVarLoader.add_implicit_resolver('!path', self.__PATH_MATCHER, None)
        EnvVarLoader.add_constructor('!path', path_constructor)

        with open(r'./config.yaml') as file:
            self.config = yaml.load(file, Loader=EnvVarLoader)



