from base64 import encode
from web3 import Web3
import json
import hashlib
from datetime import datetime

# sends transaction and returns the tx.id
def sendTransaction(message):
    w3 = Web3(Web3.HTTPProvider('https://goerli.infura.io/v3/17b153bb0c384e5995ee7a12b450370e'))
    address = '0x58Df929b9Aa49892A915450a9A8c26f936F06dbA'
    privateKey = "0x5f4800cfb7f42c232ed01ce7b601df3be64d0d5f5d3ab4624c5d1465715fe06d"
    nonce = w3.eth.getTransactionCount(address)
    gasPrice = w3.eth.gasPrice
    value = w3.toWei(0, 'ether')

    tx_fields = {
        'nonce': nonce,
        'gasPrice':gasPrice,
        'gas':100000,
        'to':'0x0000000000000000000000000000000000000000',
        'value':value,
        'data': message.encode('utf-8'),
        }

    signedTx = w3.eth.account.signTransaction(tx_fields, privateKey)
    
    tx = w3.eth.sendRawTransaction(signedTx.rawTransaction)
    txId = w3.toHex(tx)
    return txId

# creates a json file containing the data and returns its sha256 encryption
def sha_from_json_of_article(article):  

    data = {
        'title': article.title,
        'description': article.description,
        'content': article.content,
        'author': str(article.author),
        'date published': str(article.published_date),
    }

    json_object = json.dumps(data, indent=4)
    
    with open(f'newspaper/static/json_from_articles/{article.pk}.json', "w") as myjson:
        myjson.write(json_object) 

    return(hashlib.sha256(json_object.encode("utf-8")).hexdigest())

# returns how long ago every article was published (weeks, days and hours) inside a dictionary structured {pk_of_article: age}
def get_articles_age(articles, date_now):
    ages={}

    for article in articles:
        date_pub = article.published_date
        delta_in_seconds = int((date_now - date_pub).total_seconds())
        age = ""

        years   = divmod(delta_in_seconds, 31536000)
        days    = divmod(years[1], 86400)     
        hours   = divmod(days[1], 3600)                

        if years[0] >= 1:
            if years[0] >=2:
                age = " ".join((age, str(years[0]), "years and", str(days[0]), "days ago"))
            else:
                age = " ".join((age, str(years[0]), "year and", str(days[0]), "days ago"))
        
        #age is less then a year (use only days and hours)
        else:
            if days[0]>=1:
                
                # if the day number is round -> don't show zero hours
                if hours[0] < 1:
                    age = " ".join((age, str(days[0]), "days ago"))
                else: 
                    if hours[0] ==1:
                        age = " ".join((age, str(days[0]), "days and", str(hours[0]), "hour ago"))
                    else:
                        age = " ".join((age, str(days[0]), "days and", str(hours[0]), "hours ago"))

            # age is less then a day (only hours)
            else:
                if hours[0]>=2:
                    age = " ".join((age, str(hours[0]), "hours ago"))
                elif hours[0] == 1:
                    age = " ".join((age, str(hours[0]), "hour ago"))

                #age is less then 1 hour 
                else:
                    age = "less than one hour ago..."
        
        ages[article.pk] = age

    return(ages)
