import aiohttp
import asyncio
import json

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'priority': 'u=1, i',
    'referer': 'https://www.zara.com/uk/en/zw-collection-100-linen-shirt-p05344241.html?v1=463549375',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    # 'cookie': 'MicrosoftApplicationsTelemetryDeviceId=4a7fb266-2d77-41ea-b4c7-e7b07387a817; MicrosoftApplicationsTelemetryFirstLaunchTime=2025-11-02T12:34:34.829Z; rid=55cc0701-0413-4f45-9446-3f5ea82fe082; rskxRunCookie=0; rCookie=71rwngrgdrk03apdiupsjosmhhp120p; OptanonAlertBoxClosed=2025-11-02T12:34:36.069Z; _gcl_au=1.1.1905978128.1762086876; CookiesConsent=C0001%3BC0002%3BC0003%3BC0004; ITXDEVICEID=637d6b66478b0463877a1a832f0c14be; UAITXID=5130c7a182db58f1ef8f9638dc3d7a4d6dc15a7ba1fc70d02305ddaa818a783a; _ga=GA1.1.1327396113.1762086876; ITXSESSIONID=3d32463c6c94edf060c33d5e8c39eba1; IDROSTA=9f93c128ffa6:2bc73760341853288083dd757; cart-was-updated-in-standard=true; ak_bmsc=BBD0B51363DAC3F4625FF3782DBC67E6~000000000000000000000000000000~YAAQL3AyuPAjnyWaAQAAtavURB1ob1BbeXb7cnKRxoGlWU6trzfVyGMmHgmlnDdOiRRLFFVoNQdl3zZcTS8Nuk1Y6W8BWECVxChVxQZ0lGZrvtrrZY8DwoTwKv+Ox+5ARE97QgHfgErE3nhlTQOyLzItoAD17+kJRrVhyVxv7op42tQaeJKZEZPFXZZIulNO0YWhYAB7X71ZdI650nTQBsbr69ELQfukIe97De0/ZdjEW0yqjaHGDUup0AYen4Rgmx9/IJygJ4b2DNVDvscwOvsrN+w0zqzKtePL3dFFQHXYLGanRlo8l411htf36VAJx4pgNSC+oVAm9OJcZCKOqput14lPNC+qmUddb8Ub39jO8Mbozu9CIJZgE7rzE0la+4GHPiYHZp87byfTJ5I/cTVchKXfI3P41y/s5V9yUAAiWKCpUiZk3UsYpCh1+xrb/NvBkpUwf0y1nqKoarDVzO4w6vwwe/LcQ0QcaggSzekp0scpz+kJ7SH/uYf3NybAmrMJvE+wnK7wSIOyblC1ukgeiaeUeG66/E0xQ3Fv3OGr6tzIy0wyFUaA+PZFuJwu3XCcYZbd2KW5ft/fL5wu/g==; FPID=FPID2.2.vdQHGnsLfZ9pt6Yj5xQaOP96nKVo3mznoakldS8bR9k%3D.1762086876; FPLC=4%2F764dC39gQ26tkFEfYJGui%2F1W%2FUym4W5mMKUuhaVBZvFLSYg%2FsNNvfK5UJ5GgOfKU40Ko9pjpaPL1hTx8ovOtyM9nm2v6u2CXcF0wGwE5ENkj2EkmzYPOtPO2GwdQ%3D%3D; _gtmeec=e30%3D; _fbp=fb.1.1762091387768.1586647538; _bamls_usid=02c9e49a-b1c6-499f-a81c-7df964d5d1d1; _tt_enable_cookie=1; _ttp=01K92DA25WH8VS9PAJ2AJQPSYZ_.tt.1; lantern=2c44972d-9a85-400a-acd3-95db53ed745f; vwr_global=1.5.1762091953.f1605359-6e67-415c-bdb6-35d7f1db9d70.1762086874..wX89IyraQXoa8nts4ORQMzUVoKY0t2wzjUzHvJFK-r8; _abck=7821A7083451198D55F7F4F6DEA04CCF~0~YAAQTEvdWBotAjaaAQAAiW/dRA7NHYExjZ92onsILVPBlIr8XH7atbo8xI4NIrgRcPniF+mKTJQ2kOR5YzEpQb//EPsYW0S27rDCtlHwolWJRFqv6gXDQSNKGvPFIopMuKQGQpwQjtskmOViPVeU/xDtuAIbUoBpS90EANzEvjgm0IjdOHjwZF2xi4E6DWE6CHvch1JVEk6U6QdxJbCt6ZDCwugu0bokuhnsUFCIt/nxitwNcLCxN8zmPVkTWH4OMHJ055MKlJffEN+EnkB5ZIoEaa2whPhKFjDNciynMaoRnzoNHg3l+MBlxdPNXUVAW0gTLPsUtRTkkUFHKwKzzvD4GvYl1C6WQ/DBZgswcedabCQZp3nNZS33ZnhEB7i6MQpBOuSG31BPKxfZghxOPac0e9QK8I08RAft7eugLtF2n39Esm6vItymATlRMdI7+ZasgxC9Kmm9og76bp0fih9uu25umumcc3ksfQ8L8+EonP7Mq5hGQhqVYPq8g0Qlkr92ZVs8t1pi7Pjet2eSep07YKroEoYVWGhJMddnmKM2VyTf7zfw2FGYCMVxPkZz5zlq/5sqhk3TbQkt94CP+HMgHHdRDEuqoz0J1t1HtEEkdJwa5s7Vrz/6pLephIPEj4HYL/Nr6evQRRPfmRLjC2BfMsBswyiWJIyZXIU4qI8kSPBAxKyi7BqPwkAbbziYoVVUc+k+Yczp5UIqd9RQTirJ5jTlN24VAxQC4C438UPEpWy+E+vW/f+RmX4qUYJCQAzgLYDpehddiju8mA2/5006rQ7EbLZrr4iDRQ2J0NSFzHjfmXOBkqN4KEsGgzYa+acZJfhpVzTpSa1o4nV9IDWNe0sdth0dC8wnYBSkJ+oc/2uEjb1eVjJo6f2GCpQudtGW35X3t6nEATD+BtDD6vwKLg==~-1~-1~1762094080~AAQAAAAE%2f%2f%2f%2f%2f09ysrsvpTmpt0MCx5Qv1IBhkX9jMadpY0fHFlPOD923wZ6cGnTEhyP+GFUT4AqpIukqI3DrP4tiiFFXbqEmOMiQQ7hvtwS3vnTP%2fOTrKv2kBaPzromEuClkFP+XNYxZldmr0yUkHgCa6uB%2fytVO9hpXHpi4QchsIdO7EXFCKw%3d%3d~-1; bm_sz=6F5F4778BE2210BB761743DAC2547DB3~YAAQTEvdWBwtAjaaAQAAiW/dRB1ETwWST4yzszHGkMw7G7Jb9GuYIkpmCmrGLyFlch0yhO7buPwY6Fc/0j9+FHUGQBpH1YniNqaKxvdRwOwYkzgF80IslEQVDlUyF4AemEryen9PLcDQiIUCxTE15qrcrLFq7qh6qAe45WNfOWTvi+KSukl+7H/jHtTkWuVv9VTVNQ3guV0P1RZYe0YOHxPwSlsanFD3hzNDwWrdl3fhirYAO/sAVwIaH3yAOTYpHzH+XqDO2RXD5ZvcDgoRDtUqhgtqGCOUdAPA7enRs/2YvDt4ne72CoQ31NqufPPMVq2ZSSQkpHnQyBXxq8sZ8FZcY/79FffgSlMANoiSmOK4gnJFWaUGuBIdVAXSIkfYsJiPVEK1ex9FHh48do4eK6fXY/aA5m52eqmNxtBXyVpIX8j1wQo/RXttuR4PICjnQ7ljQF9g0I/QUfrnTJSfUKPtyoVcpTlD51ccBRM=~3486773~3486004; lastRskxRun=1762091957643; OptanonConsent=isGpcEnabled=0&datestamp=Sun+Nov+02+2025+13%3A59%3A17+GMT%2B0000+(Greenwich+Mean+Time)&version=202508.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=eefee95c-0d39-422a-903f-c667bee9ff34&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&intType=1&geolocation=GB%3BENG&AwaitingReconsent=false; _ga_NOTFORGA4TRACKING=GS2.1.s1762091378$o1$g0$t1762091957$j60$l0$h2110700729; _ga_HCEXQGE0MW=GS2.1.s1762090312$o2$g1$t1762091957$j58$l0$h0; TS0122c9b6=01a2939ea531a45d5aaa86b7a308539f4e380107cc8246b3129c18444b3ef3a339f978bdcf767527f2b1e179fbe843dd507a0fc68a; bm_sv=D7D48C813DD047E1F25019614079F51F~YAAQTEvdWOQxAjaaAQAA24HdRB2Ux1qwWx1LZ9Kv1iCjWbmCIettvDYGy2EzMWv3J32ggR5DedZ6FJy45UILh2Z1LMfnjxwJ/C83M2PUrPzhiUdvDIadS9+YHdnfeQDzt+ZBBbLw4QSF8ZQglAJ8G/lqVGnZT81EHoD+6uqdqW2cyAfX9zDhwRRh+3ckde1tVIKASasIPOvJAyxqq7qd36eiZ+vz3JVhx57MwSQKqdzVXgaHE2ElL1RvZ9OYD2s=~1; ttcsid=1762091403462::hrLZTgwoF_wYjcAKZMMe.1.1762091969731.0; ttcsid_CPC49C3C77UFPV6QTC60=1762091403460::-Az_O54d0vFnBqinKife.1.1762091969731.0',
    }
