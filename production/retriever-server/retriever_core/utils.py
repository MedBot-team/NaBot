import csv
from haystack import Document
from typing import Dict, List, NoReturn, Generator
from haystack.document_store.faiss import FAISSDocumentStore
from haystack.retriever.dense import DensePassageRetriever
from abc import ABC, abstractmethod
from ruamel import yaml
from decouple import config


# Loads config from config.yml file
def load_conf():
    CONFIG_FILE_ADR = './config.yml'
    with open(CONFIG_FILE_ADR, 'r') as f:
        conf = yaml.load(f, Loader=yaml.RoundTripLoader)
    return conf

def read_csv(path: str) -> Generator:
    """read `csv` file and return a generator
    Parameters
    ----------
    path : str
        path of csv file
    Returns
    -------
    Generator
        generator of extarcted csv file 
    """
    with open(path, mode='r') as csv_file:
        return iter(list(csv.DictReader(csv_file)))


def store_document(dataset: List[Dict[str, str]]) -> List[Document]:
    """haystack want a `Document` type data structure the function take dataset list of dict and generate `Document`
    Parameters
    ----------
    dataset : List[Dict[str, str]]
        dataset list that must include `title` and `text`
    Returns
    -------
    Document
        input type of haystack pipelines
    """
    documents: List[Document] = []
    for row in dataset:
        doc_row: Document = Document(
            text=row["text"],
            meta={"name": row["title"] or ""},
        )
        documents.append(doc_row)

    return documents


class Retriever(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def go(self):
        pass

    @abstractmethod
    def retrieve(self):
        pass


class DensePassage(Retriever):
    def __init__(self):
        self.query_available_model = [
            "facebook/dpr-question_encoder-single-nq-base",
            "deepset/gbert-base-germandpr-question_encoder",
        ]
        self.passage_available_model = [
            "facebook/dpr-ctx_encoder-single-nq-base",
            "deepset/gbert-base-germandpr-ctx_encoder"
        ]

    def go(self, documents: List[Document], query_model_name: str, passage_model_name: str) -> NoReturn:
        """initialize and train model and update faiss documents
        Parameters
        ----------
        documents : List[Document]
            list of dataset with `Document` type 
        query_model_name : str
            query model name
        passage_model_name : str
            passage model name
        Returns
        -------
        NoReturn
        """
        # call FAISS
        document_store = FAISSDocumentStore(
            sql_url = self.build_sql_url(),
            faiss_index_factory_str="Flat",
            return_embedding=True,
            similarity="dot_product",
            progress_bar=False
        )
        # call DPR
        self.__retriever = DensePassageRetriever(
            document_store=document_store,
            query_embedding_model=query_model_name,
            passage_embedding_model=passage_model_name,
            use_gpu=True,
            embed_title=True,
            progress_bar=False,
        )

        # Update FAISS values
        document_store.delete_documents()
        document_store.write_documents(documents)
        document_store.update_embeddings(retriever=self.__retriever)

    def retrieve(self, query: str, top_k=10) -> List[str]:
        """[summary]
        Parameters
        ----------
        query : str
            Question or text according to which we want the similar contexts
        top_k : int, optional
            count of similar context for that must returned, by default 10
        Returns
        -------
        List[str]
            [description]
        """
        contexts = self.__retriever.retrieve(query=query, top_k=top_k)
        texts = [answer.to_dict()['text'] for answer in contexts]

        return texts

    @staticmethod
    def build_sql_url():
        conf = load_conf()['database']
        host = conf['postgres_host']
        user = conf['postgres_user']
        password = config('POSTGRES_PASSWORD')
        db = conf['database']
        url = f"postgresql+psycopg2://{user}:{password}@{host}/{db}"
        return url
