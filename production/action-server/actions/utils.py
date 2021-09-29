from ruamel import yaml

# Loads config from config.yml file
def load_conf():
    CONFIG_FILE_ADR = './config.yml'
    with open(CONFIG_FILE_ADR, 'r') as f:
        conf = yaml.load(f, Loader=yaml.RoundTripLoader)
    return conf