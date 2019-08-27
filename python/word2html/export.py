#!/usr/bin/env python
# coding=utf-8
from win32com import client as wc
import re, time, sys
import codecs
import chardet

reload(sys)
sys.setdefaultencoding('utf8')

'''
参数1：word文档地址
参数2：格式化好的html临时地址
'''


def main(args):
    docPath = args[1]
    exportPath = args[2]
    htmlPath = args[3]

    html = wordToHtml(docPath, exportPath)
    res = formatHtml(html)
    saveFile(res, htmlPath)


# 保存格式化好的文件
def saveFile(res, htmlPath):
    with codecs.open(htmlPath, 'w+', 'utf-8') as out:
        out.write(res)


# docPath - word 文档地址   exportPath - 导出的 html 地址
def wordToHtml(docPath, exportPath):
    try:
        word = wc.Dispatch('Word.Application')
        doc = word.Documents.Open(docPath)
        doc.SaveAs(exportPath, 10)
    finally:
        if ('doc' in dir()) and doc.Close:
            doc.Close()
        if ('word' in dir()) and word.Quit:
            word.Quit()

    f = open(exportPath, 'r')
    str = f.read()  # f = codecs.open(originalPath, 'r', 'gb2312')
    f.close()
    return str


# 格式化html
# res - 导出的 html
def formatHtml(res):
    res = re.sub(r'charset=[\w\d\-]+', 'charset=utf-8', res)

    curCode = chardet.detect(res)['encoding']
    try:
        res = res.decode(curCode)
    except UnicodeDecodeError:
        # charsetList = ['gbk', 'ansii', 'big5']
        res = res.decode('gbk')

    head = r'''
            <title></title>
            <meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,minimum-scale=1.0,user-scalable=no">
            <meta charset="utf-8">  
            <link rel="stylesheet" href="https://ashita.top/custom.css">
            <script src="https://ashita.top/custom.js" type="text/javascript"></script>
            '''
    # 去除默认生成的 style 标签
    res = re.sub(r'<style>[\s\S]*<\/style>', head, res)
    res = re.sub(curCode, r'utf-8', res)  # 改编码

    # 去掉行间样式 style
    res = re.sub(u'style=[\w\d;\-_.\.\s;,:#\"\'%\u4e00-\u9fa5]+>', '>', res)

    # 添加title标签
    searchObj = re.search(u'(MsoTitle|MsoSubtitle)[\'\"<>=\s\d\w]+([\u4e00-\u9fa5\d]+)', res, re.I | re.M)
    if (searchObj):
        title = searchObj.group(2)
        res = re.sub(r'<title></title>', '<title>{0}</title>'.format(title), res)

    # 格式化 class
    res = re.sub(r'class=WordSection1', r'', res)
    res = re.sub(r'MsoTitle', r'title', res)
    res = re.sub(r'MsoSubtitle', r'title', res)
    res = re.sub(r'MsoNormal', r'normal', res)
    res = re.sub(r'MsoListParagraph', r'graph', res)
    res = re.sub(r'class=[\'\"]?title[\'\"]?', r'class=title id=title', res)

    # 去属性
    res = re.sub(r'lang=[\w-]+', r'', res)  # 去lang属性
    res = re.sub(r'align=left', '', res)  # align 属性
    res = re.sub(r'<body[\s\d\w=\'\"#\(\)\.\:\\/;,-]+>', '<body>', res)  # body 上的 vlink 和 link 属性

    # table 处理
    res = re.sub(r'<table[\s\d\w=\'\"#\(\)\.\:\\/;,-]+>', '<table cellspacing="1" cellpadding="1">', res)  # table去属性
    res = re.sub(r'<td([\s\d\w=\'\"#\(\)\.\:\\/;,-]+)>', filterTdAttr, res)  # 处理td的属性，rowspan、colspan、valign
    # if re.search(r'(rowspan)|(colspan)', res):
    # res = re.sub(r'<td[\s\d\w=\'\"#\(\)\.\:\\/;,-]+>', '<td>', res)  # td 去所有属性

    # a链接target 改为"_self" 以及 添加 target="_self"
    res = re.sub(r'(<a[\s\d\w\"\'=#\(\)\.\:\\/;,-]+)(target=[\s\d\w\"\'=#\(\)\.\:\\/;,-]+)(>|\s)?',
                 filterAtag, res)
    res = re.sub(r'(<a[\s\d\w\"\'=#\(\)\.\:\\/;,-]+)(href=[\s\d\w\"\'#\(\)\.\:\\/;,-]+)>',
                 filterAtag1, res)  # 添加target='_self'

    # 去标签 < meta name = Generatorcontent = "Microsoft Word 14 (filtered)" >
    res = re.sub(r'<meta\s+name=Generator[\w\d\s=\'\"()]+>', r'', res)  # 标签结尾的空格

    # 去空 - 格式化
    res = re.sub(r'&nbsp;', r'', res)  # 去空格
    res = re.sub(r'\s+', r' ', res)  # 多个空格合并成一个
    res = re.sub(r'\s+>', r'>', res)  # 标签结尾的空格
    res = re.sub(r'<span>\s{0,}</span>', r'', res)  # 空的span标签
    res = re.sub(r'<p[\s\w\d=\"\']{0,}>\s{0,}</p>', r'<p class="pb20"></p>', res)  # 插入空行，控制间距
    res = re.sub(r'>\s+<', r'><', res)  # 去除标签之间的空格

    # 去掉批注
    res = re.sub(r'<div><hr\s+class=msocomoff[\s\S]+</body>', '</body>', res)
    res = re.sub(r'<a[\s\d\w=\'\"#\(\)\.\:\\/;,-]+>\[[\w\d]+\]</a>', '', res)

    # 动态参数
    res = re.sub(r'\{\{([\w\d]+)\}\}', createParams, res)

    # 给body下的>div添加class
    res = re.sub(r'<body><div>', '<body><div class="jm-protocol">', res)

    res = res.encode('utf-8')
    return res


