from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.generator import generate_dockerfile

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate-dockerfile")
async def generate_dockerfile_endpoint(
    code: str = Form(None),
    file: UploadFile = File(None)
):
    try:
        if file:
            code_content = (await file.read()).decode("utf-8")
        else:
            code_content = code

        dockerfile = generate_dockerfile(code_content)
        return JSONResponse(content={"dockerfile": dockerfile})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
