import tabula
import fitz  # PyMuPDF
import json


# Try if input can be cast to float, if so, return the value as string using 2 decimal places.
# Else return the raw value as string
def format_data(value):
    try:
        return f'{float(value):.2f}'
    except ValueError:
        return str(value)


def read_pdf(filename: str, output_prefix: str):
    # Read PDF from input directory
    filename = 'input/' + filename
    pdf_document = fitz.open(filename)
    result_lookup = {'men': {}, 'women': {}}
    points_lookup = {'men': {}, 'women': {}}

    # Use tabula.read_pdf to extract tables from the PDF
    for i in range(1, round(pdf_document.page_count)):
        print(f'\nLoading page: {i:3}/{pdf_document.page_count} ({round(100*i/pdf_document.page_count,1):4}%)', end="")
        tables = tabula.read_pdf(filename, pages=i)

        # Some pages don't contain scoring tables, they can be skipped:
        if not tables:
            print('  -  No table on this page', end="")
            continue
        else:
            # Need to check the first line of text to check if the table is for Men or Women
            header = pdf_document.load_page(i-1).get_text().split('\n')[0].strip()  # load_page is 0-indexed, get the page header to determine MEN/WOMEN
            gender = header.split('’')[0].lower()

            df = tables[0]
            # Some tables contain an extra 'Unnamed: 0' row, they are removed
            if 'Unnamed: 0' in df.columns.tolist():
                df.columns = df.iloc[0]
                df = df.iloc[1:]
            df.set_index('Points', inplace=True)  # Set the Points column as index
            data = df.to_dict(orient='dict')  # Convert to dictionary

            # Loop through every event
            for key, value in data.items():
                # Format the value of every row to string
                value = {p: format_data(s) for p, s in value.items()}

                # Add the values to the existing table
                if key in result_lookup[gender]:
                    result_lookup[gender][key].update(value)
                else:
                    result_lookup[gender][key] = value
    pdf_document.close()

    for gender in result_lookup.keys():
        # Reverse the table to get the lookup from result to points
        for event_name, event_dict in result_lookup[gender].items():
            points_lookup[gender][event_name] = {v: k for k, v in event_dict.items() if v != '-'}

        # Export the files to output directory
        with open('output/' + output_prefix + '_'+gender+'_result_lookup.json', 'w') as json_file:
            json.dump(result_lookup[gender], json_file)
        with open('output/' + output_prefix + '_'+gender+'_points_lookup.json', 'w') as json_file:
            json.dump(points_lookup[gender], json_file)


if __name__ == '__main__':
    print('\n\n========== Loading Tables ==========\n\n')
    read_pdf('WA-Scoring-Tables-2025.pdf', '2025')
