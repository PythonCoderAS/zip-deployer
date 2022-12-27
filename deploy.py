import shutil
from pathlib import Path, PurePath
from random import randrange
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
    exists = False
    rand_hash = ".{:x}".format(randrange(0, 2**48))
    if dest_dir.exists():
        dest_dir.rename(dest_dir.with_suffix(rand_hash))
        exists = True
    try:
        try:
            zipfile = ZipFile(data.file, "r")
        except BadZipFile:
            raise HTTPException(status_code=400, detail="Invalid zip file.")
        zipfile.extractall(dest_dir)
    except:
        if dest_dir.exists():
            shutil.rmtree(dest_dir)
        if exists:
            dest_dir.with_suffix(rand_hash).rename(dest_dir)
        raise
    else:
        if exists:
            shutil.rmtree(dest_dir.with_suffix(rand_hash))
    return Response(new_url=new_url % dirname)

