from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "API is working"
    }


@app.get("/predict")
def predict(text: str):
    return {
        "input": text,
        "result": f"You sent: {text}"
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    