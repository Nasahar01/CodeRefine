from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from ai_engine import analyze_code
from parser import parse_review_response

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class CodeRequest(BaseModel):
    code: str
    language: str
    mode: str  # review or rewrite

@app.get("/", response_class=HTMLResponse)
def frontend(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze")
def analyze(req: CodeRequest):
    if not req.code.strip():
        raise HTTPException(status_code=400, detail="Code is empty")

    ai_output = analyze_code(req.code, req.language, req.mode)

    if req.mode == "review":
        parsed = parse_review_response(ai_output)
    else:
        parsed = {"REWRITTEN_CODE": ai_output.strip()}

    return {"result": parsed}
