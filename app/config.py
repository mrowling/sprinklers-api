import yaml


def get_config():
    with open(r'config.yaml') as file:
        config = yaml.full_load(file)
        return config


CONFIG = get_config()
