import functions_framework
import json
import re

def clean_text(text):
    """
    Remove non-alphanumeric characters and trim spaces
    """
    if not isinstance(text, str):
        return text
    return re.sub(r'[^a-zA-Z0-9\s]', '', text).strip()

def format_date(date_string):
    """
    Format date from YYYY-MM-DD to DD/MM/YYYY
    """
    if not date_string or '-' not in date_string:
        return ''
    parts = date_string.split('-')
    return f"{parts[2]}/{parts[1]}/{parts[0]}"

@functions_framework.http
def process_data(request):
    try:
        request_body = request.get_data(as_text=True)
        data = json.loads(request_body) if request_body else {}

        if "records" not in data:
            return json.dumps({"error": "Expected JSON with 'records' key"}), 400, {'Content-Type': 'application/json'}

        processed_data = []

        for reference in data["records"]:
            processed_data.append({
                "ITEM": reference.get("item", ""),
                "COUNTRY": clean_text(reference.get("country", "")),
                "VAT_CODE": reference.get("vat_code", ""),
                "BAR_CODE": reference.get("bar_code", ""),
                "ITEM_DESC": clean_text(reference.get("item_desc", "")),
                "DEPT": reference.get("famille_dept", ""),
                "CLASS": reference.get("codemarque_class", ""),
                "CARAC_RMS_PRODUIT": reference.get("ugencaissement_code", ""),
                "UOM": reference.get("uom", ""),
                "CARAC_RMS_TYPE_ARTICLE": reference.get("carac_rms_type_article", ""),
                "CARAC_RMS_STATUT_MARCHANDISE": reference.get("carac_rms_statut_marchandise", ""),
                "CARAC_RMS_ESCOMPTABILITE": reference.get("carac_rms_escomptabilite", ""),
                "CARAC_UG_FAMILLE": reference.get("ugencaissement_code", ""),
                "UNITE_CONTENANCE": reference.get("unite_contenance", ""),
                "CONTENANCE": reference.get("contenance", ""),
                "CARAC_TICKET_RESTAURANT": clean_text(reference.get("carac_ticket_restaurant", "")),
                "CREDATE": format_date(reference.get("date", "")),
                "ACTION": reference.get("action", "")
            })

        return json.dumps({"processed_records": processed_data}), 200, {'Content-Type': 'application/json'}

    except Exception as e:
        return json.dumps({"error": str(e)}), 500, {'Content-Type': 'application/json'}