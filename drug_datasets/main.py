#!/usr/bin/env python3

# Import necessary modules
import sys
import getopt
import drugs_parser as dp


# Main function to call the URL parser
def main(args):
    # Argument handling
    try:
        opts, args = getopt.getopt(args, 'hi:o:', 
                                ['help=', 'input=', 'output='])
    except getopt.GetoptError:
        print('Run script with assigning input and output files.\nEx. python main.py -i inputfile.txt -o outputfile.csv')
        sys.exit()
    for opt, arg in opts:
        if opt in ['-h', '--help']:
            print('Run script with assigning input and output files.\nEx. python main.py -i inputfile.txt -o outputfile.csv')
            sys.exit()
        elif opt in ['-i', '--input']:
            input_list = arg
        elif opt in ['-o', '--output']:
            output_file = arg

    # Class instance
    drugs = dp.drugs_dot_com()
    # Call parser with output file name and list of URLs as inputs
    df = drugs.drugs_parser(input_list, output_file)
    print(df)


if __name__ == '__main__':
    main(sys.argv[1:])
