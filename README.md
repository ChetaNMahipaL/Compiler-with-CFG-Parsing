# Simple Compiler with CYK Algorithm for CNF Grammars

## Introduction

This project is a simple compiler for a programming language that supports various token types, including identifiers, keywords, integers, floating-point numbers, and symbols. The goal is to perform tokenization (lexical analysis) and syntactic analysis using the CYK (Cocke-Younger-Kasami) algorithm for context-free grammars (CFG).

## Features

- Tokenizes source code into different token types.
- Performs syntactic analysis based on a provided CFG.
- Detects and reports lexical and syntactic errors.
- Handles token hierarchy conflicts (e.g., prioritizing keywords over identifiers).

## Implementation

The project is implemented in Python and consists of the following components:

1. **Tokenization (Lexical Analysis):**
   - Finite State Automata (FSAs) are implemented for each token type.
   - Prioritizes token recognition based on token hierarchy.
   - Handles conflicts and resolves ambiguities.

2. **Syntactic Analysis:**
   - A context-free grammar (CFG) based on the provided rules is implemented.
   - The CYK algorithm is used to parse the tokens and check if they conform to the CFG.
   - Appropriate exceptions are raised for lexical and syntactic errors.

3. **Input/Output:**
   - The program prompts the user to enter source code.
   - Outputs token types and values for valid input.
   - Raises lexical errors for invalid identifiers.
   - Raises syntactic errors for code that doesn't follow grammar rules.

## How to Use

1. Run the program.
2. Enter the source code when prompted.
3. The program will perform tokenization and syntactic analysis.
4. It will output token types and values for valid input or raise errors for invalid code.

## Project Significance

This project demonstrates the following skills and knowledge:

- Implementation of lexical analysis using FSAs.
- Utilization of the CYK algorithm for parsing based on CFG.
- Handling of lexical and syntactic errors with informative error messages.
- Understanding of token hierarchies and conflict resolution.
