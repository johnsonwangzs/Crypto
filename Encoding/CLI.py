"""
Author：@19373297 WZS
Function：在CLI终端集成的编码/解码程序
    可选功能：使用Huffman编码或解码文件
            使用LZ_78编码或解码文件
            联合使用Huffman和LZ_78编码或解码文件（*）
            返回编码或解码后的文件大小（*）
            返回可能的错误信息（参数错误、文件错误）（*）
"""

import argparse
import os
import time
import Huffman_encode
import Huffman_decode
import LZ78_encode
import LZ78_decode


def encode_in_Huffman(filepara, fin):
    global originSize
    outFileName = filepara + "_encodedByHuffman"
    fout = open(outFileName, "wb")
    print("\nEncoding......Please wait......")
    origTxt = fin.read()
    sortedByte = Huffman_encode.getByteFreq(origTxt, fout)  # 按字节读入，统计频率，按出现次数排序
    if sortedByte is None:
        print("空文件!")
        return outFileName
    rootNode = Huffman_encode.creatHuffTree(sortedByte)  # 构造Huffman树
    Huffman_encode.encodeNode(rootNode, '')  # 给节点编码
    Huffman_encode.encodeTxt(origTxt, fout)  # 给原文编码，并将结果输出到文件
    print("Encoding Succeed!\n")
    print("文件：\"{0}\"的Huffman编码完成！请在同目录的文件：\"{1}\"中查看（可使用WinHex打开）！".format(args.filename, outFileName))
    fout.close()
    return outFileName


def encode_in_LZ78(filepara, fin):
    global originSize
    outFileName = filepara + "_encodedByLZ78"
    fout = open(outFileName, "wb")
    print("\nEncoding......Please wait......")
    origTxt = fin.read()
    flag = LZ78_encode.encode(origTxt, fout)
    if flag == -1:  # 空文件
        return
    print("Encoding Succeed!\n")
    print("文件：\"{0}\"的LZ78编码完成！请在同目录的文件：\"{1}\"中查看（可使用WinHex打开）！".format(args.filename, outFileName))
    fout.close()
    return outFileName


def decode_in_Huffman(filepara, fin):
    global originSize
    outFileName = filepara + "_decodedByHuffman"
    fout = open(outFileName, "wb")
    print("\nDecoding......Please wait......")
    origTxt = fin.read()
    flag = Huffman_decode.decode(origTxt, fout)
    if flag == -1:  # 空文件
        return
    print("Decoding Succeed!\n")
    print("文件：\"{0}\"的Huffman解码完成！请在同目录的文件：\"{1}\"中查看（可使用WinHex打开）！".format(args.filename, outFileName))
    fout.close()
    return outFileName


def decode_in_LZ78(filepara, fin):
    global originSize
    outFileName = filepara + "_decodedByLZ78"
    fout = open(outFileName, "wb")
    print("\nDecoding......Please wait......")
    origTxt = fin.read()
    flag = LZ78_decode.decode(origTxt, fout)
    if flag == -1:  # 空文件
        return
    print("Decoding Succeed!\n")
    print("文件：\"{0}\"的LZ78解码完成！请在同目录的文件：\"{1}\"中查看（可使用WinHex打开）！".format(args.filename, outFileName))
    fout.close()
    return outFileName


def encode_2time(m2, out):
    global originSize
    print("--------------------------------")
    print("联合编码第一阶段已完成，下面进行第二阶段的编码！")
    if m2 in ['LZ78', 'lz78', 'Lz78', 'LZ_78', 'lz_78', 'Lz_78', 'LZ', 'lz', 'Lz', '78']:
        midfin = open(out, "rb")
        outname = encode_in_LZ78(out, midfin)
        nowsize = printFileStat(outname)
        if originSize != 0:
            print("压缩率：current / origin = ", nowsize / originSize)
        print("联合编码第二阶段已完成！")
        midfin.close()
    elif m2 in ['Huffman', 'huffman', 'H', 'h', 'Hu', 'hu', 'Huf', 'huf', 'Huff', 'huff']:
        midfin = open(out, "rb")
        outname = encode_in_Huffman(out, midfin)
        nowsize = printFileStat(outname)
        if originSize != 0:
            print("压缩率：current / origin = ", nowsize / originSize)
        print("联合编码第二阶段已完成！")
        midfin.close()
    else:
        returnBadPara('method')


