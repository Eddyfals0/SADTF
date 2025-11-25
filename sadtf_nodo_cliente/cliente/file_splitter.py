"""Cortar/juntar archivos en bloques de 1 MB (stub)."""
def split_file(path, block_size=1024*1024):
    with open(path, 'rb') as f:
        i = 0
        while True:
            chunk = f.read(block_size)
            if not chunk:
                break
            yield f"block_{i}", chunk
            i += 1

def join_blocks(block_iter, out_path):
    with open(out_path, 'wb') as out:
        for _id, data in block_iter:
            out.write(data)
