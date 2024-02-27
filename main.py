from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse
from decouple import config
from openai import OpenAI

from fastapi import FastAPI, Query
from starlette.requests import Request
from starlette.responses import Response

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
async def verify_webhook(request: Request):
    """
    Update your verify token.
    This will be the Verify Token value when you set up webhook.
    """
    verify_token = "golf1"  # Update with your actual verify token

    # Parse params from the webhook verification request
    hub_mode = request.query_params.get("hub.mode")
    hub_verify_token = request.query_params.get("hub.verify_token")
    hub_challenge = request.query_params.get("hub.challenge")

    # Check if a token and mode were sent
    if hub_mode and hub_verify_token:
        # Check the mode and token sent are correct
        if hub_mode == "subscribe" and hub_verify_token == verify_token:
            # Respond with 200 OK and challenge token from the request
            print("WEBHOOK_VERIFIED")
            return Response(content=hub_challenge, status_code=200)
        else:
            # Responds with '403 Forbidden' if verify tokens do not match
            return Response(status_code=403)

@app.post("/webhook")
async def obtain(request: Request):
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
