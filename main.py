from unidecode import unidecode
import re

def to_ascii(text):
    replacements = {
        '“': '"', '”': '"', '‘': "'", '’': "'", '…': '...', '–': '-',
        '—': '-', 'œ': 'oe', 'Œ': 'OE', 'æ': 'ae', 'Æ': 'AE',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = unidecode(text)
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    return text

def fix_headers_no_empty_lines(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as infile, \
         open(output_path, 'w', encoding='ascii') as outfile:
        
        in_header = False
        
        for line in infile:
            stripped = line.strip()
            
            # Detect start of header
            if stripped.startswith('[Event'):
                in_header = True
                outfile.write(stripped + '\n')
                continue
            
            if in_header:
                # Skip empty lines inside header
                if stripped == '':
                    continue
                
                # Write header tag lines
                if stripped.startswith('['):
                    outfile.write(stripped + '\n')
                    # End header after [Result]
                    if stripped.startswith('[Result'):
                        in_header = False
                else:
                    # First non-tag line ends header
                    in_header = False
                    outfile.write(line)
            else:
                # Outside header, simply write moves/comments
                outfile.write(line)

# Usage
input_file = 'input_file'
output_file = 'output_ascii_fixed.pgn'

# First convert entire file to ASCII in memory
with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

ascii_content = to_ascii(content)

# Write ascii_content to a temp file
temp_file = 'temp_ascii.pgn'
with open(temp_file, 'w', encoding='ascii') as f:
    f.write(ascii_content)

# Fix headers in the ascii file
fix_headers_no_empty_lines(temp_file, output_file)

print(f"Fixed PGN written to {output_file}")
