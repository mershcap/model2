from flask import Flask
app=Flask(__name__)

class N:
    def __init__(self):
        self.n=0
    def add(self):
        self.n=self.n+1
        
n=N()

@app.route('/')
def Home():
    n.add()
    return str(n.n)

if __name__=='__main__':
    app.run()

