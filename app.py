import threading
import time
from flask import Flask, render_template, jsonify
from config import Config
import database
import monitor

app = Flask(__name__)
app.config.from_object(Config)

# Inicializace DB při startu
database.init_db()

def background_logger():
    """Smyčka běžící na pozadí, která ukládá data do DB."""
    monitor.psutil.cpu_percent(interval=None)
    
    while True:
        try:
            metrics = monitor.get_live_metrics()
            database.log_metrics(metrics)
        except Exception as e:
            print(f"Chyba při zápisu do DB: {e}")
        time.sleep(Config.MONITOR_INTERVAL)

# Spuštění daemon vlákna
threading.Thread(target=background_logger, daemon=True).start()

@app.route('/')
def index():
    sys_info = monitor.get_system_info()
    metrics = monitor.get_live_metrics()
    history = database.get_history(10)
    return render_template('index.html', sys_info=sys_info, metrics=metrics, history=history)

@app.route('/api/metrics')
def api_metrics():
    """API endpoint pro AJAX obnovování dat."""
    return jsonify(monitor.get_live_metrics())

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
