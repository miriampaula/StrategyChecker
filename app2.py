import requests
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

long_color = "#C2C5BA"
short_color = "#DDC0BA"

placeholder_ema_values = {
        "short": 1.5,  # Placeholder value for short EMA
        "long": 1.8    # Placeholder value for long EMA, ensuring short EMA > long EMA
    }




def get_last_ema(cross, timeframe, timeperiod):
    url = "https://api.twelvedata.com/ema?symbol={}&interval={}&apikey=$apikey&time_period={}"
    response = requests.get(url.format(cross, timeframe, timeperiod)).json()
    return float(response['values'][0]['ema'])

def get_trend_color(ema_short, ema_long):
    return long_color if ema_short > ema_long else short_color

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route("/", methods=["GET"])
def index():
    symbols = ["GBP/CAD", "AUD/USD", "EUR/USD", "USD/CHF", "GBP/JPY"]
    timeframes = ["5min", "1h", "4h", "1day"]
    ema_periods = {"short": 9, "long": 21}

    
    context = {}
    for symbol in symbols:
        for timeframe in timeframes:
            ema_short = get_last_ema(symbol, timeframe, ema_periods["short"])
            ema_long = get_last_ema(symbol, timeframe, ema_periods["long"])
            
            key = f"{symbol.replace('/', '')}_TREND_{timeframe.upper()}"
            context[key] = get_trend_color(ema_short, ema_long)

    return render_template("index.html", **context)


"""
 context = {}
    for symbol in symbols:
        for timeframe in timeframes:
            ema_short = get_last_ema(symbol, timeframe, ema_periods["short"])
            ema_long = get_last_ema(symbol, timeframe, ema_periods["long"])
            
            key = f"{symbol.replace('/', '')}_TREND_{timeframe.upper()}"
            context[key] = get_trend_color(ema_short, ema_long)

    return render_template("index.html", **context)
 """


    

if __name__ == "__main__":
    app.run(debug=True)
