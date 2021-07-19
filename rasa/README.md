## To-Do list

1. ~~Design Chabot to retrieve information from both drug and lab datasets:~~
    
    - ~~Write notebook to generate nlu.yml data from datasets~~ (Done)
    - ~~Write action scripts to retrieve data from datasets~~ (Done)
    - ~~Fix **None value** return problem for some drugs/labs~~ (Has been fixed by replacing slots by entities) 
    - ~~Fix retrieval algorithm to work for both forms and entities~~ (Done)

2. Make lab test names lowercase in the database
    - Also .lower() should be added to actions/lab_retriever.py -> line:41/44

3. Convert data generation notebook to python script
    - Also, remove duplicate lines in the yml file (New feature)
4. Add empty output handling feature to actions: Return 'Sorry massage', if the desired value in the dataframe does not exist.
5. Add typo fixer feature: Return similar drug/lab by finding word similarities. Ex. In the case of *acetamenophen*, details of *acetaminophen* should be returned.
6. Add *slot_reset* custom action
    - This action should be added after *drug/lab_retrieve* in data/rules.yml
7. Add some stories in the *stories.yml* file to define good/bad paths
8. Add *fall_back* and *out_of_scope* features
