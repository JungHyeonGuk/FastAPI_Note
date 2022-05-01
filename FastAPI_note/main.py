
from multiprocessing.connection import wait
from fastapi import FastAPI, Request, Form, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import copy 

app = FastAPI()
templates = Jinja2Templates(directory="templates")

notes = {
    # "1": {
    #     "body":"first content", 
    #     "pw":""
    #     },
    # "2": {
    #     "body":"second content", 
    #     "pw":"1234"
    #     }
}

# (서버 포트로 이동하기)
def redirect_home():
    return RedirectResponse("http://127.0.0.1:8000/", status_code=status.HTTP_303_SEE_OTHER)


# 검색과 노트 보여주기
@app.get('/', response_class=HTMLResponse) 
def main(request: Request, search: str = ''):
    search_notes = {}
    if search is None:
        search_notes = copy.deepcopy(notes);
    else:
        for key, value in notes.items():
            if search in value['body']:
                search_notes[key] = copy.deepcopy(value)
    
    print(search_notes)
    # 한줄만 보이기
    for key, value in search_notes.items():
        search_notes[key]["body"] = search_notes[key]["body"].split('\n')[0]
        
    return templates.TemplateResponse("main.html", {"request":request, "notes":search_notes})


# 패스워드가 일치하면 노트 열기
@app.post('/note') 
async def note(request: Request, id: str = Form(""), pw: str = Form("")):
    print(notes)
    if notes[id]["pw"] != "":
        if notes[id]["pw"] == pw:
            return templates.TemplateResponse("note.html", {"request":request, "id":id, "body":notes[id]["body"]})
        else:
            return redirect_home()
    else:
        return templates.TemplateResponse("note.html", {"request":request, "id":id, "body":notes[id]["body"]})
    

# 노트 지우기
@app.post('/note/delete')
async def note_delete(request: Request, id: str = Form("")):
    del(notes[id])
    return redirect_home()


# 노트 편집
@app.post('/note/edit')
async def note_edit(request: Request, id: str = Form("")):
    return templates.TemplateResponse("note_edit.html", {"request":request, "id":id, "body":notes[id]["body"], "pw":notes[id]["pw"]})


# 노트 편집 완료
@app.post('/note/edit/complete')
async def note_edit_complete(request: Request, id: str = Form(""), body: str = Form(""), pw: str = Form("")):
    notes[id]["body"] = body
    notes[id]["pw"] = pw
    return redirect_home()


# 새 노트
@app.get('/note/new', response_class=HTMLResponse) 
async def main(request: Request):
    newId = str(len(notes) + 1)
    notes[newId] = {
        "body":"",
        "pw":""
    }
    return RedirectResponse("http://127.0.0.1:8000/", status_code=status.HTTP_303_SEE_OTHER)