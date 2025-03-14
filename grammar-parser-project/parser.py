import argparse

def read_grammar(file):
    content = []
    variables = ""
    terminals = ""
    rules = []
    rules_cleaned = []
    start_variable = ""
    with open(file, 'r') as f:
        for line in f:
            content.append(line)
    #print(content)
    variables += content[0]
    terminals += content[1]
    for element in content:
        if "->" in element:
            rules.append(element)
         
    start_variable += content[5]
    #print("Variables: " + variables)
    
    #print("Terminals: " + terminals)
    #print("Rules:\n" + "-----")
    for rule in rules:
        for subrule in rule[4:].split('|'):
            #print(rule[:4] + subrule)
            rules_cleaned.append(rule[:4] + subrule.strip('\n'))
    
    #print("Start Variable: " + start_variable)
    return variables, terminals, rules_cleaned, start_variable

def testing_helper(rules, line, variables):
    check = []
    table = []
    for rule in rules: 
        ## this checks if there is an empty string, and if our grammar allows it
        if line == "\n":
            if "S -> e" in rules:
                return True
                
            else: return False
        ## need to complete case where input is not empty
        ## probably will use a 2D array
        else: 
            length = len(line)
            #for i in range(length):
               #for variable in variables:
                   #if (str(variable) + " -> " + line[i]) in rules:
                       
    return False
    
def testing_function(input_file, rules, variables):
    with open(input_file, 'r') as f:
        for line in f: 
            print(line.strip('\n') + ": " + str(testing_helper(rules, line, variables)))
        
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("grammar", help="Grammar file to be utilized")
    parser.add_argument("inputfile", help="Input file to test membership")
    
    args = parser.parse_args()
    #print(args.grammar)
    #print(args.inputfile) 
    terminals = read_grammar(args.grammar)[1]
    start_variable = read_grammar(args.grammar)[3]
    rules = read_grammar(args.grammar)[2]
    variables = read_grammar(args.grammar)[0]
    print("Variables: " + variables)
    
    print("Terminals: " + terminals)
    
    ## rules was originally a list, so I just made a new variable
    ## that contained the rules split up line by line (probably could have just
    ## printed here
    
    print_rules = ''
    for rule in rules: 
        print_rules += str(rule) + "\n"
    
    print("Rules:\n" + "-----\n" + print_rules)
    print("Start Variable: " + start_variable)
    testing_function(args.inputfile, rules, variables)
    
    
if __name__ == "__main__":
    main()