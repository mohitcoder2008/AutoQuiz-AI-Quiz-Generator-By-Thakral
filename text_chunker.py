# jada bddi files ko sort it krke ai ko dena hai isliye chunker bnaaya

def split_text(text, chunk_size):           #text = poora cleaned text or chunks_size = kitne  chuks m krna hai  
    if chunk_size <= 0:                     #agr loi chunk size zero dede to error nhi ayega ab
        return []
    words = text.split()                    #ek line ko alg alg word m tod dega
    chunks = []                             #empty list mein store krenge

    for i in range(0, len(words), chunk_size):      # isme i chunk current , len total words , chunk_size smjh ja
        chunk = words[i:i + chunk_size]

        chunk_text = " ".join(chunk)                #chunk ko string bana kar chunks list mein add karenge.
        chunks.append(chunk_text)

    return chunks