from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from decouple import config
from openai import OpenAI

app = FastAPI()


app.mount("/css", StaticFiles(directory="frontend/css"), name="css")

templates = Jinja2Templates(directory="frontend/templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse('index.html', context={'request':request})

pipe = None

@app.on_event('startup')
def startup():

    from huggingface_hub import login

    login(config('HUGGING'))
    
    from transformers import pipeline

    pipe = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")


@app.get("/answer")
def read_root(request: Request):
    return pipe('Hola llama 2')


@app.post("/api")
async def read_root2(request: Request):

    json = await request.json()

    client = OpenAI(
        api_key=config('API_KEY'),
    )
    
    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": "eres un experto en ia que contesta preguntas solo de temas relacionados a ella"},
            {"role": "user", "content": f"{json['msg']} Responde con un json y que el valor tenga todo el texto"}
        ]
    )
    
    msg = chat_completion.choices[0].message.content

    return JSONResponse(content={'msg':msg})
