import functions_framework
import json
import csv
import io

@functions_framework.http
def json_to_csv(request):
    """Convert JSON data to CSV format with | separator and ~ enclosure for ITEM_DESC, 
    with an optional parameter to include/exclude headers (default: yes)."""
    try:
        # Read input JSON
        request_body = request.get_data(as_text=True)
        data = json.loads(request_body) if request_body else {}

        if "processed_records" not in data:
            return "Invalid input: Expected 'processed_records' key", 400

        records = data["processed_records"]

        if not records:
            return "Invalid input: 'processed_records' should not be empty", 400

        # Get optional include_header parameter (default is 'yes')
        include_header = request.args.get("include_header", "yes").lower()

        # Define CSV column headers
        csv_headers = list(records[0].keys())

        # Convert JSON to CSV in-memory
        output = io.StringIO()
        csv_writer = csv.writer(output, delimiter='|', escapechar='\\', quoting=csv.QUOTE_NONE)

        # Write headers if include_header is not 'no'
        if include_header != "no":
            csv_writer.writerow(csv_headers)

        # Convert records using list comprehension
        csv_writer.writerows([
            [f"~{record[col]}~" if col == "ITEM_DESC" else record.get(col, "") for col in csv_headers]
            for record in records
        ])

        # Return CSV response
        response = output.getvalue()
        output.close()

        return response, 200, {'Content-Type': 'text/plain; charset=utf-8'}

    except Exception as e:
        return f"Error: {str(e)}", 500
