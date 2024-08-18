from flask import Flask, render_template, request, redirect, url_for
import requests
import re
import sqlite3

# Note end clothing websites have website number 7 in their json results as the SG website

app = Flask(__name__)

def format_html(html_string):
    formatted_text = re.sub(
        r"<[^>]+>|[\r\n]+",
        lambda m: "\n" if m.group(0) in ["\r", "\n"] else "",
        html_string,
    ).strip()

    return formatted_text


def end_clothing_scraper(query_item):
    url = "https://search1web.endclothing.com/1/indexes/*/queries"

    # Define the payload
    payload = {
        "requests": [
            {
                "indexName": "catalog_products_v2_gb_products_search",
                "params": f"facets=%5B%5D&highlightPostTag=__%2Fais-highlight__&highlightPreTag=__ais-highlight__&query={query_item}&tagFilters=",
            },
            {
                "indexName": "catalog_categories_en_search",
                "params": f"facets=%5B%5D&highlightPostTag=__%2Fais-highlight__&highlightPreTag=__ais-highlight__&query={query_item}&tagFilters=",
            },
        ]
    }

    headers = {
        "X-Algolia-Agent": "Agolia for JavaScript (3.35.1); Browser",
        "X-Algolia-API-Key": "dfa5df098f8d677dd2105ece472a44f8",  
        "X-Algolia-Application-Id": "KO4W2GBINK", 
    }

    # Make the POST request
    response = requests.post(url, headers=headers, json=payload)
    data = response.json()

    return data


def end_clothing_json_parser(data):
    search_list = []

    for item in data["results"][0]["hits"]:
        name = item["name"]

        if name in search_list:
            continue

        url_key = f"https://www.endclothing.com/sg/{item['url_key']}.html"
        img_url = f"https://media.endclothing.com/media/f_auto,q_auto:eco,w_300/prodmedia/media/catalog/product{item['small_image']}"

        #if item["full_price_7"] == item["final_price_7"]: #End Clothing's 7th website is the Singapore website
        price = int(item["full_price_7"])
        #else:
            #price = "Unavailable"

        search_list.append((name, url_key, img_url, price))


    return search_list


def end_desc(item):
    desc = format_html(item["description"])
    model_img_url = f"https://media.endclothing.com/media/f_auto,q_auto:eco,w_300/prodmedia/media/catalog/product{item['model_full_image']}"

    return (desc, model_img_url)


