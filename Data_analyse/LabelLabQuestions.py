import sys
import pandas as pd

## Run with this:
# python LabelLabQuestions.py '<labdataset path>' 'questions column name' '<final file name>.csv'
# ex: python LabelLabQuestions.py 'labtestonline_datasets/dataset_statics/url_item_static.csv' 'item' 'labeledquestions.csv'

class LabelQuestions():
    def __init__(self, cv_path=None, questions_column_name=None, intent_tag_list=[]):
        if cv_path == None:
            raise Exception("Error: [path] can't be empty.")
        if intent_tag_list==[]:
            raise Exception("Error: [intent_tag_list] can't be empty")
        if questions_column_name==None:
            raise Exception("Error: [questions_column_name] can't be empty")
            
        self.path = cv_path
        self.tag_list = intent_tag_list
        self.questions = pd.read_csv(self.path)[questions_column_name].values
        self.intents = []
    def run(self, saved_name=None):
        print('Whats these questions intent?')
        print('Current intent list: ' , self.tag_list)
        print('Print "finish" to finish labeling.')
        counter = 0
        for q in self.questions:
            intent = ''
            while(not intent in self.tag_list):
                intent = input('Type intent for this question: [ '+q+' ]')
                if intent=='finish':
                    self.finishing(counter, saved_name)
                    return
                if intent in self.tag_list:
                    self.intents.append(intent)
                    break
                else :
                    print('ERROR: I done have this tag in our list type one of current intent list.')
            counter += 1
        print(self.intents)
        
    def finishing(self, counter, saved_name):
        self.df = pd.DataFrame(list(zip(self.questions[:counter],self.intents)), columns=['question', 'intent'])
        if saved_name:
            self.df.to_csv('/'.join(self.path.split('/')[:-1])+'/'+saved_name, index=False)
def main():
    args = sys.argv
    intent_tag_list = ['usage_lab','detail_lab','need_lab','during_lab','prepare_lab','risk_lab','result_lab','any_detail_lab']
    LabelQuestions(cv_path=args[1], questions_column_name=args[2], intent_tag_list=intent_tag_list).run(args[3])  
if __name__ == '__main__':
    main()
