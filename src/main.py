from fastapi import FastAPI, status, HTTPException , Depends 



app = FastAPI()

@app.get("/", status_code=status.HTTP_200_OK)
async def hello(name: str):
    return {f"Hello, {name}"}
