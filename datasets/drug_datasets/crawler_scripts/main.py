#!/usr/bin/env python3

# Import necessary modules
import sys
import getopt
import drugs_parser as dp
import extra_drugs_parser as edp


# Main function to call the URL parser
def main(args):
    extra = False
    # Argument handling
    try:
        opts, args = getopt.getopt(args, 'hi:o:u:e:',
                                   ['help=', 'input=', 'output=', 'url=', 'extra='])
    except getopt.GetoptError:
        print('Run script with assigning input and output files.\nEx1. python main.py -i inputfile.txt -o outputfile.csv\n\
Ex2. python main.py -i inputfile.txt -o outputfile.csv -u input.json -e True\n')
        sys.exit()
    for opt, arg in opts:
        if opt in ['-h', '--help']:
            print('Run script with assigning input and output files.\nEx1. python main.py -i inputfile.txt -o outputfile.csv\n\
Ex2. python main.py -i inputfile.txt -o outputfile.csv -u input.json -e True\n')
            sys.exit()
        elif opt in ['-i', '--input']:
            input_list = arg
        elif opt in ['-o', '--output']:
            output_file = arg
        elif opt in ['-u', '--url']:
            url_item_file = arg
        elif opt in ['-e', '--extra']:
            extra = arg

    if extra:
        # Class instance
        drugs = edp.drugs_dot_com()
        # Call parser with output file name, list of URLs and list of the items of URLs as inputs
        df = drugs.drugs_parser(input_list, url_item_file, output_file)
    else:
        # Class instance
        drugs = dp.drugs_dot_com()
        # Call parser with output file name and list of URLs as inputs
        df = drugs.drugs_parser(input_list, output_file)
    print(df)


if __name__ == '__main__':
    main(sys.argv[1:])
