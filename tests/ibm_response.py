from ..app.data_extractor import call_ibm_granite

def test_ibm_connection():
    # Sample text to send to IBM Granite
    sample_text = "Test connection with IBM Granite."

    # Call the IBM Granite function
    response = call_ibm_granite(sample_text)

    # Print the response
    print("IBM Granite Response:", response)

if __name__ == "__main__":
    test_ibm_connection()
