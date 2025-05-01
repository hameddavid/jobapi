import json
webflow_siteId = "60d7d6d5b3b5b8127f5d149a"
webflow_auth_token = "f8e61fe79ecb93c190dbe73bc946a3531d181e57b1476b9f577733fc6400586b"
def getProductInListOfProducts(productid):
    try:
        global webflow_auth_token, webflow_siteId
        import http.client
        conn = http.client.HTTPSConnection("api.webflow.com")
        headers = { 
                     'Accept-Version': "1.0.0",
                     'Authorization':  f"{webflow_auth_token}" ,
                     'content-type': "application/json"
                  }
        req = f"/sites/{webflow_siteId}/products/{productid}"   
        conn.request("GET",  req, headers=headers) 
        res = conn.getresponse()
        data = res.read() 
        if res.status == 200:          
            ret = {"success": json.loads(data.decode("utf-8").replace("'", "\""))}
        else:
            ret = {"error": data.decode("utf-8")}
    except Exception as e:
        ret = {"error": str(e)}
    return ret       

def getListOfProducts():
    try:
        import http.client
        global webflow_auth_token, webflow_siteId
        conn = http.client.HTTPSConnection("api.webflow.com")
        headers = { 
                     'Accept-Version': "1.0.0",
                     'Authorization':  f"{webflow_auth_token}" ,
                     'content-type': "application/json"
                  }
        req = f"/sites/{webflow_siteId}/products/"   
        conn.request("GET",  req, headers=headers) 
        res = conn.getresponse()
        data = res.read() 
        if res.status == 200:           
            ret = {"success": json.loads(data.decode("utf-8").replace("'", "\""))}
        else:
            ret = {"error": data.decode("utf-8")}
    except Exception as e:
        ret = {"error": str(e)}
    return ret

def getProduct(itemid):
    try:        
        global webflow_auth_token, webflow_siteId
        import http.client
        global webflow_auth_token, webflow_siteId
        conn = http.client.HTTPSConnection("api.webflow.com")
        req = f"/sites/{webflow_siteId}/products/{itemid}"   
        headers = { 
                     'Accept-Version': "1.0.0",
                     'Authorization':  f"{webflow_auth_token}" ,
                     'content-type': "application/json"
                  }
        conn.request("GET",  req, headers=headers) 
        res = conn.getresponse()
        data = res.read()
        if res.status ==  200: 
            ret = json.loads(data.decode("utf-8").replace("'", "\""))         
            if ret["count"] <=0:
                ret = {"error":  f"product[{itemid}] not found."} 
            else:
                items =  ret["items"]
                item = items[0]               
                product = item["product"]
                skus = item["skus"]
                skus = skus[0]  #only object in the list [skus]
                name = product["name"]
                price = skus["price"]
                price = price["value"]
                categories = ""
                if "category" in product:
                    categories = product["category"]
                desc = ""   #not currently returned to caller
                if "description" in product:
                    desc=  product["description"]  
                ret = {"name": name, "categories": categories, "price": price}
                ret = { "success": ret }
        else:
            ret = {"error": data.decode("utf-8")}
      
    except Exception as e:
        ret = {"error": str(e)}
    return ret 

def getCategoriesArtworks():
    try:
        collectionid = "615e83040ea2ff03a77d4ea7"  #id of Categories collection
        ret = listItemsInCollection(collectionid)   
        if  "success" in ret:
            ret = ret["success"]
            if ret["count"] <= 0:
                ret = {"error": "Categories not found in Webflow."}
            else:
                items = ret["items"]
                ret = []
                for item in items:
                    ret.append({ "name": item["name"], "id": item["_id"]})
                ret = {"success": ret}
        else:
            ret = {"error": ret}
    except Exception as e:  
        ret = {"error": str(e)}
    return ret 
