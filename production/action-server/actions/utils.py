from ruamel import yaml


def load_yml(file_adr):
    '''
    Loads .yml file
    '''
    with open(file_adr, 'r') as f:
        dict_ = yaml.load(f, Loader=yaml.RoundTripLoader)
    return dict_

def get_retriever_conf():
    '''
    returns retriever configuration from config.yml file.
    '''
    CONFIG_FILE_ADR = './config.yml'
    conf = load_yml(CONFIG_FILE_ADR)
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
        assert 'tables' in conf['retriever'], "Data tables not defined"
    # Checks if all parameters for semantic retriever are set
    elif conf['retriever']['type'] == 'semantic':
        pass

def get_columns(intent, table):
    '''
    returns a list of columns mapped to intent
    '''
    INTENT_MAP_FILE_ADR = 'intent_map.yml'
    intent_map = load_yml(INTENT_MAP_FILE_ADR)
    if intent in intent_map[table]:
        columns = intent_map[table][intent]
        if not isinstance(columns, list):
            columns = [columns]
        return columns
    else:
        return []