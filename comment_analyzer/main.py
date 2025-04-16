from DB_utils.ERM.storage.interfaces.get_data import get_product, get_comments, get_vendor, get_vendors, \
    get_comment_from_analyze
from DB_utils.ERM.storage.interfaces.add_data import add_analyze
import requests
import json
from analyzer import analyze  # Import the analyze function

def get_materials(comment, vendor_id):
    foods = []
    detail = []
    materials = []
    for food in comment['foods']:
        product = get_product(vendor_id, food['title'])
        if product:
            materials.append({food['title']: product['description']})
            detail.append({'product_title': food['title'],
                           'product_description': product['description'],
                           'product_id': product['product_id']})
        else:
            return False
        foods.append(food['title'])

    return {"materials": materials, "foods": foods, "detail": detail}

def fetch_and_analyze_comments(vendor_id):
    comments = get_comments(vendor_id)
    counter = 1
    if len(comments) > 200:
        for comment in comments:
            if get_comment_from_analyze(comment['comment_id']):
                return True
            if counter == 15:
                return True
            data = {"comment": comment['comment_text']}
            materials = get_materials(comment, vendor_id)
            if materials:
                data['materials'] = materials['materials']
                data["foods"] = materials['foods']
                detail = materials['detail']
                
                # Use the analyze function
                analysis_results = analyze(data)
                
                if analysis_results:
                    print(f'request number {counter}, AI response is : {analysis_results}')
                    counter += 1
                    vendor_code = get_vendor(vendor_id)
                    add_analyze(
                        comment['comment_id'],
                        vendor_id,
                        comment['comment_text'],
                        vendor_code,
                        analysis_results['qualities'],
                        analysis_results['services'],
                        analysis_results['foods overall rating'],
                        detail,
                    )
                else:
                    print('error from AI')
                    break

# x = fetch_and_analyze_comments(232663)
# print(get_vendor(232663))
counter = 1
vendors = get_vendors()
for vendor in vendors:
    print(f"[{counter}] process started for vendor: {vendor['title']}")
    fetch_and_analyze_comments(vendor['id'])
    counter += 1
    print('#####################################################')
    if counter == 200:
        print('done')
        break
