from secrets import compare_digest, token_urlsafe
from urllib.parse import unquote

from fastapi import FastAPI, status, Body, Response, Header
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel, Extra


class SendEmailOrder(BaseModel):
    user: str
    email: str
    url: str

    class Config:
        extra = Extra.ignore


app = FastAPI(docs_url=None, redoc_url=None)
api_key = token_urlsafe(64)
storage = dict()


@app.on_event('startup')
def start():
    import logging
    logging.getLogger('uvicorn.error').info(f'Api Key: {api_key}')


@app.get('/')
def main():
    return FileResponse('mail.html')


@app.get('/get-mail')
def get_mail(q: str = None, authorization: str = Header(...)):
    if not compare_digest(authorization, api_key):
        return Response(status_code=403)
    q = unquote(q)
    try:
        return JSONResponse(content={'data': storage[q]})
    except KeyError:
        return Response(status_code=404)


@app.post('/send', status_code=status.HTTP_202_ACCEPTED)
def endpoint_send_email(model: SendEmailOrder):
    storage[model.email] = model.url
    storage[model.user] = model.url


@app.post('/validate')
def endpoint_validate_email(email: str = Body(..., )):
    return JSONResponse(content={'email': email})
