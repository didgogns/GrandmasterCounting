from tabulate import tabulate


def html_table(table, row, col):
    assert(len(table) + 1 == len(row))
    assert(len(table[0]) == len(col))
    attached_table = [[a] + b for a, b in zip(row[1:], table)]
    return tabulate(attached_table, [row[0]] + col, tablefmt='html')\
        .replace('<table>', '<table style="border:1px solid black;border-collapse:collapse;">')\
        .replace('<th>', '<th style="border:1px solid black;border-collapse:collapse;">')\
        .replace('<td>', '<td style="border:1px solid black;border-collapse:collapse;width:100px">')\
        + '<br><br>'


def round_per(val, n):
    return str(round(val / n * 100, 2)) + '%'
