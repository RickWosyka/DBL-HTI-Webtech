from flask import Flask

app = Flask(__name__)


from app import app


@app.route('/')
@app.route('/index')
def index():
    return '''
    <html>
        <head>
            <title>Home Page: Hierarchy Visualisation</title>
            <style> 
            
            #rcorner {
            border-radius: 50px;
            background: #9999FF;
            padding: 20px;
            width: 800px;
            height: 50px;
            margin-left: 325px;
            }
            
            div.t1 {
            width: 150px;
            border: 2px solid black;
            background-color: #6666FF;
            font-family:Russo One;
            margin-left: 20px;
            margin-top: -480px;
            }

            div.t2 {
            width: 150px;
            border: 2px solid black;
            background-color: #6666FF;
            font-family: Russo One;
            margin-left: 760px;
            margin-top: -60px;
            }

            div.u {
            border-radius: 15px;
            background-color: #9999FF;
            width: 275px;
            height: 80px;
            border: 5px solid #4C0099;
            margin-top: -30px;
            }
            
            div.horl {
            border-radius: 15px;
            border: 4px solid #330066;
            margin-top: 5px;
            }
            
            div.vertl {
            border-left: 6px solid #330066;
            height: 500px;
            margin-left: 720px;
            margin-top: 10px;
            }

            </style>
        </head>
        <body background="/static/bg1.jpg">
            <h1 id="rcorner" align= "center" style="color:#000066; font-family:Russo One; font-size:250%;">Hierarchy visualisation</h1>
            <img src="/static/tue_logo.png" style="width:270px; height:100px; margin-left:1240px; margin-top: -20px"> 
            <p style= "font-size:200%; margin-top:-100px;"><b>Welcome to our homepage!</b></p>
            <div class="u">
            <p style= "font-size:120%; margin-left: 10px;"><b>Upload here your dataset file:</b></p>
            <button type="button" onclick="alert('Your file has been uploaded!')" style="margin-left: 10px; margin-top: -10px;">Upload</button>
            </div>
            <div class="horl"></div>
            <div class="vertl"></div>
            <div class="t1"><p align="center" style= "font-size:110%;"><b>Visualisation 1:</b></p></div>
            <div class="t2"><p align="center" style= "font-size:110%;"><b>Visualisation 2:</b></p></div>
            <br>
            <br>
            <br>
            <br>
            <br>
            <br>
            <br>
            <br>
            <br>
            <br>
            <br>
            <br>
            <br>
            <br>
            <br>
            <br>
            <br>
            <br>
            <br>
            <br>
            <br>
            <br>
            <br>
            <br>
            Made by: <b>Almir Šahman, Dave Cornelis Leonardus Emons, 
            Raffaello Claudio Poritz, Richard Jacobus Rumoldus Schutte,
            Rick Theodorus Leonardus Wosyka & Ying Huang</b>
        </body>
    </html>'''