def decode_2time(m2, out):
    global originSize
    print("--------------------------------")
    print("联合解码第一阶段已完成，下面进行第二阶段的解码！")
    if m2 in ['LZ78', 'lz78', 'Lz78', 'LZ_78', 'lz_78', 'Lz_78', 'LZ', 'lz', 'Lz', '78']:
        midfin = open(out, "rb")
        outname = decode_in_LZ78(out, midfin)
        nowsize = printFileStat(outname)
        if originSize != 0:
            print("压缩率：current / origin = ", nowsize / originSize)
        print("联合解码第二阶段已完成！")
        midfin.close()
    elif m2 in ['Huffman', 'huffman', 'H', 'h', 'Hu', 'hu', 'Huf', 'huf', 'Huff', 'huff']:
        midfin = open(out, "rb")
        outname = decode_in_Huffman(out, midfin)
        nowsize = printFileStat(outname)
        if originSize != 0:
            print("压缩率：current / origin = ", nowsize / originSize)
        print("联合解码第二阶段已完成！")
        midfin.close()
    else:
        returnBadPara('method')


def returnBadPara(para):  # 返回参数错误信息
    if para == 'method':
        print("\nBad input! Some parameters CANNOT be recognized!")
        print("The available value of parameter \'encoding_method\' are: "
              "['Huffman', 'huffman', 'H', 'h', 'Hu', 'hu', 'Huf', 'huf', 'Huff', 'huff'] or "
              "['LZ78', 'lz78', 'Lz78', 'LZ_78', 'lz_78', 'Lz_78', 'LZ', 'lz', 'Lz', '78']")
        print("Please try again!")
    elif para == 'mode':
        print("\nBad input! Some parameters CANNOT be recognized!")
        print("The available value of parameter \'mode\' are: "
              "['en', 'encode', 'encrypt', \"编码\", 'E', 'e', 'En', 'EN', 'Encrypt', 'Encode', 'enc', 'Enc', "
              "'encoding', 'Encoding'] or "
              "['de', 'decode', 'decrypt', \"解码\", 'D', 'd', 'De', 'DE', 'Decrypt', 'Decode', 'dec', 'Dec', "
              "'decoding', 'Decoding']")
        print("Please try again!")


def printFileStat(file_name):
    file_stats = os.stat(file_name)
    print('File Size in Bytes, KiloBytes and MegaBytes are', file_stats.st_size, file_stats.st_size / 1024, file_stats.st_size / (1024 * 1024))
    return file_stats.st_size


