import functions_framework
import json

def format_date(date_string):
    """Formats a date from YYYY-MM-DD to DD/MM/YYYY."""
    if not date_string or date_string.lower() == "null":
        return ''
    parts = date_string.split('-')
    if len(parts) == 3:
        return f"{parts[2]}/{parts[1]}/{parts[0]}"
    return ''

def process_lambda(itemReference, itemMagasin):
    """Generates jsonTarifs for each reference-magasin combination."""
    return {
        "ITEM": str(itemReference.get("item", "")),
        "STORE": str(itemMagasin.get("code", "")),  # Store code from magasins
        "PRICE_TYPE": str(itemReference.get("price_type", "")),
        "STARTDATE": format_date(itemReference.get("start_date", "")),
        "ENDDATE": format_date(itemReference.get("end_date", "")),
        "PRICE": round(float(itemReference.get("pv_ttc", 0)) * 100),
        "PROMOTIONID": str(itemReference.get("promotion_id", "")),
        "ACTION": str(itemReference.get("action", ""))
    }

@functions_framework.http
def process_tarifs(request):
    """Cloud Function that processes all magasins for each reference."""
    try:
        # Read and parse JSON input
        request_json = request.get_json(silent=True)
        if not request_json:
            return json.dumps({"error": "Invalid JSON"}), 400, {"Content-Type": "application/json"}

        magasins = request_json.get("magasins", [])
        references = request_json.get("references", [])

        liste_tarifs = []

        # Loop through each reference
        for itemReference in references:
            # Iterate through all magasins for each reference
            for itemMagasin in magasins:
                jsonTarifs = process_lambda(itemReference, itemMagasin)
                liste_tarifs.append(jsonTarifs)

        # Return JSON response
        return json.dumps({"ListeTarifs": liste_tarifs}), 200, {"Content-Type": "application/json"}

    except Exception as e:
        print(f"Error processing references: {e}")
        return json.dumps({"error": "Internal Server Error"}), 500, {"Content-Type": "application/json"}
