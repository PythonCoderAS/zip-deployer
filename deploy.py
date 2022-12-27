import shutil
from pathlib import Path, PurePath
from zipfile import BadZipFile, ZipFile

from fastapi import FastAPI, Form, UploadFile, HTTPException
from pydantic.main import BaseModel

from config import secret_key, export_to, new_url

app = FastAPI()
export_path = Path(export_to)
export_path.mkdir(parents=True, exist_ok=True)

class Response(BaseModel):
    new_url: str
@app.post("/", response_model=Response)
async def root(key: str = Form(), *, data: UploadFile):
    if key != secret_key:
        raise HTTPException(status_code=403, detail="Invalid key.")
    dirname = PurePath(data.filename).stem # The target directory name
    dest_dir = (export_path / dirname)
    if dest_dir.exists():
        raise HTTPException(status_code=409, detail="File already exists.")
    try:
        zipfile = ZipFile(data.file, "r")
    except BadZipFile:
        raise HTTPException(status_code=400, detail="Invalid zip file.")
    zipfile.extractall(dest_dir)
    return Response(new_url=new_url % dirname)

