# Ye file ka kaam hai extracted text ko clean karna. Jaise extra spaces aur blank lines hatana.

def clean_text(text):
    lines = text.splitlines()                   #text ko alag-alag lines mein divide karega.
    cleaned_lines = []

    for line in lines:
        line = line.strip()                     #har line ke start aur end ki extra spaces hatayega.

        if line:                                 
            cleaned_lines.append(line)           #bilkul empty lines ko htadega

    return "\n".join(cleaned_lines)              #har line k bich newline ko wapas layega