if __name__ == '__main__':
    stime = time.perf_counter()
    print("--------欢迎使用！若有疑问请输入参数-h查看使用方法！谢谢！！！--------")
    parser = argparse.ArgumentParser(description='文件编码&解码——可选：[1]Huffman编（解）码。[2]LZ编（解）码。[3]联合编（解）码')
    parser.add_argument('mode', type=str, help='功能选项。要编码文件，请输入\'encode\'或相关字符（串）；'
                                               '要解码文件，请输入\'decode\'或相关字符（串）。')
    parser.add_argument('coding_method_1', type=str,
                        help='编码方法。[1]要以Huffman编码的方式进行操作，请输入\'huffman\'或相关字符（串）；'
                             '[2]要以LZ_78编码的方式进行操作，请输入\'LZ78\'或相关字符（串）。'
                             '[3]要以Huffman和LZ78对同一文件联合依次进行编码，请在此位置输入想要优先使用的编码方法（同[1][2]），然后在可选参数中输入后使用的编码方法。'
                             '[4]要以Huffman和LZ78对同一已编码文件联合依次进行解码，请在此位置输入第一轮解码使用的方法（同[1][2]），然后在可选参数中输入第二轮解码使用的方法。')
    parser.add_argument('-m2', '--coding_method_2', type=str, default='none',
                        help='如果想使用两种方法对同一文件进行编（解）码，请在此可选参数处指定后使用的编码方法（前提是您已在前一必选参数中指定了优先使用的编码方法）。')
    parser.add_argument('filename', type=str, help='文件名。要进行编码或解码的文件的文件名（不需加引号）。')
    args = parser.parse_args()
    print(args)
    with open(args.filename) as file:
        fin = open(args.filename, "rb")  # 根据传入的参数filename定向到文件
    originSize = printFileStat(args.filename)

    # 根据传入的参数mode选择编码或解码模式；根据参数encoding_method选择编码方法为Huffman或LZ78或联合编码
    if args.mode in ['en', 'encode', 'encrypt', "编码", 'E', 'e', 'En', 'EN', 'Encrypt', 'Encode', 'enc', 'Enc',
                     'encoding', 'Encoding']:
        if args.coding_method_1 in ['Huffman', 'huffman', 'H', 'h', 'Hu', 'hu', 'Huf', 'huf', 'Huff', 'huff']:
            out = encode_in_Huffman(args.filename, fin)  # 使用Huffman编码
            if out is not None:
                nowSize = printFileStat(out)
                if originSize != 0:
                    print("压缩率：current / origin = ", nowSize / originSize)
            if args.coding_method_2 != 'none':
                encode_2time(args.coding_method_2, out)
        elif args.coding_method_1 in ['LZ78', 'lz78', 'Lz78', 'LZ_78', 'lz_78', 'Lz_78', 'LZ', 'lz', 'Lz', '78']:
            out = encode_in_LZ78(args.filename, fin)  # 使用LZ78编码
            if out is not None:
                nowSize = printFileStat(out)
                if originSize != 0:
                    print("压缩率：current / origin = ", nowSize / originSize)
            if args.coding_method_2 != 'none':
                encode_2time(args.coding_method_2, out)
        else:
            returnBadPara('method')  # 返回参数错误信息
    elif args.mode in ['de', 'decode', 'decrypt', "解码", 'D', 'd', 'De', 'DE', 'Decrypt', 'Decode', 'dec', 'Dec',
                       'decoding', 'Decoding']:
        if args.coding_method_2 != 'none':
            print("***请注意！如果您选择的已编码文件不是依次按coding_method_1和coding_method_2进行的，那么可能发生错误！***")
        if args.coding_method_1 in ['Huffman', 'huffman', 'H', 'h', 'Hu', 'hu', 'Huf', 'huf', 'Huff', 'huff']:
            out = decode_in_Huffman(args.filename, fin)  # 使用Huffman解码
            if out is not None:
                nowSize = printFileStat(out)
                if originSize != 0:
                    print("压缩率：current / origin = ", nowSize / originSize)
            if args.coding_method_2 != 'none':
                decode_2time(args.coding_method_2, out)
        elif args.coding_method_1 in ['LZ78', 'lz78', 'Lz78', 'LZ_78', 'lz_78', 'Lz_78', 'LZ', 'lz', 'Lz', '78']:
            out = decode_in_LZ78(args.filename, fin)  # 使用LZ78解码
            if out is not None:
                nowSize = printFileStat(out)
                if originSize != 0:
                    print("压缩率：current / origin = ", nowSize / originSize)
            if args.coding_method_2 != 'none':
                decode_2time(args.coding_method_2, out)
        else:
            returnBadPara('method')  # 返回参数错误信息
    else:
        returnBadPara('mode')  # 返回参数错误信息
    fin.close()
    etime = time.perf_counter()
    print("Running Time:", etime - stime)