# 处理表格td的rowspan colspan
def filterTdAttr(matched):
    if (type(matched) == type(None) or type(matched.groups()) == type(None) or (len(matched.groups()) == 0)):
        return ''
    res = ''
    str = matched.group(1)
    res += filterTdCommon(r'rowspan=(\d+)', str, 'rowspan')
    res += filterTdCommon(r'colspan=(\d+)', str, 'colspan')
    res += filterTdCommon(r'valign=(\w+)', str, 'valign')

    # mts = re.search(r'rowspan=(\d+)', str)
    # if (type(mts) != type(None) and type(mts.groups()) != type(None) and (len(mts.groups()) > 0)):
    #     num = mts.group(1)
    #     res += ' rowspan="{0}" '.format(num)
    #
    # mts = re.search(r'colspan=(\d+)', str)
    # if (type(mts) != type(None) and type(mts.groups()) != type(None) and (len(mts.groups()) > 0)):
    #     num = mts.group(1)
    #     res += ' colspan="{0}" '.format(num)

    return '<td {0}>'.format(res)


# 过滤表格属性公共函数
def filterTdCommon(regStr, str, attr):
    res = ''
    mts = re.search(regStr, str)
    if (type(mts) != type(None) and type(mts.groups()) != type(None) and (len(mts.groups()) > 0)):
        num = mts.group(1)
        res += ' {0}="{1}" '.format(attr, num)
    return res


# A 标签属性过滤
def filterAtag(matched):
    mLen = len(matched.groups())
    if mLen < 3:
        print('error: ', matched.group(0))
        return matched.group(0)
    # original = matched.group(0)
    prefix = matched.group(1)
    stuff = matched.group(3)
    return '{0}{1}{2}'.format(prefix, ' target="_self" ', stuff)


# A 标签属性过滤1
def filterAtag1(matched):
    mLen = len(matched.groups())
    if mLen < 2:
        print('error: ', matched.group(0))
        return matched.group(0)
    prefix = matched.group(1)
    href = matched.group(2)
    return '{0}{1}{2}'.format(prefix, href, ' target="_self">')


# 创建参数
def createParams(matched):
    key = matched.group(1)
    return '<span class="holder holder-{0}"></span>'.format(key)


def init():
    debugEnv = 1
    # debugEnv = 0
    args = sys.argv

    if debugEnv == 0:
        args[1] = r'E:\Temp\testDoc\pizhu.doc'

    argLen = len(args)
    if (argLen < 1):
        sys.exit(u'请传入文件路径')
    else:
        original = args[1]
        args.append(re.sub('\.docx?$', '.html', re.sub(r'\\doc\\', r'\\export\\', original)))
        args.append(re.sub('\.docx?$', '.html', re.sub(r'\\doc\\', r'\\format\\', original)))
        main(args)

    print(args)
    quit(100)


if __name__ == "__main__":
    init()
