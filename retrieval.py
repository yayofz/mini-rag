import string


def word_freq(text: str, stop_words = None) -> dict:
    text = text.lower()
    translator = str.maketrans(string.punctuation, " " * len(string.punctuation))
    clean_text = text.translate(translator)
    words_list = clean_text.split()
    freq = {}
    if stop_words is None:
        stop_words = set()
    for word in words_list:
        if word in stop_words:
            continue
        if word in freq:
            freq[word] += 1
        else:
            freq[word] = 1
    return freq


def chunk_text(text, size, overlap):
    if size <= 0:
        raise ValueError("size должен быть больше нуля")
    if overlap < 0:
        raise ValueError("overlap не может быть отрицательным")
    if overlap >= size:
        raise ValueError("overlap должен быть меньше size")
    text_list = text.split()
    chunks = []
    step = size - overlap
    for i in range(0, len(text_list), step):
        chunk = " ".join(text_list[i:i + size])
        chunks.append(chunk)
        if i + size >= len(text_list):
            break  # кусок дошёл до конца текста, следующий был бы лишним дублем
    return chunks

with open("notes.txt", encoding="utf-8") as f:
    text = f.read()

chunks = chunk_text(text, 50, 10)

def chunk_score(query: str, part: str):
    score = 0
    query_words = word_freq(query)
    part_freq = word_freq(part)        
    for word in query_words:       
        score += part_freq.get(word, 0)
    return score


def search_chunks(query, chunks, k=3):
    scored = []
    for chunk in chunks:
        score = chunk_score(query, chunk)
        if score > 0:
            scored.append((score, chunk))
    return sorted(scored, key=lambda pair: pair[0], reverse=True)[:k]