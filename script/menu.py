#!/usr/bin/env python
# coding=utf-8
import sys, re, os
import codecs

reload(sys)
sys.setdefaultencoding('utf8')


def main():
    dirname = 'frontend'
    # 目标文件夹和过滤配置
    target_dir = '../{0}/'.format(dirname)
    filter_dir = ['css', 'js', 'tpl']
    filter_list = []
    for name in filter_dir:
        filter_list.append('({0}\/{1})'.format(dirname, name))
    filter_pattern = '|'.join(filter_list)

    result = get_res(target_dir, filter_pattern)
    fill_menu(result)


# 生成html结构并填充到index.html里边
def fill_menu(result):
    str_cont = ''
    for key in result:
        list = result[key]
        str_li = ''
        idx = 1
        for item in list:
            str_li += '<li><a href="{0}">{1}. {2}</a></li>'.format(item['href'], idx, item['title'])
            idx += 1
        str_ul = '<ul class="menu">{0}</ul>'.format(str_li)
        str_cont += '<h2>{0}</h2>{1}'.format(key, str_ul)

    full_path = os.path.abspath('../index.html')
    f = open(full_path, 'r')
    html = f.read()
    f.close()
    res = re.sub('<div\s+class="list"\s{0,}>[\s\S]+</div>','<div class="list">{0}</div>'.format(str_cont), html)

    with codecs.open(full_path, 'w+', 'utf-8') as out:
        out.write(res)


# 获取结果对象
def get_res(target_dir, filter_pattern):
    result = {}
    for root, dirs, files in os.walk(target_dir):
        for file_item in files:
            part_path = root + r'/' + str(file_item)
            if re.search(filter_pattern, root) is not None:
                continue
            if re.search(r'\.html$', part_path) is None:
                continue

            full_path = os.path.abspath(part_path)
            title = get_title(full_path)
            # a的href
            href = os.path.normpath(part_path)
            href = re.sub(r'^\.\.', r'.', href)
            href = re.sub(r'\\', r'/', href)
            ress = re.search(r'frontend/([\w\d_-]+)/', href)
            # if ress is None:
            group = str(ress.group(1))
            obj = {
                'path': full_path,
                'title': title,
                'href': href,
                'group': group
            }
            if result.has_key(group):
                result[group].append(obj)
            else:
                result[group] = [obj]
    return result


# 获取标题内容
def get_title(full_path):
    f = open(full_path, 'r')
    html = f.read()
    f.close()

    gps = re.search(r'<title>([\s\S]*)<\/title>', html)
    if gps is None:
        print(full_path, '没有匹配到title')

    title = gps.group(1)
    title = re.sub(r'(^\s+)|(\s+$)', '', title)
    return title


# 获取脚本文件的当前路径，不包括文件名  E:\python
def get_cur_path():
    # 获取脚本路径
    path = sys.path[0]
    # 判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)


if __name__ == "__main__":
    main()