params = {
    'productIds': [
        '490754812',
        '472926659',
    ],
    'ajax': 'true',
    }

async def get_page(session,url):
    async with session.get(url, headers = headers,  params=params) as response:
        if response.status in (403,429):
            print(f"Blocked with status code: {response.status}")
            return None
        return await response.json()

async def fetch_product(session,url):
    results = []
    # print(await get_page(session, url))
    content = await get_page(session, url)
    print(content.keys())
    if content:
        results = parse(content)

    return results


async def main(url):
    if not url:
        return []

    async with aiohttp.ClientSession() as session:
        data = await fetch_product(session, url)
    return parse(data) if data else []

def parse(data):
    results = []
    color_images = {}
    print(data.keys())
    for key, value in data.items():
        print(key, type(value))


    for color in data.get('product', {}).get('detail', {}).get('colors', []):
        print(color)
        for media in color.get('xmedia', []):
            image_url = media.get('extraInfo', {}).get('deliveryUrl')
            if image_url:
                color_images[color.get('name')] = image_url
                break

    for item in data.get('productMetaData', []):
        print(item)
        if item.get('availability') == 'in_stock' and item.get('price') is not None:
            results.append({
                "sku": item.get('sku', ''),
                "name": item.get('name') or 'Zara product',
                "price": item['price'],
                "url": item.get('url'),
                "sizeName": item.get('sizeName'),
                "colorName": item.get('colorName'),
                "description": item.get('description'),
                "image_url": color_images.get(item.get('colorName')),
            })
    #     price = data['productMetaData'][item]['price']
    #     url = data['productMetaData'][item]['url']
    #     availability = data['productMetaData'][item]['availability']
    #     description = data['productMetaData'][item]['description']
    #     sizeName = data['productMetaData'][item]['sizeName']
    #     colorName = data['productMetaData'][item]['colorName']
    # return {
    #     "price": price,
    #     "url": url,
    #     "availability": availability,
    #     "description": description,
    #     "sizeName": sizeName,
    #     "colorName": colorName
    # }
    return results



