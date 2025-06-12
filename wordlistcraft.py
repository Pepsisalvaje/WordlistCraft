import argparse
import itertools
from typing import List
import sys
import os

ascii = r"""
 _    _                  _  _  _       _    _____               __  _   
| |  | |                | || |(_)     | |  /  __ \             / _|| |  
| |  | |  ___   _ __  __| || | _  ___ | |_ | /  \/ _ __  __ _ | |_ | |_ 
| |/\| | / _ \ | '__|/ _` || || |/ __|| __|| |    | '__|/ _` ||  _|| __|
\  /\  /| (_) || |  | (_| || || |\__ \| |_ | \__/\| |  | (_| || |  | |_ 
 \/  \/  \___/ |_|   \__,_||_||_||___/ \__| \____/|_|   \__,_||_|   \__|
                                                                                                                                
                                                        By Edson Paredes
"""

DESCRIPTION = """
WordlistCraft - Custom wordlist generator
"""

EXAMPLES = """
Examples:
  # Generate wordlist with base words "cat" and "dog"
  python3 wordlist_generator.py --data cat,dog

  # Use special characters '%' and '&'
  python3 wordlist_generator.py --data cat,dog --special-chars '%,&'

  # Generate numbers pattern with '@' as wildcard
  python3 wordlist_generator.py --data user --numbers 12@@

  # Toggle case variations
  python3 wordlist_generator.py --data admin --toggle-case

  # Save output to custom file
  python3 wordlist_generator.py --data test -o custom_wordlist.txt

  # Generate all numbers of fixed length 3 (000-999)
  python3 wordlist_generator.py --data number --number-length 3

  # Capitalize the second word in the combination (index 2)
  python3 wordlist_generator.py --data john,doe,juan --capitalize-index 2

  # Full example combining most options:
  python3 wordlist_generator.py --data alice,bob --special-chars '!,$' --numbers 9@@ --capitalize-index 1 --output results.txt
  
"""

def generar_leet_speak(palabra: str) -> List[str]:
    leet_map = {
        'a': ['a', '@', '4'],
        'b': ['b','8', '6'],
        'c': ['c', '(', '<', '{', '['],
        'd': ['d'],
        'e': ['e', '3'],
        'f': ['f'],
        'g': ['g', '9', '6'],
        'h': ['h', '#'],
        'i': ['i', '1', '!', '|'],
        'j': ['j'],
        'k': ['k'],
        'l': ['l', '1', '|', '7'],
        'm': ['m'],
        'n': ['n'],
        'o': ['o', '0', '()','@'],
        'p': ['p'],
        'q': ['q', '9'],
        'r': ['r'],
        's': ['s', '$', '5', '§'],
        't': ['t', '7', '+'],
        'u': ['u', 'v'],
        'v': ['v', 'u'],
        'w': ['w', 'vv'],
        'x': ['x', '%', '*'],
        'y': ['y'],
        'z': ['z', '2'],
    }

    partes = []
    for c in palabra:
        if c in leet_map:
            partes.append(leet_map[c])
        else:
            partes.append([c])
    combinaciones = [''.join(p) for p in itertools.product(*partes)]
    return combinaciones

def generar_audibles(palabra: str) -> List[str]:
    reemplazos = {
        'v': ['v', 'b'],
        'b': ['b', 'v'],
        's': ['s', 'z'],
        'z': ['z', 's'],
        'c': ['c', 'k', 'q'],
        'k': ['k', 'c', 'q'],
        'q': ['q', 'k', 'c'],
        'll': ['ll', 'y'],
        'y': ['y', 'll'],
        'r': ['r', 'rr'],
        'rr': ['rr', 'r'],
        't': ['t', 'd'],
        'd': ['d', 't'],
        'g': ['g', 'j'],
        'j': ['j', 'g']
    }

    segmentos = []
    i = 0
    palabra_lower = palabra
    while i < len(palabra):
        if i + 1 < len(palabra):
            par = palabra_lower[i:i+2]
            if par in reemplazos:
                segmentos.append(reemplazos[par])
                i += 2
                continue
        c = palabra_lower[i]
        if c in reemplazos:
            segmentos.append(reemplazos[c])
        else:
            segmentos.append([palabra[i]])
        i += 1

    combinaciones = [''.join(p) for p in itertools.product(*segmentos)]
    return combinaciones