def grailed_scraper(query_item):
    url = "https://mnrwefss2q-3.algolianet.com/1/indexes/*/queries?"

    # Define the payload
    payload = {
        "requests": [
            {
                "indexName": "Listing_production",
                "params": f"analytics=true&clickAnalytics=true&enableABTest=true&enablePersonalization=true&facets=%5B%22department%22%2C%22category_path%22%2C%22category_size%22%2C%22designers.name%22%2C%22price_i%22%2C%22condition%22%2C%22location%22%2C%22badges%22%2C%22strata%22%5D&filters=&getRankingInfo=true&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&highlightPreTag=%3Cais-highlight-0000000000%3E&hitsPerPage=40&maxValuesPerFacet=100&numericFilters=%5B%22price_i%3E%3D0%22%2C%22price_i%3C%3D1000000%22%5D&page=0&personalizationImpact=99&query={query_item}&tagFilters=&userToken=03d6d929-89b2-48f0-864f-158e78967f7c",
            },
            #{
            #   "params": f"analytics=false&clickAnalytics=false&enableABTest=true&enablePersonalization=true&facets=price_i&filters=&getRankingInfo=true&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&highlightPreTag=%3Cais-highlight-0000000000%3E&hitsPerPage=0&maxValuesPerFacet=100&page=0&personalizationImpact=99&query={query_item}&userToken=03d6d929-89b2-48f0-864f-158e78967f7c",
            #},
            #{
            #    "indexName": "Listing_sold_production",
            #    "params": f"analytics=true&clickAnalytics=true&enableABTest=true&enablePersonalization=true&facets=%5B%22department%22%2C%22category_path%22%2C%22category_size%22%2C%22designers.name%22%2C%22price_i%22%2C%22condition%22%2C%22location%22%2C%22badges%22%2C%22strata%22%5D&filters=&getRankingInfo=true&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&highlightPreTag=%3Cais-highlight-0000000000%3E&hitsPerPage=40&maxValuesPerFacet=100&numericFilters=%5B%22price_i%3E%3D0%22%2C%22price_i%3C%3D1000000%22%5D&page=0&personalizationImpact=99&query={query_item}&tagFilters=&userToken=03d6d929-89b2-48f0-864f-158e78967f7c",
            #},
            #
            {
                "indexName": "Listing_sold_production",
                "params": f"analytics=false&clickAnalytics=false&enableABTest=true&enablePersonalization=true&facets=price_i&filters=&getRankingInfo=true&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&highlightPreTag=%3Cais-highlight-0000000000%3E&hitsPerPage=0&maxValuesPerFacet=100&page=0&personalizationImpact=99&query={query_item}&userToken=03d6d929-89b2-48f0-864f-158e78967f7c",
            },
        ]
    }

    params = f"x-algolia-agent=Algolia%20for%20JavaScript%20(4.14.3)%3B%20Browser%3B%20JS%20Helper%20(3.11.3)%3B%20react%20(18.2.0)%3B%20react-instantsearch%20(6.39.1)"

    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Content-Length": "2102",
        "DNT": "1",
        "Host": "mnrwefss2q-3.algolianet.com",
        "Origin": "https://www.grailed.com",
        "Referer": "https://www.grailed.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        "content-type": "application/x-www-form-urlencoded",
        "sec-ch-ua": 'Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Linux",
        "x-algolia-api-key": "bc9ee1c014521ccf312525a4ef324a16",
        "x-algolia-application-id": "MNRWEFSS2Q",
    }

    # Make the POST request
    response = requests.post(url, params=params, headers=headers, json=payload)
    data = response.json()

    return data


def grailed_json_parser(data): #Finds the name, url key, the image url, price, and result-count
    search_list = []

    for item in data["results"][0]["hits"]:
        name = item["title"]

        if name in search_list:
            continue

        listing_id = item["cover_photo"]["listing_id"]
        item_url_name = (
            (item["designer_names"] + name).lower().replace(" ", "-").replace("×", "x")
        )

        url_key = f"https://www.grailed.com/listings/{listing_id}-{item_url_name}?g_aidx=Listing_production&g_aqid=0423e32dedbd523eb7b0a357f5f7235d"
        img_url = item["cover_photo"]["url"]

        try:
            US_price = item["price"]
            SG_price = 1.32 * US_price
            price = int(SG_price)
        except:
            price = "Unavailable"

        search_list.append((name, url_key, img_url, price))

    return search_list

# def AddDB(data): #Main logic will be done in index()



@app.route("/", methods=["GET", "POST"])
def index():
    end_item_list, grailed_item_list = [], []
    if request.method == "POST":
        query_item = request.form["item"]
        end_json = end_clothing_scraper(query_item)
        grailed_json = grailed_scraper(query_item)

        end_item_list = end_clothing_json_parser(end_json)
        grailed_item_list = grailed_json_parser(grailed_json)

    return render_template(
        "index.html", end_item_list=end_item_list, grailed_item_list=grailed_item_list
    )


@app.route("/desc")
def desc():
    name = request.args.get("name")
    brand = request.args.get("brand")

    if brand == "END":
        end_json = end_clothing_scraper(name)
        desc, model_img_url = end_desc(end_json["results"][0]["hits"][0])

        return render_template("desc.html", desc=desc, model_img_url=model_img_url)

    else:
        return redirect(url_for("index"))
    
@app.route("/purchaselink")
def linkredirect():
    url = request.args.get("url")
    print(url)
    try:
        response = requests.get(url)

        if response.status_code == 404:
            return render_template("404.html")
        else:
            return redirect(url)
    except Exception:
        return redirect(url_for(index))


if __name__ == "__main__":
    

    app.run(debug=True)
