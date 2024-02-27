from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse
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

@app.get("/webhook")
async def whatsapp_webhook(request: Request):
    print(request.json())
    return {"message": "Hello World"}

@app.post("/webhook")
def obtain(request: Request):
    return {"message": "OK"}

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse('index.html', context={'request':request})

@app.get("/js")
def read_root(request: Request):
    return FileResponse('frontend/js/index.js')

@app.get("/css")
def read_root(request: Request):
    return FileResponse('frontend/css/chatbot.css')

@app.post("/api")
async def read_root2(request: Request):

    json = await request.json()

    '''from pathlib import Path
    
    speech_file_path = Path(__file__).parent / "speech.mp3"
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input="Piensa en mi de vez en cuando"
    )
    response.stream_to_file(speech_file_path)'''

    response = API(
        url="https://papinnovacin.com/", # Your store URL
        consumer_key=config('USERNAME_WOOCOMERCE'), # Your consumer key
        consumer_secret=config('PASSWORD_WOOCOMERCE'), # Your consumer secret
        version="wc/v3" # WooCommerce WP REST API version
    ).get('products')


    if response.status_code==200:
        print(response.json())

    '''client = OpenAI(
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
    
    msg = chat_completion.choices[0].message.content'''

    return JSONResponse(content={'msg':5})
