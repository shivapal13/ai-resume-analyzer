from fastapi import FastAPI


app=FastAPI()


@app.get("/")
def TestServer():
    return {"message":"AI Resume Analyser is running"}