#!/usr/bin/env python
# coding=utf-8
from win32com import client as wc
import sys

reload(sys)
sys.setdefaultencoding('utf8')


def main():
    output_path = 'E:/output.html'

    word = wc.Dispatch('Word.Application')
    doc = word.Documents.Open('E:/test.doc')
    doc.SaveAs(output_path, 10)
    doc.Close()
    word.Quit()

    '''
    先要安装 pypiwin32(只支持windows系统)，
    原理：利用win32com接口直接调用office API，处理出来的结果和office word 里面“另存为”一致。
    可以将导出来的html，进行格式化，做一个word文档转html的工具；
    
    SaveAs(output_path, 类型)，详细的类型列表如下：
    wdFormatDocument                    =  0
    wdFormatDocument97                  =  0
    wdFormatDocumentDefault             = 16
    wdFormatDOSText                     =  4
    wdFormatDOSTextLineBreaks           =  5
    wdFormatEncodedText                 =  7
    wdFormatFilteredHTML                = 10
    wdFormatFlatXML                     = 19
    wdFormatFlatXMLMacroEnabled         = 20
    wdFormatFlatXMLTemplate             = 21
    wdFormatFlatXMLTemplateMacroEnabled = 22
    wdFormatHTML                        =  8
    wdFormatPDF                         = 17
    wdFormatRTF                         =  6 
    wdFormatTemplate                    =  1
    wdFormatTemplate97                  =  1
    wdFormatText                        =  2
    wdFormatTextLineBreaks              =  3
    wdFormatUnicodeText                 =  7
    wdFormatWebArchive                  =  9
    wdFormatXML                         = 11
    wdFormatXMLDocument                 = 12
    wdFormatXMLDocumentMacroEnabled     = 13
    wdFormatXMLTemplate                 = 14
    wdFormatXMLTemplateMacroEnabled     = 15
    wdFormatXPS                         = 18
    '''

if __name__ == "__main__":
    main()