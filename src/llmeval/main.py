from fastapi import FastAPI
from llmeval.score import evaluate

app = FastAPI()


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.post("/evaluate")
def post_evaluate(body: dict):
    return evaluate(body.get("answer"), body.get("gold"), body.get("context"))
