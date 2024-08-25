# VC Pitch Simulator

Welcome to the VC Pitch Simulator! This project helps you analyze startup pitch decks and extract valuable insights using IBM's Granite model.

## Features

- **File Upload**: Upload your startup pitch deck in PDF, DOCX, or TXT format.
- **Text Extraction**: Extract text from the uploaded pitch deck.
- **Data Extraction**: Use pre-defined prompts to extract specific data points from the text.
- **User Prompts**: Prompt the user for any missing information.
- **Metrics Calculation**: Calculate important startup metrics.
- **Report Generation**: Generate a comprehensive VC analysis report.

## How to Use

1. **Upload a File**: Upload your pitch deck file using the file uploader.
2. **Extract Data**: The app will process the file and extract text.
3. **Analyze Data**: The extracted text will be analyzed to extract specific data points.
4. **Complete Information**: Provide any missing information prompted by the app.
5. **Generate Report**: View the generated VC analysis report.

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/mjdyibrahim/VC-Pitch-Simulator.git
   cd VC-Pitch-Simulator
   ```

2. Create a virtual environment and activate it:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Run the Streamlit app:
   ```sh
   streamlit run app/main.py
   ```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License.
