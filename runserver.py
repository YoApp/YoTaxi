from yotaxi import app
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # Cache template for fast loading
    app.jinja_env.cache = {}
    app.run(host='0.0.0.0', port=port, debug=True)
