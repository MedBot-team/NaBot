import csv
from haystack import Document
from typing import Dict, List, NoReturn
from haystack.document_store.faiss import FAISSDocumentStore
from haystack.retriever.dense import DensePassageRetriever


def read_csv(path: str) -> csv.DictReader:
    """read `csv` file and return a generator

    Parameters
    ----------
    path : str
        path of csv file

    Returns
    -------
    csv.DictReader
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


class Retriever:
    def __init__(self):
        super(Retriever, self).__init__()
        # All huggingface models that can run
        self.query_available_model = [
            "facebook/dpr-question_encoder-single-nq-base",
            "deepset/gbert-base-germandpr-question_encoder",
        ]
        self.passage_available_model = [
            "facebook/dpr-ctx_encoder-single-nq-base",
            "deepset/gbert-base-germandpr-ctx_encoder"
        ]

    def __call_faiss(self) -> FAISSDocumentStore:
        """create a object for use faiss storing document with `dot_product` similarity mode

        Returns
        -------
        FAISSDocumentStore
            object of FAISS
        """
        return FAISSDocumentStore(
            faiss_index_factory_str="Flat",
            return_embedding=True,
            similarity="dot_product",
        )

    def __call_dpr(
            self,
            document_store: List[Document],
            query_model_name: str,
            passage_model_name: str) -> DensePassageRetriever:
        """create a object for dense passage retriver

        Parameters
        ----------
        document_store : List[Document]
            list of dataset that stored with `Document` type
        query_model_name : str
            model of query
        passage_model_name : str
            model of passage

        Returns
        -------
        DensePassageRetriever
            DensePassageRetriever object
        """
        return DensePassageRetriever(
            document_store=document_store,
            query_embedding_model=query_model_name,
            passage_embedding_model=passage_model_name,
            use_gpu=True,
            embed_title=True,
        )

    def model_init(self, documents: List[Document], query_model_name: str, passage_model_name: str) -> NoReturn:
        """initialize and training model

        Parameters
        ----------
        documents : List[Document]
            the dataset that collected for model
        query_model_name : str
            model of query
        passage_model_name : str
            model of passage

        Returns
        -------
        NoReturn

        """
        # call FAISS
        document_store = self.__call_faiss()
        # call DPR
        self.__retriever = self.__call_dpr(
            document_store, query_model_name, passage_model_name)

        # Update FAISS values
        document_store.delete_documents()
        document_store.write_documents(documents)
        document_store.update_embeddings(retriever=self.__retriever)

    def retrieve(self, query: str, top_k=10) -> List[str]:
        """retrieve texts that DPR model returned

        Parameters
        ----------
        query : str
            text for search in documents and model find related text
        top_k : int, optional
            count of returned related text, by default 10

        Returns
        -------
        List[str]
            list of answers
        """
        contexts = self.__retriever.retrieve(query=query, top_k=top_k)
        texts = []
        for answer in contexts:
            texts.append(
                answer.to_dict()['text']
            )

        return texts
