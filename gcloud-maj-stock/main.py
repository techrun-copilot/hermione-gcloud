import functions_framework
import json

# Fonction pour convertir une chaîne en nombre flottant en détectant le séparateur décimal
def parse_number(value):
    if ',' in value:
        return float(value.replace(',', '.'))
    return float(value)

# Fonction pour formater un nombre en chaîne avec un point comme séparateur décimal
def format_number(num):
    return "{:.2f}".format(num)

@functions_framework.http
def lambda_stock(request):
    # Récupérer les données JSON envoyées par l'utilisateur
    data = request.get_json()

    items = data['item'].split(', ')
    pa_hts = data['pa_ht'].split(', ')
    tailles = data['taille'].split(', ')
    bar_codes = data['bar_code'].split(', ')
    quantites = data['quantite'].split(', ')
    item_descs = data['item_desc'].split(', ')
    magasin_id = int(data['magasin_id'])
    stock_pmp = data['StockPourPMP']

    output = []

    # Prétraiter stockPourPMP en dictionnaire pour des recherches plus rapides
    stock_map = {}
    for pmp in stock_pmp:
        key = f"{pmp['magasin_id']}-{pmp['item']}"
        stock_map[key] = parse_number(pmp['pmp']) if 'pmp' in pmp else None

    for i in range(len(items)):
        pa_ht = parse_number(pa_hts[i])
        quantite = int(quantites[i])
        item_code = int(items[i])

        if pa_ht is None:
            pa_ht = 0  # Valeur par défaut si la conversion échoue

        # Recherche du pmp correspondant dans le stock_map
        key = f"{magasin_id}-{item_code}"
        pmp = stock_map.get(key, None)

        if pmp is not None:
            pa_ht = pmp

        if quantite == 0:
            continue  # Ignore cet item si la quantité est invalide

        prix_total_ht = format_number(pa_ht * quantite)

        item = {
            'item': items[i],
            'pa_ht': pa_ht,
            'taille': tailles[i],
            'bar_code': bar_codes[i],
            'quantite': quantite,
            'item_desc': item_descs[i],
            'prix_total_ht': prix_total_ht,
            'pmp': pmp
        }

        output.append(item)

    # Retourner la réponse JSON
    return json.dumps(output)

