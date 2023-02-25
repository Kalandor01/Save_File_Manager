
def encode_save(save_file_lines:list[str]|str, save_num=1, save_name="save*", save_ext="sav", version=2, encoding="utf-8"):
    """
    Creates a file that has been encoded, from a string or a list of strings.\n
    If `save_name` contains a "*", when creating the file, it will be replaced in the name by the `save_num`.\n
    version numbers:
    - 1: normal: weak
    - 2: secure: stronger
    - 3: super-secure: strogest (only works, if opened on the same location, with the same name)
    - 4: stupid secure: v3 but encription "expires" on the next day\n
    You shouldn't need to change the `encoding`, but it stays there for legacy reasons.
    """
    from math import pi, sqrt
    from base64 import b64encode
    from numpy import random as npr

    def encode_line(line, r:npr.RandomState):
        encode_64 = r.randint(2, 5)
        # encoding into bytes
        line_enc = str(line).encode(encoding, "replace")
        # encode to base64 x times
        for _ in range(encode_64):
            line_enc = b64encode(line_enc)
        # back to text
        line_enc = line_enc.decode(encoding)
        # shuffling bytes
        line_bytes = bytearray(line_enc, "utf-8")
        line_bytes_enc = bytearray("", "utf-8")
        for byte in line_bytes:
            line_bytes_enc.append(byte + r.randint(-32, 134))
        # \n + write
        line_bytes_enc.append(10)
        return line_bytes_enc

    rr = npr.RandomState(int(sqrt((save_num * pi)**7.42 * (3853.587 + save_num * pi)) % 2**32))
    with open(f'{save_name.replace("*", str(save_num))}.{save_ext}', "wb") as f:
        if type(save_file_lines) is str:
            save_file_lines = [save_file_lines]
        # v1
        if version == 1:
            f.write(bytes(encode_line(1, rr)))
            f.write(bytes(encode_line(-1, rr)))
            rr = npr.RandomState(int(sqrt((save_num * pi)**7.42 * (3853.587 + save_num * pi)) % 2**32))
            for line in save_file_lines:
                encoded_line = encode_line(line, rr)
                f.write(bytes(encoded_line))
        else:
            from datetime import datetime
            f.write(bytes(encode_line(version, rr)))
            # v2
            if version == 2:
                seed_num = int(str(datetime.now()).replace(" ", "").replace("-", "").replace(".", "").replace(":", "")) / sqrt((save_num * pi)**17.42 * (0.587 + save_num * pi))
            # v3-4
            elif version == 3 or version == 4:
                import os.path
                path = os.path.dirname(os.path.abspath(__file__)) + f'{save_name.replace("*", str(save_num))}.{save_ext}'
                b_path = bytes(path, "utf-8")
                num_p = 1
                for by in b_path:
                    num_p *= int(by)
                    num_p = int(str(num_p).replace("0", ""))
                t_now = int(str(datetime.now()).replace(" ", "").replace("-", "").replace(".", "").replace(":", "")) / sqrt((save_num * pi)**1.42 * (0.587 + save_num * pi))
                seed_num = float(str(num_p * t_now).replace("0", "").replace("e+", "")) * 15439813
            else:
                seed_num = sqrt((save_num * pi)**7.42 * (3853.587 + save_num * pi))
            encoded_line = encode_line(seed_num, rr)
            # v4
            if version == 4:
                n = datetime.now()
                seed_num *= (n.year + n.month + n.day)
            seed = npr.RandomState(int(seed_num % 2**32))
            f.write(bytes(encoded_line))
            for line in save_file_lines:
                encoded_line = encode_line(line, seed)
                f.write(bytes(encoded_line))


def decode_save(save_num=1, save_name="save*", save_ext="sav", decode_until=-1, encoding="utf-8"):
    """
    Returns a list of strings, decoded fron the encoded file.\n
    If `save_name` contains a "*", when opening the file, it will be replaced in the name by the `save_num`.\n
    `decode_until` controlls how many lines the function should decode (strarting from the beggining, with 1).\n
    You shouldn't need to change the `encoding`, but it stays there for legacy reasons.
    """
    from math import pi, sqrt
    from base64 import b64decode
    from numpy import random as npr

    def decode_line(line:bytes, r:npr.RandomState):
        encode_64 = r.randint(2, 5)
        line_bytes = bytearray("", "utf-8")
        for byte in line:
            if byte != 10:
                line_bytes.append(byte - r.randint(-32, 134))
        line_enc = line_bytes.decode("utf-8")
        line_enc = line_enc.encode(encoding)
        for _ in range(encode_64):
            line_enc = b64decode(line_enc)
        return line_enc.decode(encoding)

    # get version
    rr = npr.RandomState(int(sqrt((save_num * pi)**7.42 * (3853.587 + save_num * pi)) % 2**32))
    with open(f'{save_name.replace("*", str(save_num))}.{save_ext}', "rb") as f:
        version = int(decode_line(f.readline(), rr))
        seed_num = float(decode_line(f.readline(), rr))
    # decode
    with open(f'{save_name.replace("*", str(save_num))}.{save_ext}', "rb") as f:
        lines = f.readlines()
    lis:list[str] = []
    if version == 4:
        from datetime import datetime
        n = datetime.now()
        seed_num *= (n.year + n.month + n.day)
    elif version < 2 or version > 4:
        seed_num = sqrt((save_num * pi)**7.42 * (3853.587 + save_num * pi))
    seed = npr.RandomState(int(seed_num % 2**32))
    for x in range(2, len(lines)):
        if decode_until > -1 and x >= decode_until + 2:
            break
        lis.append(decode_line(lines[x], seed))    
    return lis