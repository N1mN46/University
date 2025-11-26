from flask import Flask, request, Response, jsonify
import requests
import datetime 

app = Flask(__name__)
 #Easy - Сервер та запит Hello World
@app.route("/")
def hello_world():
    return "Hellow world"

#Easy-Medium 
@app.route("/currency")
def currency():
        today = request.args.get("today")
        key = request.args.get("key")
        return "USD - 41.5"

#Medium
@app.route("/content-type")
def content_type_handler():
     content_type = request.headers.get('Content-Type')
     message = "Сервер"
     if content_type == 'application/json':
          return jsonify({
               "message": message,
               "type": "JSON",
               "status": "success"
          })
     elif content_type =='application/xml':
          xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
          <root>
                <message>{message}</message>
                <type>XML</type>
            </root>
            """
          return xml_content, 200, {'Content-Type': 'application/xml'}
     else:
        return f"Type: Plain Text. Message: {message}"

#Medim-Hard
def get_usd_rate(date_str=None):
    base_url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange"
    params = {
        "valcode": "USD",
        "json": ""
    }
    
    if date_str:
        params["date"] = date_str

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status() # Перевірка на помилки мережі
        data = response.json()
        
        if data:
            return data[0]['rate'], data[0]['exchangedate']
        return None, None
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None, None

@app.route("/usd-curr")
def usd_curr():
    param_value = request.args.get("param")
    
    if not param_value:
        return "Будь ласка, вкажіть параметр: ?param=today або ?param=yesterday", 400

    rate = None
    date_display = None

    if param_value == 'today':
        rate, date_display = get_usd_rate()
        
    elif param_value == 'yesterday':
        yesterday_obj = datetime.date.today() - datetime.timedelta(days=1)
        yesterday_str = yesterday_obj.strftime("%Y%m%d")
        rate, date_display = get_usd_rate(yesterday_str)

    else:
        return "Невірний параметр. Використовуйте 'today' або 'yesterday'", 400

    if rate:
        return jsonify({
            "currency": "USD",
            "date": date_display,
            "rate": rate,
            "period": param_value
        })
    else:
        return "Не вдалося отримати дані від НБУ", 502
    
if __name__ == '__main__':
    app.run(port=8000)
