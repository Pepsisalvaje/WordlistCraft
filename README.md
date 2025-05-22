# WordlistCraft

Many users, including system administrators, tend to create passwords by modifying familiar words—such as names, dates, or job titles—using predictable patterns like leetspeak, capitalization, and common suffixes. This script automates the generation of password wordlists based on those behaviors. By providing one or more base words, the tool outputs a comprehensive set of possible mutations that reflect real-world password creation habits. It’s designed for use in password audits, red team operations, and targeted wordlist crafting during penetration tests.

## Installation
Just clone the repository, give execute permission to the script, and you're ready to go:
``` shell
git clone https://github.com/Pepsisalvaje/WordlistCraft.git
cd WordlistCraft
chmod +x wordlistcraft.py
```
## Usage
Run the script with any parameters you want. If you need some help you can type -h
``` shell
wordlistcraft.py [-h] --data DATA [--special-chars SPECIAL_CHARS] [--all-special-chars] [--numbers NUMBERS] [--number-length NUMBER_LENGTH] [--toggle-case] [--capitalize-index CAPITALIZE_INDEX] [--output OUTPUT] [--leet] [--audibles]
```
## Features / Functionalities
Here are the features of what the tool can do.

- **Leet Substitutions**: Automatically replace letters in your base words with common leetspeak characters. For example, 'a' becomes '@' or '4', and 'e' becomes '3'. This helps simulate realistic password mutations often used by users.
- **Audible Substitutions**: Replace letters with similar-sounding alternatives, like 'b' with 'v' or 'c' with 'k'. This increases the variety of wordlist entries by accounting for phonetic variations.
- **Toggle Case**: Generate all possible uppercase and lowercase variations of your base words. For example, 'admin' will produce 'admin', 'Admin', 'aDmin', 'ADMIN', etc.
- **Number Patterns**: Add numeric patterns to your base words using '@' as a wildcard to indicate variable digits. For example, the pattern '12@@' will expand to '1200' through '1299'.
- **Number Length**: Generate all numbers with a fixed digit length. For example, setting the length to 3 will produce numbers from '000' to '999', which can be appended or prepended to your base words.
- **Special Characters**: Add special characters before or after your base words or numbers. You can specify which characters to include or use a predefined set of common special characters.
- **Capitalization**: Capitalize the character at a specific position within your base words, allowing targeted mutations like capitalizing the second letter in "john" to get "jOhn".
- **Flexible Output**: Save the generated wordlist to a file of your choice by specifying the output filename. The default is wordlist.txt if no filename is provided.
- **File Size Estimation**: Before generating the wordlist file, get an estimated size of the output based on the current parameters. This helps you anticipate storage needs without creating the full file.

## Examples
Here are some examples of how can you use the tool:
- Generate wordlist with base words "cat" and "dog"
```shell
python3 wordlist_generator.py --data cat,dog
- Use special characters '%' and '&'
```shell
python3 wordlist_generator.py --data cat,dog --special-chars '%,&'
```
- Generate numbers pattern with '@' as wildcard
```shell
python3 wordlist_generator.py --data user --numbers 12@@
```
- Toggle case variations
```shell
python3 wordlist_generator.py --data admin --toggle-case
```
- Save output to custom file
```shell
python3 wordlist_generator.py --data test -o custom_wordlist.txt
```
- Generate all numbers of fixed length 3 (000-999)
```shell
python3 wordlist_generator.py --data number --number-length 3
```
- Capitalize the second word in the combination (index 2)
```shell
python3 wordlist_generator.py --data john,doe,juan --capitalize-index 2
```
- Enable leetspeak mutations
```shell
python3 wordlist_generator.py --data hacker --leet
```
- Enable phonetic (audible) variations
```shell
python3 wordlist_generator.py --data jon --audibles
```
- Full example combining most options:
```shell
python3 wordlist_generator.py --data empresa --all-special-chars --numbers 20@@ --toggle-case --leet --audibles --output full_result.txt
```
