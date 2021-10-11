import sys
import argparse
from summarizer_test import summarizertest


def main(args):
    parser = argparse.ArgumentParser(description='To get arguments')

    parser.add_argument('--generator_max_length',
                        nargs='*',
                        type=int,
                        default=[80, 110],
                        help='Maximum length of generator text',
                        required=False)

    parser.add_argument('--generator_min_length',
                        nargs='*',
                        type=int,
                        default=[10, 20],
                        help='Minimum length of generator text',
                        required=False)

    parser.add_argument('--generator_top_k',
                        nargs='*',
                        type=int,
                        default=[50, 100],
                        help='top_k of generator model',
                        required=False)

    parser.add_argument('--generator_length_penalty',
                        nargs='*',
                        type=int,
                        default=[0.8, 1],
                        help='length_penalty of generator model',
                        required=False)

    parser.add_argument('--generator_no_repeat_ngram_size',
                        nargs='*',
                        type=int,
                        default=[2, 3],
                        help='no_repeat_ngram_size of generator model',
                        required=False)

    parser.add_argument('--generator_sequences',
                        nargs='*',
                        type=int,
                        default=[2],
                        help='count of sequences that model returned',
                        required=False)

    parser.add_argument('--summarizer_models',
                        nargs='*',
                        type=str,
                        default=["sshleifer/distilbart-cnn-12-6"],
                        help='Models that want test in data',
                        required=False)

    parser.add_argument('--report_out_dir',
                        type=str,
                        default='summarizer-report.json',
                        help='The report of run all models with diffrent parameters',
                        required=False)

    parser.add_argument('--data_dir',
                        type=str,
                        default='summarizer-context.json',
                        help='dataset that include long text for summarization',
                        required=False)

    args = parser.parse_args()

    report_generator = summarizertest.ReportGenerator(
        models_names=args.summarizer_models,
        val_contexts_path=args.data_dir,
        report_path=args.report_out_dir,
        max_lengths=args.generator_max_length,
        min_lengths=args.generator_min_length,
        top_k=args.generator_top_k,
        penalty_l=args.generator_length_penalty,
        no_repeat_ngram_size=args.generator_no_repeat_ngram_size,
        num_return_sequences=args.generator_sequences,
        )

    report_generator.get_report()


if __name__ == "__main__":
    main(sys.argv[1:])
