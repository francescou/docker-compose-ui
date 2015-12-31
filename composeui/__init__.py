from flask import Flask
app = Flask(__name__, static_url_path='')

import composeui.main
import composeui.host
import composeui.auth
