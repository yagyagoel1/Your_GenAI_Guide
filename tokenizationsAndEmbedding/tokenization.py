import tiktoken

encoder = tiktoken.encoding_for_model("gpt-4o")

print("vocab size", encoder.n_vocab)
text= "the cat sat on the mat"
tokens = encoder.encode(text)

print("tokens",tokens)

normal_text = encoder.decode(tokens)

print("normal text",normal_text)

