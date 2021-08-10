import sys
import argparse
import add_typo


def main(args):
    parser = argparse.ArgumentParser(description='To get arguments')

    parser.add_argument('-i',
                        '--input',
                        type=str,
                        default='test_data.yml',
                        help='Path of the input nlu.yml file',
                        required=False)

    parser.add_argument('-o',
                        '--output',
                        type=str,
                        default='test_typo_data.yml',
                        help='Path of the output nlu.yml file',
                        required=False)

    parser.add_argument('-n',
                        '--number',
                        type=str,
                        default=1,
                        help='Number of wrong letters in the string',
                        required=False)

    args = parser.parse_args()


    # Instance of AddTypo class
    typo_adder = add_typo.AddTypo()
    # Load the nlu datas
    typo_adder.load_nlu(args.input)
    # Name of the entity tags
    entities = typo_adder.get_entities()
    # Add typo under nlu key examples in the nlu.yml file
    typo_adder.nlu_typo(args.number, entities)
    # Save new nlu.yml data with typos
    typo_adder.save_nlu(args.output)


if __name__ == "__main__":
    main(sys.argv[1:])
