# Pure API Person ID Classification Migrator

This Python script automates the process of:
1. Fetching data from the Pure API using GET requests for a list of UUIDs.
2. Modifying the Person ID classification in the response based on conditions.
3. Sending the modified payload back to the Pure API using PUT requests.

## Features
- Handles multiple UUIDs from an Excel file.
- Only modifies matching identifiers based on specified conditions.
- Logs all operations, including successful updates and errors, for auditing and debugging purposes.

## Requirements
- Python 3.7 or later
- Libraries:
  - `requests`
  - `pandas`
  - `openpyxl`

Install the required libraries using:
```bash
pip install requests pandas openpyxl
```

## How to Use
1. Prepare an Excel file with the following columns:
   - `UUID`: The unique identifier for the person.
   - `Medarbejder id`: The identifier to match in the API response.

2. Update the script configuration:
   - Replace `myapikey` with your actual API key.
   - Specify the path to your Excel file.

3. Run the script:
```bash
python personID_classification_migrator.py
```

4. Logs will be generated in the same directory as the script, with a timestamped filename (e.g., `api_update_log_YYYYMMDD_HHMMSS.log`).

## Error Handling
- **503 Errors**: Temporary service issues. Retry after some time.
- **500 Errors**: Internal server issues.
- **404 Errors**: UUID not found. Verify the data in the Excel file.
- **400 Errors**: Validation issues. Review the log file for details and ensure data consistency.

## Example Log Entry
```plaintext
2024-11-27 12:34:56 - INFO - Processing UUID: 32b6ee1a-6340-4fc4-be50-ec9acab429be with Medarbejder ID: m7rg
2024-11-27 12:34:56 - INFO - Original Identifiers for UUID 32b6ee1a-6340-4fc4-be50-ec9acab429be: [{"typeDiscriminator": "ClassifiedId", "id": "m7rg", "type": {"uri": "/dk/atira/pure/person/personsources/employee", "term": {"en_GB": "Employee ID", "da_DK": "Medarbejder id"}}}]
2024-11-27 12:34:56 - INFO - Updating identifier for UUID: 32b6ee1a-6340-4fc4-be50-ec9acab429be, Original URI: /dk/atira/pure/person/personsources/employee, New URI: /dk/atira/pure/person/personsources/aauh_employee_id
2024-11-27 12:34:56 - INFO - Successfully updated UUID: 32b6ee1a-6340-4fc4-be50-ec9acab429be
```

## Customization
- Modify the API endpoint, headers, or logic in the script to suit your requirements.
- Adjust logging levels or format if needed.

## License
This script is provided "as is" without warranty of any kind. Use at your own risk.