if __name__ == "__main__":
    result = asyncio.run(main('https://www.zara.com/uk/en/off-the-shoulder-knit-top-p02142047.html?v1=509631874&v2=2419925'))
    print(result)


 











# async def get_page(session, url):
#     async with session.get(url, headers = headers, params = params) as request:
#         return await request.json()

# async def get_all(session, urls):
#    items_to_scrape = []
#    for url in urls:
#       task = asyncio.create_task(get_page(session,url))
#       items_to_scrape.append(task)
#       results = await asyncio.gather(*items_to_scrape)
#    # return results
#    return items_to_scrape


# async def main(urls):
#     async with aiohttp.ClientSession() as session:
#         data = await get_all(session, urls)
#         return data

#to fetch specific data from json  
# def parse(results):
#    for item in results['Price']:
#        print(item)
    
# if __name__ == '__main__':
#    urls = ['https://www.zara.com/uk/en/running-trainers-p15036610.html?v1=458113705',
#             'https://www.zara.com/uk/en/zw-collection-100-linen-shirt-p05344241.html?v1=463549375']
#    results = asyncio.run(main(urls))
#    for item in results:
#        print(item.result())


# async def main():
#    url = 'https://www.zara.com/uk/en/running-trainers-p15036610.html?v1=458113705'
#    response_json = await fetch(url)
#    pretty_data = json.dumps(response_json, indent = 4)
   
#    with open('data.txt', 'w') as f:
#       # only write specific data to file 
#       f.write(pretty_data)

#    with open('data.txt', 'r') as f:
#       data = json.load(f)
#       for line in data:
#          if line == "productMetaData":
#             pdata = data[line][2]
#             print(pdata)
#             df = pd.DataFrame([pdata])
#             print(df)
#             print(df[['url']].to_string(index = False))

#          elif line == "analyticsData":
#             print(f"Is this Item Low in stock : {data[line]["lowOnStockProduct"]}")
#       return df
            # print(data[line])
    #   print(type(new_data))


# if __name__ == "__main__":
#    asyncio.run(main())