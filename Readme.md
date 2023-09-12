# World Athletics Scoring Tables PDF to JSON Converter

This Python script reads PDF files from the input directory and extracts all lookup tables, saving them as JSON files in the output directory.

## Scoring Tables Source

The World Athletics Scoring Tables can be downloaded from the [official WA website](https://worldathletics.org/about-iaaf/documents/technical-information) under the **Scoring Tables** tab. The 2022 tables are already included in this repo.

## Prerequisites

Before using this tool, please make sure you have the following prerequisites installed on your system:

- **Java**: You need Java installed on your machine. Make sure your `JAVA_HOME` environment variable is correctly set.

## Installation

1. Clone or download this repository to your local machine.

2. Open your terminal or command prompt and navigate to the project directory.

3. Run the following command to install the required dependencies:
```
pip install -r requirements.txt
```

## Usage

Once you have the prerequisites and dependencies installed, follow these steps to use the PDF to JSON converter:

1. Run the `WA-Scoring-Tables.py` script:
```
python WA-Scoring-Tables.py
```
2. The script will process the PDF files, extract lookup tables, and save them as JSON files in the `output` directory.

3. You can now access the extracted data in JSON format for further use or analysis. The data is structured as ```points['event']['result']``` or ```result['event']['points']```. Events are named exactly as they occur in the input PDF.

4. Keep in mind that not all possible results have a points count associated with them. So when using the points_lookup with a certain result, there might not be an anwser. You'll need to implement finding the closest valid result yourself.

## Contributing

Contributions to this project are welcome. If you encounter any issues or have suggestions for improvements, please open an issue or create a pull request.