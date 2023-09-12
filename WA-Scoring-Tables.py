import tabula
import fitz  # PyMuPDF
import json


def format_data(value):
    try:
        return f'{float(value):.2f}'
    except ValueError:
        return value


def read_pdf(filename: str, output_prefix: str):
    filename = 'input/' + filename
    pdf_document = fitz.open(filename)
    result_lookup = {'men': {}, 'women': {}}
    points_lookup = {'men': {}, 'women': {}}

    # Use tabula.read_pdf to extract tables from the PDF
    for i in range(1, round(pdf_document.page_count)):
        print(f'\nLoading page: {i:3}/{pdf_document.page_count} ({round(100*i/pdf_document.page_count,1):4}%)', end="")
        tables = tabula.read_pdf(filename, pages=i)
        if not tables:
            print('  -  No table on this page', end="")
            continue
        else:
            header = pdf_document.load_page(i-1).get_text().split('\n')[0].strip()  # load_page is 0-indexed, get the page header to determine MEN/WOMEN
            gender = header.split('’')[0].lower()

            df = tables[0]
            if 'Unnamed: 0' in df.columns.tolist():
                df.columns = df.iloc[0]
                df = df.iloc[1:]
            df.set_index('Points', inplace=True)
            data = df.to_dict(orient='dict')

            for key, value in data.items():
                value = {p: format_data(s) for p, s in value.items()}
                if key in result_lookup[gender]:
                    result_lookup[gender][key].update(value)
                else:
                    result_lookup[gender][key] = value
    pdf_document.close()

    # Reverse the table to get the lookup from result to points
    for event_name, event_dict in result_lookup['men'].items():
        points_lookup['men'][event_name] = {v: k for k, v in event_dict.items() if v != '-'}

    with open('output/' + output_prefix + '_men_result_lookup.json', 'w') as json_file:
        json.dump(result_lookup['men'], json_file)
    with open('output/' + output_prefix + '_women_result_lookup.json', 'w') as json_file:
        json.dump(result_lookup['women'], json_file)
    with open('output/' + output_prefix + '_men_points_lookup.json', 'w') as json_file:
        json.dump(points_lookup['men'], json_file)
    with open('output/' + output_prefix + '_women_points_lookup.json', 'w') as json_file:
        json.dump(points_lookup['women'], json_file)


if __name__ == '__main__':
    print('========== Loading Indoor Tables ==========')
    read_pdf('WA-Scoring-Tables-2022-Indoor.pdf', 'indoor')
    print('========== Loading Outdoor Tables ==========')
    read_pdf('WA-Scoring-Tables-2022-Outdoor.pdf', 'outdoor')