def generar_numeros_con_patron(patron: str) -> List[str]:
    partes = []
    for caracter in patron:
        if caracter == '@':
            partes.append([str(i) for i in range(10)])
        else:
            partes.append([caracter])
    return [''.join(p) for p in itertools.product(*partes)]

def generar_toggle_case(palabra: str) -> List[str]:
    combinaciones = list(itertools.product(*[
        (c.lower(), c.upper()) if c.isalpha() else (c,)
        for c in palabra
    ]))
    return [''.join(comb) for comb in combinaciones]

def main():

    parser = argparse.ArgumentParser(
        description = ascii + DESCRIPTION,
        epilog= EXAMPLES,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    
    parser.add_argument('--data', '-d', required=True, help='Base values separated by comma')
    parser.add_argument('--special-chars', help="Special characters separated by commas '%%,&&,/'")
    parser.add_argument('--all-special-chars', action='store_true', help='Use all special characters')
    parser.add_argument('--numbers', help="Number pattern. Use '@' to indicate variable digits.")
    parser.add_argument('--number-length', type=int, help='Fixed length to generate all possible numbers')
    parser.add_argument('--toggle-case', action='store_true', help='Toggle between uppercase and lowercase letters')
    parser.add_argument('--capitalize-index', type=int, help='Index of the word to which capitalization is to be applied')
    parser.add_argument('--output','-o', default='wordlist.txt', help='Output file (default name is wordlist.txt)')
    parser.add_argument('--leet', action='store_true', help='Generate leet speak variations of the base words')
    parser.add_argument('--audibles', action='store_true', help='Generate audible variations')
    
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()

    args = parser.parse_args()    

    data_originales = args.data.split(',')

    ## ERROR MESSAGES-data alice,bob --special-chars '!,$' --numbers 9@@ --capitalize-index 0 --output results.txt
    if args.toggle_case and args.capitalize_index is not None:
        parser.error("Can't use --toggle-case and --capitalize-index at the same time.")
    if args.numbers and args.number_length:
        parser.error("Can't use --numbers y --number-length at the same time.")
    if '--special-chars' in sys.argv and '--all-special-chars' in sys.argv:
        parser.error("Can't use --special-chars y --all-special-chars at the same time.")
    if args.all_special_chars and args.special_chars:
        parser.error("Can't use --special-chars y --all-special-chars at the same time.")

    ## FUNCTIONS 

    if args.capitalize_index is not None:
        max_len = max(len(palabra) for palabra in data_originales)
        if args.capitalize_index < 1 or args.capitalize_index > max_len:
            parser.error(f"--capitalize-index have to be between 1 and {max_len}")

    if args.capitalize_index is not None:
        data = []
        for palabra in data_originales:
            if 0 < args.capitalize_index <= len(palabra):
                palabra = palabra[:args.capitalize_index - 1] + palabra[args.capitalize_index - 1].upper() + palabra[args.capitalize_index:]
            data.append(palabra)
    else:
        if args.toggle_case:
            data = []
            for palabra in data_originales:
                data.extend(generar_toggle_case(palabra))
            data = list(set(data))
            
        else:
            data = data_originales

    if args.leet:
        data_leet = []
        for palabra in data:
            data_leet.extend(generar_leet_speak(palabra))
            
        data = list(set(data_leet))
    
    if args.audibles:
        data_audibles = []
        for palabra in data:
            data_audibles.extend(generar_audibles(palabra))
        data = list(set(data_audibles))
        

    special_chars = list(args.special_chars) if args.special_chars else []
    if args.all_special_chars:
        special_chars = list("!@#$%^&*()_-+=}{[]:;\"'<>.,?/")

    numbers = []
    if args.number_length:
        numbers = [str(i).zfill(args.number_length) for i in range(10 ** args.number_length)]
    elif args.numbers:
        numbers = generar_numeros_con_patron(args.numbers)

    

    output_filename = args.output if args.output else "wordlist.txt"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, output_filename)

    print(ascii)

    with open(output_path, 'w') as f:
        if args.data and not (args.special_chars or args.all_special_chars or args.numbers or args.number_length or args.toggle_case or args.capitalize_index or args.leet or args.audibles):
            for r in range(1, len(data_originales) + 1):
                for combo in itertools.permutations(data_originales, r):
                    f.write(''.join(combo) + '\n')
        else:
            combinaciones_vistas = set()
            for dato in data:
                base = dato
                if base not in combinaciones_vistas:
                    f.write(base + '\n')
                    combinaciones_vistas.add(base)

                for num in numbers:
                    c1 = f'{base}{num}'
                    if c1 not in combinaciones_vistas:
                        f.write(c1 + '\n')
                        combinaciones_vistas.add(c1)

                    c2 = f'{num}{base}'
                    if c2 not in combinaciones_vistas:
                        f.write(c2 + '\n')
                        combinaciones_vistas.add(c2)

                for esp in special_chars:
                    c1 = f'{base}{esp}'
                    if c1 not in combinaciones_vistas:
                        f.write(c1 + '\n')
                        combinaciones_vistas.add(c1)

                    c2 = f'{esp}{base}'
                    if c2 not in combinaciones_vistas:
                        f.write(c2 + '\n')
                        combinaciones_vistas.add(c2)

                for num in numbers:
                    for esp in special_chars:
                        combs = [
                            f'{base}{num}{esp}',
                            f'{base}{esp}{num}',
                            f'{num}{base}{esp}',
                            f'{esp}{base}{num}'
                        ]
                        for c in combs:
                            if c not in combinaciones_vistas:
                                f.write(c + '\n')
                                combinaciones_vistas.add(c)


