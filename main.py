from fastapi import FastAPI

app=FastAPI()

@app.get("/home")
def hello():
    return {'message':'Hello World'}


@app.get('/about')
def about():
    return {'message':'This is the message from the about route'}