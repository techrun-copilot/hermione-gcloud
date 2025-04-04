import functions_framework
import json

@functions_framework.http
def check_csv(request):
    try:
        request_json = request.get_json(silent=True)
        if not request_json:
            return json.dumps({"error": "Invalid JSON input"}), 400

        all_references = request_json.get("AllReferences", [])
        csv_data = request_json.get("csv_import_content", {}).get("data", "")

        if not all_references or not csv_data:
            return json.dumps({"error": "Missing required data"}), 400

        # Transformer la liste de références en dictionnaire pour une recherche rapide
        reference_dict = {ref["item"]: ref for ref in all_references}

        # Traiter le CSV en ignorant l'en-tête
        csv_items = []
        for line in csv_data.split("\n")[1:]:  
            parts = line.strip().split(",")
            if len(parts) < 2:
                continue
            item = parts[0].strip()
            quantite = parts[1].strip().replace(",", ".")  # Convertir les virgules en points
            
            try:
                quantite = int(float(quantite))  # Conversion sécurisée
            except ValueError:
                quantite = 1  # Valeur par défaut si conversion échoue
            
            csv_items.append({"item": item, "quantite": quantite})

        # Initialisation des listes d'items
        items_ok = []
        items_manquants = []

        for csv_item in csv_items:
            reference = reference_dict.get(csv_item["item"])  # Recherche rapide dans le dict
            if reference:
                try:
                    pa_ht = float(reference["pa_ht"])  # Conversion de `pa_ht` en float
                except ValueError:
                    pa_ht = 0  # Valeur par défaut si problème

                items_ok.append({
                    "item": reference["item"],
                    "pa_ht": pa_ht,
                    "taille": reference.get("taille_nom", ""),
                    "bar_code": reference.get("bar_code", ""),
                    "item_desc": reference.get("item_desc", ""),
                    "quantite": csv_item["quantite"],
                })
            else:
                items_manquants.append(csv_item["item"])

        # Calcul du montant total HT
        montant_total_ht = sum(item["pa_ht"] * item["quantite"] for item in items_ok)

        # Format de retour optimisé
        response_data = {
            "item_ok": {
                "item": ", ".join(item["item"] for item in items_ok) or "",
                "type": request_json.get("type", ""),
                "pa_ht": ", ".join(str(item["pa_ht"]) for item in items_ok) or "",
                "taille": ", ".join(item["taille"] for item in items_ok) or "",
                "user_id": request_json.get("user_id", ""),
                "bar_code": ", ".join(item["bar_code"] for item in items_ok) or "",
                "quantite": ", ".join(str(item["quantite"]) for item in items_ok) or "",
                "item_desc": ", ".join(item["item_desc"] for item in items_ok) or "",
                "magasin_id": request_json.get("magasin_id", ""),
                "type_mouvement": request_json.get("type_mouvement", ""),
                "montant_total_ht": f"{montant_total_ht:.2f}",
            },
            "item_manquants": items_manquants if items_manquants else []
        }

        return json.dumps(response_data), 200, {"Content-Type": "application/json"}

    except Exception as e:
        return json.dumps({"error": str(e)}), 500, {"Content-Type": "application/json"}
