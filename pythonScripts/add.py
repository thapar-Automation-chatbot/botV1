import os

# Define the paths to the NLU and domain files
curr_dir = os.getcwd()
nlu_file_path = os.path.join(os.path.dirname(curr_dir),'data','nlu.yml') 
domain_file_path = os.path.join(os.path.dirname(curr_dir),'domain.yml')  
rules_file_path = os.path.join(os.path.dirname(curr_dir),'data','rules.yml')
# cannot use \t have to use 2 spacess
#-------------------------------------------------------------------------------------------
def add_intent_rules_utter(intent, examples,responses,rule_name, nlu_file_path, domain_file_path,rules_file_path):
    utter = 'utter_'+intent
    formatted_responses = f'\n\n  {utter}:\n'
    for response in responses:
        formatted_responses += f'    - text: {response}\n'
    # Append the intent and examples to the NLU file
    with open(nlu_file_path, "a") as nlu_file:
        nlu_file.write(f"\n- intent: {intent}\n")
        nlu_file.write(f"  examples: |\n")
        for example in examples:
            nlu_file.write(f"    - {example}\n")

    with open (domain_file_path,'r') as domain_file:
        file_text = domain_file.read()
    pointer_loc_after_intents = file_text.find('intents:') + len('intents:')
    file_text = file_text[:pointer_loc_after_intents] + f"\n  - {intent}" + file_text[pointer_loc_after_intents:]
    pointer_loc_after_responses = file_text.find('responses:') + len('responses:')
    file_text = file_text[:pointer_loc_after_responses] + formatted_responses + file_text[pointer_loc_after_responses:]
    
    with open(domain_file_path,'w') as domain_file:
        domain_file.write(file_text)

    with open(rules_file_path,'a') as rules_file:
        rules_file.write('\n\n')
        rules_file.write(f'- rule: {rule_name}\n')
        rules_file.write(f'  steps: \n')
        rules_file.write(f'  - intent: {intent}\n')
        rules_file.write(f'  - action: {utter}\n')

def main():
    intent = input("Enter the intent name: ")
    rule_name = 'Respond to '+ intent
    utter = 'utter_'+intent
    responses =[]
    while True:
        response = input("Enter an response (or 'done' to finish): ")
        if response.lower() == "done":
            break
        responses.append(response)

    examples = []
    while True:
        example = input("Enter an example (or 'done' to finish): ")
        if example.lower() == "done":
            break
        examples.append(example)

    if not intent or not examples:
        print("Intent and examples are required.")
        return

    add_intent_rules_utter(intent, examples,responses,rule_name, nlu_file_path, domain_file_path,rules_file_path)
    print(f"Intent '{intent}' , {utter},{rule_name} and rule added to NLU ,domain,rules files.")

if __name__ == "__main__":
    main()
