# Token types enumeration

class TokenType:
    IDENTIFIER = "IDENTIFIER"
    KEYWORD = "KEYWORD"
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    SYMBOL = "SYMBOL"

# Token hierarchy dictionary
token_hierarchy = {
    "if": TokenType.KEYWORD,
    "else": TokenType.KEYWORD,
    "print": TokenType.KEYWORD
}


# helper function to check if it is a valid identifier
def is_valid_identifier(lexeme):
    if not lexeme:
        return False

    # Check if the first character is an underscore or a letter
    if not (lexeme[0].isalpha() or lexeme[0] == '_'):
        return False

    # Check the rest of the characters (can be letters, digits, or underscores)
    for char in lexeme[1:]:
        if not (char.isalnum() or char == '_'):
            return False

    return True


# Tokenizer function
def tokenize(source_code):
    tokens = []
    position = 0

    check_error = 0
    try:

        while position < len(source_code):
            # Helper function to check if a character is alphanumeric
            def is_alphanumeric(char):
                return char.isalpha() or char.isdigit() or (char=='_')

            char = source_code[position]

            # Check for whitespace and skip it
            if char.isspace():
                position += 1
                continue

            # Identifier recognition
            if char.isalpha():
                lexeme = char
                position += 1
                while position < len(source_code) and is_alphanumeric(source_code[position]):
                    lexeme += source_code[position]
                    position += 1

                if lexeme in token_hierarchy:
                    token_type = token_hierarchy[lexeme]
                else:
                    # check if it is a valid identifier
                    if is_valid_identifier(lexeme):
                        token_type = TokenType.IDENTIFIER
                    else:
                        raise ValueError(f"Invalid identifier: {lexeme}")

            # Integer or Float recognition
            elif char.isdigit():
                lexeme = char
                position += 1

                is_float = False
                while position < len(source_code):
                    next_char = source_code[position]
                    # checking if it is a float, or a full-stop
                    if next_char == '.':
                        if (position + 1 < len(source_code)):
                            next_next_char = source_code[position+1]
                            if next_next_char.isdigit():
                                is_float = True

                    # checking for illegal identifier
                    elif is_alphanumeric(next_char) and not next_char.isdigit():
                        while position < len(source_code) and is_alphanumeric(source_code[position]):
                            lexeme += source_code[position]
                            position += 1
                        if not is_valid_identifier(lexeme):
                            raise ValueError(f"Invalid identifier: {str(lexeme)}\nIdentifier can't start with digits")

                    elif not next_char.isdigit():
                        break

                    lexeme += next_char
                    position += 1

                token_type = TokenType.FLOAT if is_float else TokenType.INTEGER

            # Symbol recognition
            else:
                lexeme = char
                position += 1
                token_type = TokenType.SYMBOL

            tokens.append((token_type, lexeme))

    except ValueError as e:
        # Handle the error here, e.g., print an error message
        print(e)
        exit()
        # You can also choose to return an error code or take any other action as needed
    if check_error == 0:
        return tokens
    else:
        return None

def check_terminal_type(token, terminal_type, list_of_operators):
    if terminal_type == "y":
        return not (token[1] in ["if", "else"] or token[1] in list_of_operators)
    elif terminal_type == "r":
        num = 0
        if token[0] == "INTEGER":
            num = int(token[1])
        elif token[0] == "FLOAT":
            num = float(token[1])

        return num >= 0
    elif terminal_type in ["else", "if"]:
        return token[1] == terminal_type
    elif terminal_type == "symbols":
        return token[1] in list_of_operators
    else:
        return False


def error_handling_token(
        pp_token,
        p_token,
        cur_token,
        n_token,
        nn_token,
        op_list,
        if_else_count,
    ):
    try:

        def expect_terminal(token, terminal_type, op_list):
            if token is None:
                raise SyntaxError(f'Syntax Error: Expected {terminal_type} but got None')
            if not check_terminal_type(token, terminal_type, op_list):
                raise SyntaxError(f'Syntax Error: Expected {terminal_type} but got {token[1]}')

        if cur_token[1] == "if":
            expect_terminal(n_token, "y", op_list)
            expect_terminal(nn_token, "symbols", op_list)

        elif cur_token[1] == "else":
            if if_else_count < 0:
                raise SyntaxError('Syntax Error: Number of "else" exceeds Number of "if"')
            if not p_token or not n_token:
                raise SyntaxError('Syntax Error: Expected expression before and after "else"')
            if not (
                check_terminal_type(p_token, "y", op_list)
                or check_terminal_type(n_token, "y", op_list)
                or n_token[1] == "if"
            ):
                raise SyntaxError('SYntax Error: Expected "Statement" before and after "else"')

        elif cur_token[1] in op_list:
            if pp_token is None:
                raise SyntaxError('Syntax Error: Condition can only be followed by an "if"')
            if not p_token or not n_token:
                raise SyntaxError('Syntax Error: Expected "statement" before and after an operand')
            if not (
                check_terminal_type(p_token, "y", op_list)
                and check_terminal_type(n_token, "y", op_list)
            ) or pp_token[1] != "if":
                raise SyntaxError('Syntax Error: Expected "statement" before and after an operand or "condition" followed by an "if"')
            if nn_token is None:
                raise SyntaxError('Syntax Error: Expected "statement" after encountering a condition')
            if not (
                check_terminal_type(nn_token, "y", op_list)
                or check_terminal_type(nn_token, "symbols", op_list)
            ):
                raise SyntaxError('Syntax Eroor: Expected "statement" after encountering a condition')

    except SyntaxError as e:
        print(e)
        exit()

