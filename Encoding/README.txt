--------说明--------
建议将此文件夹目录按照“名称”排序，以获得最佳查看体验。
谢谢！



--------代码文件--------
CLI.py：集成所有功能的CLI。对于所有测试，都请通过在PowerShell/cmd中运行此文件来进行
Huffman_encode.py：Huffman编码代码
Huffman_decode.py：Huffman解码代码
LZ78_encode.py：LZ78编码代码
LZ78_decode.py：LZ78解码代码



--------测试文件--------
待编码文件：
	pictest1.jpeg：创作的3840*2160像素的jpeg图片
	pictest2.bmp：创作的3840*2160像素的bmp图片
	testfile1：给定的测试文件
	EnglishStory.txt：一篇英文小说
	SingleByteTest.txt：单一字节值文件
	EmptyByteTest.txt：空文件
	

待解码文件：
	分别使用Huffman、LZ78以及联合使用二者对pictest1.jpeg编码后的文件：
	pictest1.jpeg_encodedByHuffman
	pictest1.jpeg_encodedByLZ78
	pictest1.jpeg_encodedByLZ78_encodedByHuffman

	分别使用Huffman、LZ78以及联合使用二者对pictest2.bmp编码后的文件：
	pictest2.bmp_encodedByHuffman
	pictest2.bmp_encodedByLZ78
	pictest2.bmp_encodedByLZ78_encodedByHuffman

	分别使用Huffman、LZ78以及联合使用二者对EnglishStory.txt编码后的文件：
	EnglishStory.txt_encodedByHuffman
	EnglishStory.txt_encodedByLZ78
	EnglishStory.txt_encodedByLZ78_encodedByHuffman

	分别使用Huffman、LZ78以及联合使用二者对testfile1编码后的文件：
	testfile1_encodedByHuffman
	testfile1_encodedByLZ78
	testfile1_encodedByLZ78_encodedByHuffman

	分别使用Huffman、LZ78对LOL.exe编码后的文件：
	LOL.exe_encodedByHuffman
	LOL.exe_encodedByLZ78

	以及任何非本程序编码的待解码文件，用以测试鲁棒性