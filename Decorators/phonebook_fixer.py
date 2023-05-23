import csv
import re

from logger import logger_decor


@logger_decor
def merge_duplicates(lines, key_column):
    """
    The method merges duplicates by the following rules:
        '' + 'value' => 'value'
        '' + '' => ''
        'value' + 'value' (value = value) => 'value'
        'value1' + 'value2' => 'value1', 'value2'
    :param lines: list of lists with strs: [[str, str, ...],[str, str, ...], ...]
    :param key_column: The key column index (must be unique). Duplicates are merged
                       in respect of this column.
    """
    def merge_row(base_row, new_row):
        for j in range(len(base_row)):
            if base_row[j].casefold() != new_row[j].casefold():
                base_row[j] += new_row[j]
            if not base_row[j]:
                base_row[j] = new_row[j]
        return base_row

    merged_data = {}
    for line in lines:
        merged_data[line[key_column]] = merge_row(merged_data.get(line[key_column],
                                                                  ['' for _ in range(len(line))]),
                                                  line)
    lines = list(merged_data.values())
    return lines


if __name__ == '__main__':
    with open('phonebook_raw.csv', 'rt', encoding='UTF-8') as f:
        data = list(csv.reader(f, delimiter=','))
        headers, rows = data[0], data[1:]

    rows[3].pop()    # fix csv (line 5 has 1 extra value(8 values against 7 headers)

    # Spread the names among the first 3 columns
    pattern = r'^(\w+)\s?,?(\w+)\s?,?(\w*),?,,(.*)'
    substitution = r'\1,\2,\3,\4'
    for i in range(len(rows)):
        rows[i] = re.sub(pattern, substitution, ','.join(rows[i])).split(',')
        if len(rows[i]) < len(headers):
            rows[i].insert(3, '')

    # Join duplicates
    rows = merge_duplicates(rows, 0)

    # Format phones as per "+7(999)999-99-99 доб.9999"
    for row in rows:
        if 'доб.' in row[5]:
            pattern = r"(\+7|8)\s?\(?(\d{3})\)?\s?\-?(\d{3})\s?\-?(\d{2})\s?\-?(\d{2})\s?\(?(?:доб.)?\s?(\d{4})?\)?"
            row[5] = re.sub(pattern, r'+7(\2)\3-\4-\5 доб.\6', row[5])
        else:
            pattern = r"(\+7|8)\s?\(?(\d{3})\)?\s?\-?(\d{3})\s?\-?(\d{2})\s?\-?(\d{2})"
            row[5] = re.sub(pattern, r'+7(\2)\3-\4-\5', row[5])
            
    rows.insert(0, headers)
    with open("phonebook.csv", "w") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(rows)
            
