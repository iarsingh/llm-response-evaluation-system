from llmeval.ops import router as ops_router
from fastapi import FastAPI
from llmeval.score import evaluate

app = FastAPI()
app.include_router(ops_router, prefix="/v1")


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.post("/evaluate")
def post_evaluate(body: dict):
    return evaluate(body.get("answer"), body.get("gold"), body.get("context"))
