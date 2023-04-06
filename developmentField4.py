import re

def split_sentences(text):
    # split text by punctuation and whitespace
    sentences = re.findall(r'\b\S[^.!?]*[.!?],', text)
    # strip leading/trailing whitespace and add to list
    return [s.strip() for s in sentences]

# example usage
text = "This is the first sentence, This is the second sentence! And this is the third sentence?"
sentences = split_sentences(text)
print(sentences)
