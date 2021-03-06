from ruamel import yaml
import os


def load_yml(file_adr):
    '''
    Loads .yml file
    '''
    with open(file_adr, 'r') as f:
        dict_ = yaml.load(f, Loader=yaml.RoundTripLoader)
    return dict_

def get_retriever_conf():
    '''
    Returns retriever configuration from config.yml file.
    '''
    CONFIG_FILE_ADR = 'config.yml'
    conf = load_yml(CONFIG_FILE_ADR)
    check_retriever_conf(conf)
    return conf['retriever']

     
def check_retriever_conf(conf):
    '''
    Checks if retriever config is done correctly.
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
        assert 'host' in conf['retriever'], "Host address not defined for database"
        assert 'top_k' in conf['retriever'], "top_k not defined"

def get_processor_conf():
    '''
    Returns processor configuration from config.yml file.
    '''
    CONFIG_FILE_ADR = 'config.yml'
    conf = load_yml(CONFIG_FILE_ADR)
    check_processor_conf(conf)
    return conf['processor']

def check_processor_conf(conf):
    '''
    Checks if processor config is done correctly.
    '''
    supported_types = ['no_process', 'QA', 'abstractive_QA', 'summarizer']
    assert 'processor' in conf, "Can't find 'processor' in config.yml"
    assert 'type' in conf['processor'], "Processor type not defined in config.yml"
    assert conf['processor']['type'] in supported_types, \
        f"Processor type {conf['processor']['type']} is not on supported"
    
    # Checks if all parameters for no_processor type are set(Nothing needs to be set)
    if conf['processor']['type'] == 'no_processor':
        pass
    # Checks if all parameters for QA processor are set
    if conf['processor']['type'] == 'QA':
        assert 'host_url' in conf['processor'], "Host address not defined for QA server"
    # Checks if all parameters for RAG processor are set
    if conf['processor']['type'] == 'RAG':
        pass
    # Checks if all parameters for summarizer processor are set
    if conf['processor']['type'] == 'summarizer':
        assert 'host_url' in conf['processor'], "Host address not defined for summarizer server"

def get_columns(intent, table):
    '''
    Returns a list of columns mapped to intent
    '''
    file_dir = os.path.dirname(__file__)
    INTENT_MAP_FILE_ADR = f'{file_dir}/intent_map.yml'
    intent_map = load_yml(INTENT_MAP_FILE_ADR)
    if intent in intent_map[table]:
        columns = intent_map[table][intent]
        if not isinstance(columns, list):
            columns = [columns]
        return columns
    else:
        return []