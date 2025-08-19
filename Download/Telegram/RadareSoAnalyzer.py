#!/usr/bin/env python3
#mod 2 by maalos
"""
symbols_data.append({
                    'address': address,
                    'type': type_,
                    'bind': bind,
                    'size': size,
                    'lib': lib,
                    'name': name,
                    'demangled': demangled
"""                
import os
import subprocess
import sys
import datetime
import json
from pathlib import Path

def run_r2_command(file_path, command):
    try:
        cmd = ['r2', '-q', '-c', command, file_path]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout, result.stderr
    except Exception as e:
        return None, str(e)

def parse_string_output(output):

    strings_data = []
    
    if not output:
        return strings_data
    
    lines = output.strip().split('\n')
    for line in lines:
        if not line.strip():
            continue
        
        parts = line.split(' ', 3)
        if len(parts) >= 4:
            try:
                hex_id = parts[0]
                if hex_id.startswith('0x'):
                    string_content = parts[3] if len(parts) > 3 else ''
                    strings_data.append({
                        'hex_id': hex_id,
                        'size': parts[1],
                        'content': string_content.strip()
                    })
            except IndexError:
                continue
    
    return strings_data

def parse_symbols(output):
 
    symbols_data = []
    
    if not output:
        return symbols_data

    lines = output.strip().split('\n')
    for line in lines:
        if not line.strip():
            continue
        
        parts = line.split(None, 6)  
        if len(parts) >= 7:  
            try:
                address = parts[0]
                type_ = parts[1]
                bind = parts[2]
                size = parts[3]
                lib = parts[4]
                name = parts[5]
                demangled = parts[6] if len(parts) > 6 else ''
                
                symbols_data.append({
                    'address': address,
                    'type': type_,
                    'bind': bind,
                    'size': size,
                    'lib': lib,
                    'name': name,
                    'demangled': demangled
                })
            except IndexError:
                continue

    return symbols_data

def extract_all_strings(file_path):

    all_strings = []
    symbols = []    
    commands = [
        'izz',  
        'iz',   
        'izj',  
        'izq'   
    ]

    for cmd in commands:
        output, error = run_r2_command(file_path, cmd)
        
        if cmd == 'izj' and output:
            try:
                json_data = json.loads(output)
                for entry in json_data:
                    all_strings.append({
                        'hex_id': hex(entry.get('vaddr', 0)),
                        'size': entry.get('length', 0),
                        'content': entry.get('string', ''),
                        'section': entry.get('section', ''),
                        'type': entry.get('type', '')
                    })
            except json.JSONDecodeError:
                pass
        elif output:
            strings_data = parse_string_output(output)
            all_strings.extend(strings_data)

    symbol_output, error = run_r2_command(file_path, 'iE')
    if symbol_output:
        symbols = parse_symbols(symbol_output)

    seen = set()
    unique_strings = []
    for string in all_strings:
        key = (string['hex_id'], string['content'])
        if key not in seen:
            seen.add(key)
            unique_strings.append(string)
    
    unique_strings.sort(key=lambda x: int(x['hex_id'], 16) if x['hex_id'].startswith('0x') else 0)
    return unique_strings, symbols

def analyze_so_files(input_directory='.', output_directory='string_analysis'):
  
    output_path = Path(output_directory)
    output_path.mkdir(exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file_path = output_path / f"string_analysis_log_{timestamp}.txt"
    json_file_path = output_path / f"all_strings_{timestamp}.json"
    
    so_files = [f for f in os.listdir(input_directory) if f.endswith('.so')]
    
    if not so_files:
        print(f"No .so files found in {input_directory}")
        return
    
    print(f"Found {len(so_files)} .so files to analyze")
    print(f"Output will be saved to {output_path}")
    print(f"Log file: {log_file_path}")
    print("-" * 70)
    
    all_results = {}
    
    with open(log_file_path, 'w') as log_file:
        log_file.write(f"String analysis started at {datetime.datetime.now()}\nmod&maalos\n")
        log_file.write(f"Found {len(so_files)} .so files to analyze\n")
        log_file.write("-" * 70 + "\n\n")
        
        for index, file_name in enumerate(so_files, 1):
            file_path = os.path.join(input_directory, file_name)
            base_name = os.path.splitext(file_name)[0]
            
            print(f"\n[{index}/{len(so_files)}] Processing: {file_name}")
            log_file.write(f"\n[{index}/{len(so_files)}] Processing: {file_name}\n")
            
            strings_data, symbols_data = extract_all_strings(file_path)
            
            if strings_data:
                individual_file_path = output_path / f"{base_name}_strings.txt"
                with open(individual_file_path, 'w') as f:
                    f.write(f"File: {file_name}\n")
                    f.write(f"Total strings: {len(strings_data)}\n")
                    f.write(f"Timestamp: {datetime.datetime.now()}\n")
                    f.write("-" * 70 + "\n\n")
                    
                    for entry in strings_data:
                        f.write(f"HEX ID: {entry['hex_id']}\n")
                        f.write(f"SIZE: {entry['size']}\n")
                        f.write(f"STRING: {entry['content']}\n")
                        f.write("-" * 50 + "\n")
                
                print(f"  Found {len(strings_data)} strings")
                print(f"  Results saved to: {individual_file_path}")
                log_file.write(f"  Found {len(strings_data)} strings\n")
                log_file.write(f"  Results saved to: {individual_file_path}\n")
                all_results[file_name] = {'strings': strings_data}
            if symbols_data:
                symbols_file_path = output_path / f"{base_name}_symbols.txt"
                with open(symbols_file_path, 'w') as f:
                    f.write(f"File: {file_name}\n")
                    f.write(f"Total symbols: {len(symbols_data)}\n")
                    f.write(f"Timestamp: {datetime.datetime.now()}\n")
                    f.write("-" * 70 + "\n\n")
                    
                    for entry in symbols_data:
                        f.write(f"ADDRESS: {entry['address']}\n")
                        f.write(f"TYPE: {entry['type']}\n")
                        f.write(f"BIND: {entry['bind']}\n")
                        f.write(f"SIZE: {entry['size']}\n")
                        f.write(f"LIB: {entry['lib']}\n")
                        f.write(f"NAME: {entry['name']}\n")
                        f.write(f"DEMANGLED: {entry['demangled']}\n")
                        f.write("-" * 50 + "\n")
                
                print(f"  Found {len(symbols_data)} symbols")
                print(f"  Symbols saved to: {symbols_file_path}")
                log_file.write(f"  Found {len(symbols_data)} symbols\n")
                log_file.write(f"  Symbols saved to: {symbols_file_path}\n")
 
                if file_name in all_results:
                    all_results[file_name]['symbols'] = symbols_data

        with open(json_file_path, 'w') as f:
            json.dump(all_results, f, indent=2)
        
        log_file.write(f"\n\nString analysis completed at {datetime.datetime.now()}\n")
        log_file.write(f"Global JSON results saved to: {json_file_path}\n")
    
    print("\n" + "-" * 70)
    print(f"String analysis complete! Check the {output_directory} folder for results.")
    print(f"Log file saved to: {log_file_path}")
    print(f"All strings saved to: {json_file_path}")

if __name__ == "__main__":
    try:
        subprocess.run(['r2', '-v'], capture_output=True)
    except FileNotFoundError:
        print("Error: radare2 is not installed or not in PATH")
        print("Please install radare2 first: https://github.com/radareorg/radare2")
        sys.exit(1)
    
    if len(sys.argv) > 1:
        input_dir = sys.argv[1]
    else:
        input_dir = '.'
    
        analyze_so_files(input_dir)
