# ludere
Project ludere is an application that converts text to and from Morse Code.

This project was created as a chance to collaborate and teach a family friend who is interested in programming (and also a ham radio enthusiast).  This project demonstrates Python programming and fundamental programming concepts such as the Software Development Life Cycle (SDLC), source control, software testing and others (see Concepts below).

Why "ludere"?  The word translates from Latin as "to play" which is fitting as the project is a playground for learning Python and programming concepts.

# Getting Started

1. Install a git client and checkout the code.
    1. Reference install instructions https://github.com/git-guides/install-git
    1. Example command line to checkout code `git clone https://github.com/TimAl6ert5/ludere.git`
1. Install python3
    1. Reference instructions for windows https://www.python.org/downloads/windows/
    1. After a successfull install, should be able to run `python --version` at the command line
1. Learning python resources:
    1. https://wiki.python.org/moin/BeginnersGuide
    1. https://docs.python.org/3/tutorial/index.html
    1. https://www.w3schools.com/python/default.asp
1. Use an editor (recommend VS Code with python https://code.visualstudio.com/docs/python/python-tutorial) to view the source files.
1. Pipenv
    1. This project leverages pipenv (https://pypi.org/project/pipenv/) to manage virtual environments and dependencies.  See website for installation details.
    1. From the command line use `pipenv shell` followed by `pipenv install`
    1. *Note: The rest of the instructions assumes you're in a virtual environment with dependencies installed*
1. Run the tests with the command `pytest`
1. Run the REPL program with the command `python repl.py`

# Concepts

The process of converting text to Morse Code (and vice versa) from a human standpoint essentially involves looking up characters in a conversion table.  From a machine perspective, this can naively be done in the same manner.  In the case of invalid input, a human can decide what they want to do with it.  However a machine must be told what to do with it.  A simple approach would be just raise an exception.  This may not be the desired behavior.  A more robust solution would be to indicate exactly where the error in the input is, so the user can fix it.  Another approach may be to handle certain errors internally by making some assumptions, or simply ignoring the problem.  For even more reusability, the program may provide behavioral configuration so it can function as desired by the user.

While this application is trivial, it exemplifies many fundamental concepts in programming and computer science.  Such as:

## Classes and Methods

In Object-Oriented programming, classes are a way to encapsulate state (member variables) and behavior (methods) into reusable templates.  Examples in this application include the Token, Lexer and Translator.

## Data Structures

Data structures provide a way of organizing data in memory for processing.  

### Dictionary

Dictionaries store data in key/value pairs.  In this application, the converter uses dictionaries to save the conversions to and from Morse Code.

### List

Lists store data in a sequential structure.  In this application, lists are used to store the all lexer patterns.

### Tuple

Tuples store a collection of immutable, heterogeneous data.  In this application, tuples are used to store lexer pattern regex and type id.

## Dunder (Magic Methods)

Dunder (short for double under), also known as Magic Methods are methods in Python with special meaning in the interpreter.
A prime example of this is the `__main__` method.

## Exception Handling

Exception handling is a way of dealing with unexpected

## Functions

In programming, a function is a block of code in a repeatable way, with the purpose of reducing redundancy.

## Lexical Analysis

The purpose of the lexer is to convert a sequence of characters into a sequence of tokens.  From the Python Language Reference https://docs.python.org/3/reference/lexical_analysis.html

## Dependency Management

One of the many principles of writing software is to make software that is reusable.  A side effect of this is managing what software you are depending on, and what version.  In this project, the Pipenv tool is used to manage both Python environments and dependencies.

## Regular Expressions (regex)

Regular expressions are a sequence of characters used to define a way to match a pattern of characters in a string.  Regular expressions are widely used, and available in virtually every programming language in some form, as well as many operating environments such as the `grep` command in Linux.  Online tool for testing regex: https://regex101.com/

## REPL

Short for "Read Evaluate Print Loop" is a simple interactive program to interact with the Morse Code converter.

## Testing

Software testing is the discipline of evaluating and/or executing software artifacts with the goal of finding faults.  In this project, the PyTest framework is used to write unit tests.