def updateProduct(itemid):
    def getNamesOfCategories(categories, remoteList):
        def getNameOfCategoryIfExist(category, remoteList):
            for item in remoteList:        
                if category == item["id"]:
                    return {"found":True, "name": item["name"]}
            return {"found":False, "name": "not found"}
        try:
            ret = ""
            for category in categories:
                res = getNameOfCategoryIfExist(category, remoteList)
                if res["found"]:
                    if ret == "":
                        ret = res['name']
                    else:
                        ret = f"{ret},{res['name']}"
                else:
                     ret = f"{ret},{category}"        
        except Exception as e:
            ret =  str(e)
        return ret 
    try:
        resp = getProduct(itemid)       
        categories = "default"
        if "success" in resp:
            ret = resp["success"]
            categories = ret["categories"]    
            r = getCategoriesArtworks()  
            if "success" in r:
                r = r["success"]
            categories = getNamesOfCategories(categories, r)      
    
        import http.client
        global webflow_auth_token, webflow_siteId
        conn = http.client.HTTPSConnection("api.webflow.com")
        headers = { 
                     'Accept-Version': "1.0.0",
                     'Authorization':  f"{webflow_auth_token}" ,
                     'content-type': "application/json"
                  }
        payload = {
             "fields":
                    {                      
                     "item-id": f"{itemid}",
                     "categories-names": f"{categories}"
                     }
                    }
        payload = json.dumps(payload)
        conn.request("PATCH", f"/sites/{webflow_siteId}/products/{itemid}", payload, headers)
        res = conn.getresponse()
        data = res.read() 
        if res.status ==  200: 
            ret = json.loads(data.decode("utf-8").replace("'", "\"")) 
        else:
            ret = {"error": data.decode("utf-8")}
        res = f"update[{ret}]"
        ret = {"success": res} 
    except Exception as e:
        ret = {"error": str(e)}
    return ret 

'''

def createProduct(name = "",slug = "",desc = "",  artist_name = "", title = "", 
    categories = "", categories_names = "", tags = "", 
    urlofarmodel = "", price = 0, weight = 0, width = 0, length = 0, height =0, main_image = {},  
    more_images=[],  download_files = []):
    try:
        import http.client
        global webflow_auth_token, webflow_siteId
        conn = http.client.HTTPSConnection("api.webflow.com")
        headers = { 
                     'Accept-Version': "1.0.0",
                     'Authorization':  f"{webflow_auth_token}" ,
                     'content-type': "application/json"
                  }
        payload =    {
             "product":  {
                       "name":   name,
                       "fields":    {                                                                   
                                        "shippable": True,                                   
                                        "slug": f"{slug}",
                                        "name": f"{name}",
                                        "description":  f"{desc}",
                                        "category":  categories,  
                                        "categories-names":  categories_names,                             
                                        "_archived": False,
                                        "_draft": False,
                                        "artist-name":   artist_name,
                                        "title": title,
                                        "tags": tags,
                                        "urlofarmodel": urlofarmodel
                                      
                                   },            
                         },
                "sku":   {
                  "fields":  {  "name":  f"{name}",
                                "slug":  f"{slug}",
                                "price": {
                                            "unit": "USD",
                                            "value": price
                                        },
                                "_archived": False,
                                "_draft": False,
                                "width": width,
                                "length": length,
                                "height": height,
                                "weight": weight,                               
                                "main-image":  main_image,
                                "more-images": more_images,
                                "download-files": download_files,                                                             
                                   }                                  
                }, 
             }
        payload = json.dumps(payload)
        conn.request("POST", f"/sites/{webflow_siteId}/products", payload, headers)
        res = conn.getresponse()
        data = res.read() 
        if res.status ==  200:  
            ret = json.loads(data.decode("utf-8").replace("'", "\""))  
            ret = ret["product"]  
            updateProduct(ret["_id"])          
            ret = { "success": ret["_id"]}
        else:
            ret = {"error": data.decode("utf-8")}
    except Exception as e:
        ret = {"error": str(e)}
    return ret
'''