def error_handling(tokens, list_of_operators):
        if_else_count = 0
        if_else_flag = False
        tokens_extended = [None] + tokens + [None, None]

        for i in range(1, len(tokens_extended) - 2):
            if tokens_extended[i] is None:
                continue
            elif tokens_extended[i][1] == "if":
                if_else_count += 1
                if_else_flag = True
                if not error_handling_token(
                    None,
                    None,
                    tokens_extended[i],
                    tokens_extended[i + 1],
                    tokens_extended[i + 2],
                    list_of_operators,
                    if_else_count,
                ):
                    return False
            elif tokens_extended[i][1] == "else":
                if not if_else_flag:
                    print('SyntaxError: "else" without an "if"')
                    return False
                if_else_count -= 1
                if not error_handling_token(
                    None,
                    tokens_extended[i - 1],
                    tokens_extended[i],
                    tokens_extended[i + 1],
                    tokens_extended[i + 2],
                    list_of_operators,
                    if_else_count,
                ):
                    return False
            elif tokens_extended[i][1] in list_of_operators:
                if not error_handling_token(
                    tokens_extended[i - 2],
                    tokens_extended[i - 1],
                    tokens_extended[i],
                    tokens_extended[i + 1],
                    tokens_extended[i + 2],
                    list_of_operators,
                    if_else_count,
                ):
                    return False

        return True

# def generate_cross_products(list1, list2):
#     cross_products = []
#     for item1 in list1:
#         for item2 in list2:
#             cross_products.append(item1 + " " + item2)
#     return cross_products

def token_conversion(tokens,token_mapping, grammar_for_CYK):

    mod_tok1 = []
    for token in tokens:
        if (token[1], token[0]) in token_mapping:
            mod_tok1.append((token[0], token_mapping[(token[1], token[0])]))
        elif token[1] not in grammar_for_CYK["OP1"]:
            mod_tok1.append((token[0], "y"))
        elif token[0] in (TokenType.INTEGER, TokenType.FLOAT):
            mod_tok1.append((token[0], "r"))
        else:
            mod_tok1.append(token)

            
    mod_token = []
    i = 0
    while i < len(mod_tok1):
        current_token = mod_tok1[i]
        if (
            i < len(mod_tok1) - 1
            and current_token[1] == "-"
            and mod_tok1[i + 1][0] in (TokenType.INTEGER, TokenType.FLOAT)
        ):
            mod_token.append((mod_tok1[i + 1][0], mod_tok1[i + 1][1]))
            i += 2
        else:
            mod_token.append(current_token)
            i += 1


    # print(mod_token)
    return(mod_token)

memoization = {}

def CYK_check(mod_token, grammar_for_cyk, start, end):
    # Check if the result is already memoized
    if (start, end) in memoization:
        return memoization[(start, end)]
    
    if start == end - 1:
        token = mod_token[start][1]
        derivations = []
        for symbol, productions in grammar_for_cyk.items():
            if token in productions:
                derivations.append(symbol)
        
        # Memoize and return the result
        memoization[(start, end)] = derivations if derivations else None
        return memoization[(start, end)]

    derivations = []
    for i in range(start + 1, end):
        left_derivations = CYK_check(mod_token, grammar_for_cyk, start, i)
        right_derivations = CYK_check(mod_token, grammar_for_cyk, i, end)
        if left_derivations and right_derivations:
            for left in left_derivations:
                for right in right_derivations:
                    for symbol, productions in grammar_for_cyk.items():
                        if f"{left} {right}" in productions:
                            derivations.append(symbol)
    
    # Memoize and return the result
    memoization[(start, end)] = derivations if derivations else None
    return memoization[(start, end)]

def checkGrammar(tokens):
    # write the code the syntactical analysis in this function
    # You CAN use other helper functions and create your own helper functions if needed

    if tokens[-1][1] == ";" and tokens[-1][0] == TokenType.SYMBOL:  # Remove Last Semi-Colon
        tokens.pop()

    grammar_for_CYK = {
        "S":            ["VAR_IF A", "P P", "y"],
        "P":            ["VAR_IF A", "P P", "y"],
        "A":            ["C P", "C VAR_1"],
        "VAR_1":          ["VAr_2 P"],
        "VAr_2":           ["P VAR_ELSE"],
        "C":            ["OPX X", "r", "y"],
        "OPX":          ["X OP1"],
        "VAR_IF":            ["if"],
        "VAR_ELSE":            ["else"],
        "OP1":          ["+", "-", "*", "/", "^", "<", ">", "="],
        "X":            ["r", "y", "OPX X"]
    }

    token_mapping = {
    ("if", TokenType.KEYWORD): "if",
    ("else", TokenType.KEYWORD): "else",
    }

    mod_token  = token_conversion(tokens,token_mapping,grammar_for_CYK)   
    

    n = len(mod_token)

    operation = ["+", "-", "*", "/", "^", "<", ">", "="]
    
    is_derivable = CYK_check(mod_token,  grammar_for_CYK, 0, len(mod_token))
    
    if is_derivable == None or is_derivable == -1 or "S" not in is_derivable:
        error_handling(tokens,operation)
    else:
        return True


# Test the tokenizer
if __name__ == "__main__":
    source_code = input("")
    tokens = tokenize(source_code)
    
    # print(tokens[-1][0]);

    try:

        if source_code.strip() == "":
            raise ValueError("Syntax Error: Statement cannot be empty")
                    
    except ValueError as e:
        # Handle the error here, e.g., print an error message
        print(e)
        exit()

    logs = checkGrammar(tokens)  # You are tasked with implementing the function checkGrammar
    if logs:
        if tokens is not None:
            for token in tokens:
                print(f"Token Type: {token[0]}, Token Value: {token[1]}")