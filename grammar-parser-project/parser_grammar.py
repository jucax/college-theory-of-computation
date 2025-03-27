import argparse

# Function to parse the context-free grammar from a file
def read_grammar(file):
    content = []  
    variables = ""
    terminals = ""
    rules = {} 
    start_variable = "" 

    # Read file and remove empty lines
    with open(file, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    
    variables = set(lines[0].split(', ')) # First line contains variables
    terminals = set(lines[1].split(', ')) # Second line contains terminals
    
    # Extract production rules from the file (lines 3 to second-to-last line)
    for line in lines[2:-1]:  
        left, right = line.split(" -> ") 
        right_parts = right.split(" | ")  # Handle multiple right-hand side options
        if left not in rules:
            rules[left] = set()  # If LHS variable doesn't exist
        rules[left].update(right_parts)
    
    # Last line contains the start variable
    start_variable = lines[-1]  
    
    return variables, terminals, rules, start_variable

# Function to parse the input strings from a file
def read_input(input_file):
    with open(input_file, 'r') as file:
        return [line.strip() for line in file.readlines()]  # Return list of input strings

# Function to test if a given string belongs to the language
def testing_function(grammar, string):
    # Unpack the grammar
    variables = grammar[0]  # Set of variables
    terminals = grammar[1]  # Set of terminals
    rules = grammar[2]  # Dictionary of rules
    start_variable = grammar[3]  # Start variable

    n = len(string)  # Length of input string
    
    # Handle the empty string case (epsilon)
    if n == 0:  
        if "e" in rules[start_variable]: 
            return "Accept" 
        else:
            return "Reject"
    
    # Initialize a Dynamic Programming 2D table
    dp = [[set() for _ in range(n)] for _ in range(n)]

    # Fill table for substrings of length 1
    for i, char in enumerate(string):
        for var, productions in rules.items():
            if char in productions:
                dp[i][0].add(var)  # If a variable produces char, add it to dp table

    # Fill DP table for substrings of length > 1
    for length in range(2, n+1):  # l (substring length)
        for i in range(n - length + 1):  # i (start position)
            j = i + length - 1  # j (end position)
            for k in range(i, j):  # k (split position)
                for var, productions in rules.items():
                    for production in productions:
                        if len(production) == 2:  
                            B, C = production[0], production[1]  # Extract B and C
                            if B in dp[i][k-i] and C in dp[k+1][j-k-1]:  # Ensure correct dp lookup
                                dp[i][j-i].add(var)  # Store A in table(i, j)

    # Check if the start variable can generate the full string
    if start_variable in dp[0][n-1]:
        return "Accept" 
    else:
        return "Reject"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("grammar_file", help="Grammar file to be utilized")
    parser.add_argument("input_file", help="Input file to test membership")
    
    args = parser.parse_args()
    
    # Parse the grammar and input strings
    grammar = read_grammar(args.grammar_file)
    input_strings = read_input(args.input_file)
    
    # Print parsed grammar
    print(f"Variables: {', '.join(grammar[0])}\n")  # Display variables
    print(f"Terminals: {', '.join(grammar[1])}\n")  # Display terminals
    print("Rules:\n" + "-----")  # Display rules
    for left, right in grammar[2].items():
        for prod in right:
            print(f"{left} -> {prod}")
    print(f"\nStart Variable: {grammar[3]}\n")  # Display start variable
    
    # Check membership of each input string in the language
    for string in input_strings:
        result = testing_function(grammar, string)
        print(f"{string}: {result}")  # Print result (empty string is represented as ε)

# Run the program if executed directly from terminal
if __name__ == "__main__":
    main()
