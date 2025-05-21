# WordlistCraft

Many users, including system administrators, tend to create passwords by modifying familiar words—such as names, dates, or job titles—using predictable patterns like leetspeak, capitalization, and common suffixes. This script automates the generation of password wordlists based on those behaviors. By providing one or more base words, the tool outputs a comprehensive set of possible mutations that reflect real-world password creation habits. It’s designed for use in password audits, red team operations, and targeted wordlist crafting during penetration tests.

## 

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
