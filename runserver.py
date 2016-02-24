import logging

from composeui import app

logging.basicConfig(level=logging.DEBUG)

app.run(host='0.0.0.0', debug=False, threaded=True)
