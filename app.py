from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from IPython.display import display, HTML
import markdown2
from scriptModel import load_models, enter_company, choose_competitor, to_markdown

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class Company(BaseModel):
    name: str

model, nlp = load_models()

@app.route("/", methods=["GET", "POST"])
async def home(request: Request):
    if request.method == "POST":
        form_data = await request.form()
        company_name = form_data.get("company_name", "")
        # Process the form submission
        competitors = enter_company(model, nlp, company_name)
        return templates.TemplateResponse("home.html", {"request": request, "company_name": company_name, "competitors": competitors})
    else:
        # Handle GET request, render the initial form
        return templates.TemplateResponse("home.html", {"request": request})



@app.post("/compare/", response_class=HTMLResponse)
async def compare_competitors(request: Request, company_name: str = Form(...), competitor: str = Form(...)):
    result = choose_competitor(model, company_name, competitor)
    result=to_markdown(result)
    result=markdown2.markdown(result)
    return templates.TemplateResponse("home.html", {"request": request, "result": result})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