def createProduct(name = "",slug = "",desc = "",  artist_name = "", title = "", 
    categories = "", categories_names = "", tags = "", 
    urlofarmodel = "", price = 0, weight = 0, width = 0, length = 0, height =0, main_image = {},  
    more_images=[],  download_files = []):
    try:
        import http.client
        global webflow_auth_token, webflow_siteId
        conn = http.client.HTTPSConnection("api.webflow.com")
        headers = { 
                     'Accept-Version': "1.0.0",
                     'Authorization':  f"{webflow_auth_token}" ,
                     'content-type': "application/json"
                  }
        payload =    {
             "product":  {
                       "name":   name,
                       "fields":    {                                                                   
                                        "shippable": True,                                   
                                        "slug": f"{slug}",
                                        "name": f"{name}",
                                        "description":  f"{desc}",
                                        "category":  categories,  
                                        "categories-names":  categories_names,                             
                                        "_archived": False,
                                        "_draft": False,
                                        "artist-name":   artist_name,
                                        "title": title,
                                        "tags": tags,
                                        "urlofarmodel": urlofarmodel
                                      
                                   },            
                         },
                "sku":   {
                  "fields":  {  "name":  f"{name}",
                                "slug":  f"{slug}",
                                "price": {
                                            "unit": "USD",
                                            "value": price
                                        },
                                "_archived": False,
                                "_draft": False,
                                "width": width,
                                "length": length,
                                "height": height,
                                "weight": weight,                               
                                "main-image":  main_image,
                                "more-images": more_images,
                                "download-files": download_files,                                                             
                                   }                                  
                }, 
             }
        payload = json.dumps(payload)
        conn.request("POST", f"/sites/{webflow_siteId}/products", payload, headers)
        res = conn.getresponse()
        data = res.read() 
        if res.status ==  200:  
            ret = json.loads(data.decode("utf-8").replace("'", "\""))  
            ret = ret["product"]  
            updateProduct(ret["_id"])          
            ret = { "success": ret["_id"]}
        else:
            ret = {"error": data.decode("utf-8")}
    except Exception as e:
        ret = {"error": str(e)}
    return ret
 
def listCollections():
    try:        
        import http.client
        global webflow_auth_token, webflow_siteId
        conn = http.client.HTTPSConnection("api.webflow.com")
        req = f"/sites/{webflow_siteId}/collections"
        headers = { 
                     'Accept-Version': "1.0.0",
                     'Authorization':  f"{webflow_auth_token}" ,
                     'content-type': "application/json"
                  }
        conn.request("GET",  req, headers=headers) 
        res = conn.getresponse()
        data = res.read() 
        if res.status ==  200:           
            ret = { "success": json.loads(data.decode("utf-8").replace("'", "\""))}
        else:
           ret = {"error": data.decode("utf-8")}
    except Exception as e:
        ret = {"error": str(e)}
    return ret
 
def listItemsInCollection(collectionId):
    try:            
        import http.client
        global webflow_auth_token, webflow_siteId
        conn = http.client.HTTPSConnection("api.webflow.com")
        req = f"/collections/{collectionId}/items"
        headers = { 
                     'Accept-Version': "1.0.0",
                     'Authorization':  f"{webflow_auth_token}" ,
                     'content-type': "application/json"
                  }
        conn.request("GET",  req, headers=headers)
        res = conn.getresponse()
        data = res.read() 
        if res.status ==  200:           
            ret = { "success": json.loads(data.decode("utf-8").replace("'", "\""))}
        else:
            ret = {"error": data.decode("utf-8")}
    except Exception as e:
        ret = {"error": str(e)}
    return ret             

def getItemInCollection(collectionid, itemid):
    try:       
        import http.client
        global webflow_auth_token, webflow_siteId
        conn = http.client.HTTPSConnection("api.webflow.com")
        req = f"/collections/{collectionid}/items/{itemid}"
        headers = { 
                     'Accept-Version': "1.0.0",
                     'Authorization':  f"{webflow_auth_token}" ,
                     'content-type': "application/json"
                  }
        conn.request("GET",  req, headers=headers) 
        res = conn.getresponse()
        data = res.read() 
        if res.status ==  200:          
            ret = { "success": json.loads(data.decode("utf-8").replace("'", "\""))}
        else:
            ret = {"error": data.decode("utf-8")}
    except Exception as e:
        ret = {"error": str(e)}
    return ret           
def getGalleries():
    try:
        collectionid = "61707513762d547b8160f751"  #id of galleries collection
        ret = listItemsInCollection(collectionid)   
        if  "success" in ret:
            ret = ret["success"]
            if ret["count"] <= 0:
                ret = {"error": "Galleries not found in Webflow."}
            else:
                items = ret["items"]
                ret = []
                for item in items:
                    ret.append(
                        { "name": item["name"], "id": item["_id"], "location": item["location-of-gallery"]
                        }
                        )
                ret = {"success": ret}
        else:
            ret = {"error": ret}
    except Exception as e:  
        ret = {"error": str(e)}
    return ret 

