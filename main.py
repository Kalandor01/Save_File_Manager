import numpy as np
import os
# import struct


def imput(ask="Num: "):
    while True:
        try: return int(input(ask))
        except ValueError: print("Not number!")


def encode_save(save_file=[], save_num=1, save_name="save*", save_ext="sav"):
    """""""""""""""
    creates a file that has been encoded, from a list
    """""""""
    f = open(f'{save_name.replace("*", str(save_num))}.{save_ext}', "wb")
    r = np.random.RandomState(int(save_num * np.pi * 719))
    for x in range(len(save_file)):
        line_bytes = bytearray(save_file[x], encoding="windows-1250")
        line_bytes_enc = bytearray("", encoding="windows-1250")
        for byte in line_bytes:
            line_bytes_enc.append((byte + r.randint(1, 255)) % 256)
        f.write(line_bytes_enc)
        if x != len(save_file) - 1:
            f.write(bytearray("\n", encoding="windows-1250"))
    f.close()


def decode_save(save_num=1, save_name="save*", save_ext="sav"):
    """""""""""""""
    returns a list of strings, decoded fron the encoded file
    """""""""
    f = open(f'{save_name.replace("*", str(save_num))}.{save_ext}', "rb")
    lines = f.readlines()
    f.close()
    r = np.random.RandomState(int(save_num * np.pi * 719))
    lis = []
    for line_bytes_enc in lines:
        line_bytes = bytearray("", encoding="windows-1250")
        # print("\n\n" + str(line_bytes_enc))
        for byte in line_bytes_enc:
            # print(byte, end=", ")
            if byte != 10:
                line_bytes.append((byte - r.randint(1, 255)) % 256)
        line = line_bytes.decode("windows-1250")
        lis.append(line)
    return lis


def file_reader(max_saves=5, write_out=True, save_name="save*", save_ext="sav"):
    """""""""""""""
    returns encripted data from all save files with the save file number
    """""""""
    file_data = []
    file_num = 0
    if write_out:
        print("\n")
    while max_saves > file_num:
        file_num += 1
        try:
            f = open(f'{save_name.replace("*", str(file_num))}.{save_ext}', "r")
            f.close()
        except FileNotFoundError:
            pass
        else:
            data = decode_save(file_num, "save*", "sav")
            file_data.append([file_num, data])
            if write_out:
                print(f"Save File {file_num}:")
                print(data)
                print("\n")
    return file_data


def manage_saves(file_data = [], max_saves=5, save_name="save*", save_ext="sav"):
    """""""""""""""
    allows the user to pick between creating a new save, loading an old save and deleteing a save
    returns the option the user selected:
    [0, x] = load, into x slot
    [1, x] = new file, into x slot
    [-1] = deleted file
    """""""""
    manage_exit = False
    while not manage_exit:
        if len(file_data):
            # get file range
            file_num = 0
            min_file_num = file_data[0][0]
            for data in file_data:
                if data[0] > file_num:
                    file_num = data[0]
                if data[0] < min_file_num:
                    min_file_num = data[0]
            option = imput(f"Select an option: -1: delete mode, 0: new file, {min_file_num}-{file_num}: load file: ")
            # delete
            if option == -1:
                option = imput(f"Select an option: 0: back, {min_file_num}-{file_num}: delete file: ")
                if min_file_num <= option <= file_num:
                    sure = input(f"Are you sure you want to remove Save file {option}?(Y/N): ")
                    if sure.upper() == "Y":
                        os.remove(f'{save_name.replace("*", str(option))}.{save_ext}')
                        manage_exit = True
            # new file
            elif option == 0:
                new_slot = 1
                for data in file_data:
                    if data[0] == new_slot:
                        new_slot += 1
                if new_slot <= max_saves:
                    return [1, new_slot]
                else:
                    fff = input(f"No empty save files! Delete a file to continue!")
            # load
            else:
                for data in file_data:
                    if data[0] == option:
                        return [0, option]
                print(f"Save file {option} doesn't exist!")
        else:
            fff = input(f"No save files!")
            return [1, 1]
    return [-1]

def default_run(write_out=True, max_saves=5, save_name="save*", save_ext="sav"):
    save = ["bro yes dude 42069", "éáőúűüó", "hello"]
    save_new = ["loading lol 69", "űűűűűűűűűűűűűűűűűűűűűűááááááááááááűáűáűááááááááá", "xd"]
    encode_save(save, 1)
    encode_save(save, 2)
    encode_save(save, 4)
    options_status = True
    while options_status:
        datas = file_reader(max_saves, write_out, save_name, save_ext)
        status = manage_saves(datas)
        if status[0] == 1 or status[0] == 0:
            options_status = False
    if status[0] == 1:
        print(f"NEW GAME!!! in {status[1]}")
        encode_save(save_new, status[1])
    elif status[0] == 0:
        print(f"LOADING SAVE {status[1]}!!!")

default_run()

# some stuff can turn into \n = 10 = \xA0

# test_line = ['0123456789ABCDEFNULSOHSTXETXEOTENQACKBELBSHTLFVTFFCRSOSIDLEDC1DC2DC3DC4NAKSYNETBCANEMSUBESCFSGSRSUS SP !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~DEL€	‚	„…†‡	‰Š‹ŚŤŽŹ	‘’“”•–—	™š›śťžźNBSPˇ˘Ł¤Ą¦§¨©Ş«¬SHY®Ż°±˛ł´µ¶·¸ąş»Ľ˝ľżŔÁÂĂÄĹĆÇČÉĘËĚÍÎĎĐŃŇÓÔŐÖ×ŘŮÚŰÜÝŢßŕáâăäĺćçčéęëěíîďđńňóôőö÷řůúűüýţ˙']
# save_new = ["loading lol 69", "űűűűűűűűűűűűűűűűűűűűűűááááááááááááűáűáűááááááááá", "xd"]
# encode_save(save_new, 3)
# print(decode_save(3))