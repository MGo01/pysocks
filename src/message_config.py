file_types = {
    'jpg', 'png', 'docx', 'mp4', 'gif', 'jpeg' 
}

serial_types = {
    'json'
}

format_char_types = {
    'x': 1,
    'c': 1,
    'b': 1,
    'B': 1,
    '?': 1,
    'h': 2,
    'H': 2,
    'i': 4,
    'I': 4,
    'l': 4,
    'L': 4,
    'q': 8,
    'Q': 8,
    'n': 'var',
    'N': 'var',
    'e': 2,
    'f': 4,
    'd': 8,
    's': 'var',
    'p': 'var',
    'P': 'var'
}

byte_order_types = {
    '@':'native', 
    '=':'native',
    '<':'little-endian',
    '>':'big-endian',
    '!':'network'
}