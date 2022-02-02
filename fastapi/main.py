from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def index():
    return {"message": "Hello 新世界 2"}
