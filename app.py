import numpy as np
from flask import Flask, request, jsonify, render_template
import os
page@app.route(‘/’)
def home(): 
    return render_template(‘index.html’) 

if __name__ == “__main__”: 
    port=int(os.environ.get(‘PORT’,5000))    
    app.run(port=port,debug=True,use_reloader=False)
