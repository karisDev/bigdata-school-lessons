from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def get_root():
  return {"Hello": "World"}

@app.get("/write")
def write_root(first_name, last_name, age:int):
  return first_name, last_name, age

@app.get("/get")
def get_root():
  return {"Read": "db"}

if __name__ == '__main__':
  uvicorn.run("main:app", port=8000, reload=True)
