import yaml


def apply_defaults(config):
    pull_up_down = config.get('gpio', {}).get('pull_up_down', 'PUD_DOWN')
    setmode = config.get('gpio', {}).get('setmode', 'BOARD')
    config['gpio'] = {
        "pull_up_down": pull_up_down,
        "setmode": setmode
    }
    return config


def get_config():
    with open(r'config.yaml') as file:
        config = yaml.full_load(file)
        config = apply_defaults(config)
        return config


CONFIG = get_config()
