import readchar
import duckdb

con = duckdb.connect(database='dictionary.db', read_only=True)

def get_word_by_prefix(prefix):
    query = '''
    SELECT word FROM words 
    WHERE lower(word) ^@ $1 AND strlen(word) > strlen($1) 
    LIMIT 1;
    '''
    result = con.execute(query, [prefix.lower()]).fetchall()
    return None if len(result) == 0 else result[0][0]

def get_definition_of_word(word):
    query = "SELECT definition FROM words WHERE lower(word) = ? LIMIT 1;"
    result = con.execute(query, [word.lower()]).fetchall()
    return None if len(result) == 0 else result[0][0]

def get_input(prompt):
    print(f"{prompt}: ", end="", flush=True)
    s = ""
    while True:
        # Save the cursor position
        print("\x1B7", end="", flush=True)
        # Print prefix
        if s != 0:
            top_word = get_word_by_prefix(s)
            if top_word is not None:
                print(f"\x1B[1;34;90m{top_word[len(s):]}\x1B[0m", end="", flush=True)

        # Goto saved position
        print("\x1B8", end="", flush=True)
        char = readchar.readchar()
        if char == "\x08":
            s = s[:len(s)-1]
            print("\x1B[1D", end="", flush=True)
            continue
        
        # Remove to end / clear effect & print char
        print("\x1B[0K", end="", flush=True)
        if char == "\t":
            filled = get_word_by_prefix(s)
            if filled:
                print(filled[len(s):], flush=True)
                return filled
            else:
                continue
        if char == "\r":
            print()
            return s
        print(char, end="", flush=True)
        s += char

word = get_input("Enter word")
print(f"{word}: {get_definition_of_word(word)}")