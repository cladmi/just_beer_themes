#! /usr/bin/env python

import os

OUT = "out.html"
THEMES_DIR = 'soirees'

CSS = '''<style media="screen" type="text/css">

td.first {
    width: 10px;
    white-space: nowrap;
}

table {
    margin-left: auto;
    margin-right: auto;
}

</style>
'''


def themes_files(themes_dir):
    files = sorted(os.listdir(themes_dir), key=int, reverse=True)
    files_path = [os.path.join(themes_dir, f) for f in files]
    return files_path


def extract_themes(theme_file):
    themes_list = []
    with open(theme_file) as theme_f:
        for line in theme_f:
            theme_date, theme = line.strip().split(' - ', 1)
            themes_list.append((theme_date, theme))
    return themes_list


def themes_dict(files_list):
    themes = {}
    for theme_file in files_list:
        year = int(os.path.basename(theme_file))
        themes[year] = extract_themes(theme_file)
    return themes


def html_table_from_list(year, theme_list, style):
    out_str = ''

    _theme_line = '<tr {style}><td>{date}</td><td>&nbsp;&nbsp;</td><td>{theme}</td></tr>\n'

    out_str += '<tr {style}><th colspan=3><h1>{year}</h1></th></tr>\n'.format(year=year, style=style)
    for theme_date, theme in theme_list:
        out_str += _theme_line.format(date=theme_date, theme=theme, style=style)
    out_str += '<tr></tr>\n'

    return out_str


def html_from_dict(themes_dict):
    out_str = ''
    out_str += '<html>\n'
    out_str += '<meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n'

    out_str += '<head>\n'
    out_str += CSS
    out_str += '</head>\n'

    out_str += '<body>\n'

    out_str += '<table>\n'
    for num, year in enumerate(sorted(themes_dict.keys(), reverse=True), start=-len(themes_dict) + 1):


        if num == -1:
            style = 'style="color:Gray"'
        elif num == 0:
            style = 'style="color:Silver"'
        else:
            style = 'style="color:Black"'

        print("num %d" % num)
        out_str += html_table_from_list(year, themes_dict[year], style)
        out_str += '\n'

    out_str += '</table>\n'

    out_str += '</body>\n'
    out_str += '</html>\n'
    return out_str
        
        
    

def main():
    themes = themes_dict(themes_files(THEMES_DIR))
    # print(themes)
    html = html_from_dict(themes)
    with open(OUT, 'w') as outfile:
        outfile.write(html)


if __name__ == '__main__':
    main()


