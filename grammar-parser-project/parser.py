import argparse

def read_grammar(file):
    """Reads the grammar from a file and extracts variables, terminals, rules, and start variable."""
    with open(file, 'r') as f:
        content = [line.strip() for line in f.readlines() if line.strip()]

    variables = content[0].split(", ")  # Store variables as a list
    terminals = content[1].split(", ")  # Store terminals as a list
    rules = []
    
    # Extract rules
    for line in content[2:-1]:  # Ignore first 2 lines (variables, terminals) and last line (start variable)
        left, right = line.split(" -> ")
        right_parts = right.split(" | ")  # Handle multiple right-hand sides
        rules.append((left, right_parts))

    start_variable = content[-1]  # Start variable is the last line

    return variables, terminals, rules, start_variable

def testing_helper(rules, line, variables):
    """
    Implements the CYK Algorithm to test whether a given input string is generated
    by the context-free grammar in Chomsky Normal Form (CNF).
    """
    line = line.strip()  # Remove newlines/spaces

    if line == "":  # If the input string is empty, check if S -> e is a rule
        return any(left == "S" and "e" in right for left, right in rules)

    length = len(line)
    table = [[[] for _ in range(length)] for _ in range(length)]  # Use lists instead of sets
    
    # Step 1: Fill the first row of the table (single-character substrings)
    for i, char in enumerate(line):
        for left, right_list in rules:
            if char in right_list:  # Terminal rule (A -> a)
                table[0][i].append(left)  # Store variable that generates char
    
    # Step 2: Fill the table using dynamic programming
    for span in range(2, length + 1):  # span = size of substring
        for start in range(length - span + 1):
            end = start + span - 1  # end index of the substring
            
            for split in range(start, end):  # split point
                left_part = table[split - start][start]
                right_part = table[end - split - 1][split + 1]
                
                for left, right_list in rules:
                    for right in right_list:
                        if " " in right:  # Only consider binary rules (A -> B C)
                            parts = right.split()
                            if len(parts) == 2:
                                B, C = parts
                                if B in left_part and C in right_part and left not in table[span - 1][start]:
                                    table[span - 1][start].append(left)

    # Step 3: Recursively check if any variable allows expansion into a longer substring
    for span in range(length):
        for start in range(length - span):
            for left, right_list in rules:
                for right in right_list:
                    if len(right) == 1 and right in table[span][start]:  # Unit production (A -> B)
                        if left not in table[span][start]:
                            table[span][start].append(left)

    # Step 4: Check if the start variable S is in the top-right cell of the table
    return "S" in table[length - 1][0]

def testing_function(input_file, rules, variables):
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            result = "Accept" if testing_helper(rules, line, variables) else "Reject"
            print(f"{line}: {result}")
        
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("grammar", help="Grammar file to be utilized")
    parser.add_argument("inputfile", help="Input file to test membership")
    
    args = parser.parse_args()
    
    variables, terminals, rules, start_variable = read_grammar(args.grammar)

    print("Variables: " + ", ".join(variables))
    print("\nTerminals: " + ", ".join(terminals))
    
    print("\nRules:\n------")
    for left, right_list in rules:
        for right in right_list:
            print(f"{left} -> {right}")
    
    print("\nStart Variable: " + start_variable)
    
    testing_function(args.inputfile, rules, variables)
    
    
if __name__ == "__main__":
    main()