def getCategoryOfArtworkInCollection(itemid):
    try:
        collectionid = "615e83040ea2ff03a77d4ea7"  #id of Categories collection
        ret = getItemInCollection(collectionid, itemid)
        if "success" in ret:
            ret = ret["success"]
            if ret["count"] <= 0:
                ret = {"error": "Categories not found in Webflow."}
            else:
                items = ret["items"]
                ret = []
                for item in items:
                    ret.append({ "name": item["name"], "id": item["_id"]})
                ret = {"success": ret}         
    except Exception as e:
        ret = {"error": str(e)}
    return ret 
def createGallery(name = "", slug ="", location = ""):
    try: 
        import http.client
        global webflow_auth_token, webflow_siteId
        conn = http.client.HTTPSConnection("api.webflow.com")
        headers = { 
                     'Accept-Version': "1.0.0",
                     'Authorization':  f"{webflow_auth_token}" ,
                     'content-type': "application/json"
                  }
        payload =  {
                     "fields":  {
                        "name": name,
                        "slug": slug,
                        '_archived': False,
                        '_draft': False,
                        'location-of-gallery': location
                      }
                  }
        payload = json.dumps(payload)
        conn.request("POST", "/collections/61707513762d547b8160f751/items", payload  ,   headers)
        res = conn.getresponse()
        data = res.read() 
        if res.status ==  200:  
            resp = json.loads(data.decode("utf-8").replace("'", "\""))
            ret =  {"success":  resp["_id"]}            
         
        else:
            ret = {"error": data.decode("utf-8")} 
    except Exception as e:
        ret = {"error": str(e)}
    return ret 
def createArtist(name = "", bio = "", slug ="", location = "", galleries = ""):
    try: 
        import http.client
        global webflow_auth_token, webflow_siteId
        conn = http.client.HTTPSConnection("api.webflow.com")
        headers = { 
                     'Accept-Version': "1.0.0",
                     'Authorization':  f"{webflow_auth_token}" ,
                     'content-type': "application/json"
                  }
        payload =  {
                     "fields":  {
                        "name": name,
                        "slug": slug,
                        '_archived': False,
                        '_draft': False,
                        'artist-location': location,
                        "gallery": galleries,
                        "bio": bio
                      }
                  }
        payload = json.dumps(payload)
        conn.request("POST", "/collections/61707668e36059d6cbe36353/items", payload,   headers)
        res = conn.getresponse()
        data = res.read() 
        if res.status ==  200:  
            ret = json.loads(data.decode("utf-8").replace("'", "\""))                     
            ret = { "success": ret["_id"]}
        else:          
            ret = {"error": data.decode("utf-8")} 
    except Exception as e:
        ret = {"error": str(e)}
    return ret 
from hello.domain.models.Artworks import WebFlowItems
def transformTags(tags):
    try:
        if tags.strip() == "":
         return tags
        ret =tags.split(",")
        resp = ""
        
        for t  in ret:
            tag = getItemNameLocallyIfExist(t)
            if "success" not in tag:
                tag = getCategoryOfArtworkInCollection(t)
                if "success" in tag:
                    tag = tag["success"]
                    if len(tag) > 0:                
                        tag = tag[0]
                        tag = tag["name"] 
                        storeItemNameLocally(tag, t) 
                        t = tag 
            else:
                t = tag["success"] # name retrieved locally                
            resp = f"{resp},{t}"  
        ret = resp.strip(",")
    except Exception as e:
        ret =  str(e)         
    return ret
def getItemNameLocallyIfExist(t):
    try:       
       
        items = WebFlowItems.objects.filter(itemid =  t.strip() )
        if items.count() == 0:
            return {"fail": "Item does not exist locally"}
        item = items.first() #usually will be the only item in db
        ret = {"success": item.name}
    except Exception as e:
        ret = {"error": str(e)}
    return ret
def  storeItemNameLocally(name, itemid):
    try:
        WebFlowItems(name = name, itemid = itemid).save() #inserts item (name, webflowid)
    except Exception as e:
        pass  # comes here if inserts failed, usually because of constraints violation
    return ""