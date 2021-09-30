from ruamel import yaml


def load_conf():
    '''
    Loads config.yml file
    '''
    CONFIG_FILE_ADR = './config.yml'
    with open(CONFIG_FILE_ADR, 'r') as f:
        conf = yaml.load(f, Loader=yaml.RoundTripLoader)
    return conf

def get_retriever_conf():
    '''
    returns retriever configuration from config.yml file.
    '''
    conf = load_conf()
    check_retriever_conf(conf)
    return conf['retriever']
    
    
    
def check_retriever_conf(conf):
    '''
    Checks if config is done correctly.
    '''
    supported_types = ['SQL_table', 'semantic']
    assert 'retriever' in conf, "Can't find 'retriever' in config.yml"
    assert 'type' in conf['retriever'], "Retriever type not defined in config.yml"
    assert conf['retriever']['type'] in supported_types, \
        f"Retriever type {conf['retriever']['type']} is not on supported"
    
    # Checks if all parameters for SQL_table retriever are set
    if conf['retriever']['type'] == 'SQL_table':
        assert 'host' in conf['retriever'], "Host address not defined for database"
        assert 'user' in conf['retriever'], "User not defined for database"
        assert 'database' in conf['retriever'], "Database name not defined"
    # Checks if all parameters for semantic retriever are set
    elif conf['retriever']['type'] == 'semantic':
        pass