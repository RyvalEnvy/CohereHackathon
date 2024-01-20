from fastapi import FastAPI
from pydantic import BaseModel
from API.src.process_text import return_most_relevant_passage

app = FastAPI()


class PassageRequest(BaseModel):
    input_passage: str
    patent_number: str


@app.post("/similar_passages/")
async def return_similar_passage(passageRequest: PassageRequest):
    passage_request_dict = passageRequest.dict()
    return return_most_relevant_passage(
        passage_request_dict["input_passage"], passage_request_dict["patent_number"]
    )


@app.get("/health/")
async def return_similar_passage():
    return "I be runnin'"
