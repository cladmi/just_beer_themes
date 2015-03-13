#! /usr/bin/env python

import os

OUT = "out.html"
THEMES_DIR = 'soirees'

# 2 + space + 8 + space + 4
    #white-space: nowrap;

CSS = '''<style type="text/css">

h1 {
    font-size: 5em;
}
h2 {
    font-size: 3em;
}

td {
    text-align: left;
}

.parent {
    width: 100%;
    height: 100%;
    display: table;
    text-align: center;
}

.parent > .child {
    display: table-cell;
    vertical-align: middle;
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
    out_str += '<table>\n'
    out_str += '<h2 {style}>{year}</h2>\n'.format(year=year, style=style)

    _theme_line = '<tr {style}><td style="min-width: 16em">{date}</td><td>{theme}</td></tr>\n'

    for theme_date, theme in theme_list:
        out_str += _theme_line.format(date=theme_date, theme=theme, style=style)
    out_str += '</table>\n'

    return out_str


def html_from_dict(themes_dict):
    out_str = ''
    out_str += '<html>\n'
    out_str += '<meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n'

    out_str += '<head>\n'
    out_str += CSS
    out_str += '</head>\n'

    out_str += '<body>\n'

    out_str += '<section class="parent">\n'
    out_str += '<div class = "child">\n'
    out_str += '<h1>Just Beer<br/>&<br/>Les thèmes de soirées</h1>\n'
    out_str += '</div>\n'
    out_str += '</section>\n'
    out_str += '\n'

    for num, year in enumerate(sorted(themes_dict.keys(), reverse=True), start=-len(themes_dict) + 1):
        if num == -1:
            style = 'style="color:Gray; text-align:center"'
        elif num == 0:
            style = 'style="color:Silver; text-align:center"'
        else:
            style = 'style="color:Black; text-align:center"'
        out_str += html_table_from_list(year, themes_dict[year], style)
        out_str += '<span style="page-break-after: always"></span>\n'
        out_str += '\n'

    out_str += '<h2 {style}>{year}</h2>\n'.format(
        year=year -1,
	style='style="color:white; text-align:center"')
    out_str += '<span style="page-break-after: always"></span>\n'
    out_str += '\n'

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


