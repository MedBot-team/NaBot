import sys
import argparse
from dpr_qa_test import DPRTest


def main(args):
    parser = argparse.ArgumentParser(description='To get arguments')

    parser.add_argument('--max_seq_lens', 
                        nargs = '*', 
                        type = int,
                        default = [256],
                        help='Max sequence length of one input text for the model', 
                        required = False)

    parser.add_argument('--max_seq_len_passages', 
                        nargs = '*', 
                        type = int,
                        default = [256],
                        help = 'Longest length of each passage/context sequence. Maximum number of tokens for the passage text. Longer ones will be cut down.', 
                        required = False)
    
    parser.add_argument('--max_seq_len_queries', 
                    nargs = '*', 
                    type = int,
                    default = [64],
                    help = 'Longest length of each query sequence. Maximum number of tokens for the query text. Longer ones will be cut down.', 
                    required = False)

    parser.add_argument('--embed_titles', 
                    nargs = '*', 
                    type = bool,
                    default = [True, False],
                    help = 'Whether to concatenate title and passage to a text pair that is then used to create the embedding.', 
                    required = False)

    parser.add_argument('--context_window_sizes', 
                    nargs = '*', 
                    type = int,
                    default = [150, 175],
                    help = 'The size, in characters, of the window around the answer span that is used when displaying the context around the answer.', 
                    required = False) 

    parser.add_argument('--doc_strides', 
                    nargs = '*', 
                    type = int,
                    default = [100, 128],
                    help = 'Length of striding window for splitting long texts (used if len(text) > max_seq_len)', 
                    required = False) 

    parser.add_argument('--retriever_top_ks', 
                    nargs = '*', 
                    type = int,
                    default = [3, 5, 7],
                    help = 'How many documents to return per query.', 
                    required = False) 

    parser.add_argument('--reader_top_ks', 
                    nargs = '*', 
                    type = int,
                    default = [3, 5, 7],
                    help = 'The maximum number of answers to return', 
                    required = False) 

    parser.add_argument('--reader_models', 
                    nargs = '*', 
                    type = str,
                    default = ['ktrapeznikov/albert-xlarge-v2-squad-v2',
                                'deepset/roberta-base-squad2',
                                'deepset/minilm-uncased-squad2',
                                'ahotrod/albert_xxlargev1_squad2_512'],
                    help = 'The maximum number of answers to return', 
                    required = False) 

    parser.add_argument('--text_datasets', 
                    nargs = '*', 
                    type = str,
                    default = ['titleText-threeSentences.csv',
                                'titleText-paragraphs.csv'],
                    help = 'The maximum number of answers to return', 
                    required = False) 

    parser.add_argument('--qa_datasets', 
                    nargs = '*', 
                    type = str,
                    default = ['qa-SQUAD.json'],
                    help = 'The maximum number of answers to return', 
                    required = False) 

    parser.add_argument('--report_out_dir', 
                    type = str,
                    default = 'dpr-qa-report.csv',
                    help = 'The maximum number of answers to return', 
                    required = False) 

    parser.add_argument('--sample_out_dir', 
                    type = str,
                    default = 'dpr-qa-sample.json',
                    help = 'The maximum number of answers to return', 
                    required = False) 

    args = parser.parse_args()

    # Instance of AddTypo class
    report_generator = DPRTest.report_generator(max_seq_lens = args.max_seq_lens, 
                                    max_seq_len_passages = args.max_seq_len_passages,   
                                    max_seq_len_queries = args.max_seq_len_queries,
                                    embed_titles = args.embed_titles, 
                                    context_window_sizes = args.context_window_sizes,
                                    doc_strides = args.doc_strides,
                                    retriever_top_ks = args.retriever_top_ks,
                                    reader_top_ks = args.reader_top_ks, 
                                    reader_models = args.reader_models,
                                    text_datasets = args.text_datasets,
                                    qa_datasets = args.qa_datasets,
                                    report_out_dir = args.qa_datasets,
                                    sample_out_dir = args.sample_out_dir,
                                    )
    
    _, _ = report_generator.get_report()


if __name__ == "__main__":
    main(sys.argv[1:])
