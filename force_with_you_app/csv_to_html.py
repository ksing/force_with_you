import csv


def csv_html_converter(table):
    html_code = '<div class="table-responsive">\n'
    title = ' '.join(table.readline().strip().split(',')).strip()
    html_code += '\t<h5 class="text-center">{}</h5>\n'.format(title)
    header = table.readline().strip().split(',')
    html_code += '''\t<table class="table table-hover table-bordered">
\t\t<thead>
\t\t\t<tr>
'''
    for headings in header:
        html_code += '\t\t\t\t<th><strong>{}</strong></th>\n'.format(headings)
    html_code += '''\t\t\t</tr>
\t\t</thead>
\t\t<tbody>
'''
    csvreader = csv.reader(table, delimiter=',', quotechar='"')
    for row in csvreader:
        html_code += '\t\t\t<tr>\n'
        for value in row:
            html_code += '\t\t\t\t<td class="text-left">{}</td>\n'.format(value)
        html_code += '\t\t\t</tr>\n'

    html_code += '''\t\t</tbody>
    \t</table>
    </div>
    '''

    return html_code