#    combinaciones_finales = set()
#
    #if args.data and not (args.special_chars or args.all_special_chars or args.numbers or args.number_length or args.toggle_case or args.capitalize_index or args.leet or args.audibles):
    #    combinaciones_finales = set()
    #    for r in range(1, len(data_originales) + 1):
    #        for combo in itertools.permutations(data_originales, r):
    #            combinaciones_finales.add(''.join(combo))
    #else:
    #    for dato in data:
    #        base = dato
    #        combinaciones_finales.add(base)
#
    #        for num in numbers:
    #            combinaciones_finales.add(f'{base}{num}')
    #            combinaciones_finales.add(f'{num}{base}')
#
    #        for esp in special_chars:
    #            combinaciones_finales.add(f'{base}{esp}')
    #            combinaciones_finales.add(f'{esp}{base}')
#
    #        for num in numbers:
    #            for esp in special_chars:
    #                combinaciones_finales.add(f'{base}{num}{esp}')
    #                combinaciones_finales.add(f'{base}{esp}{num}')
    #                combinaciones_finales.add(f'{num}{base}{esp}')
    #                combinaciones_finales.add(f'{esp}{base}{num}')


    print("Wordlist creada con éxito.")

    #
    #tamaño_estimado = sum(len((palabra + '\n').encode('utf-8')) for palabra in combinaciones_finales)
#
    #if tamaño_estimado >= 1_000_000_000:
    #    print(f"Tamaño estimado del archivo {args.output}: {tamaño_estimado / 1_000_000_000:.2f} GB con {len(combinaciones_finales)} combinaciones.")
    #else:
    #    print(f"Tamaño estimado del archivo {args.output}: {tamaño_estimado / 1_000_000:.2f} MB con {len(combinaciones_finales)} combinaciones.")
    #print("\n")
#
    #with open(output_path, 'w') as f:
    #    for item in sorted(combinaciones_finales):
    #        f.write(f'{item}\n')
#
    #
    

if __name__ == '__main__':
    main()