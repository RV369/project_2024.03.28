import os
import uuid
from datetime import date

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.db import get_session, init_db
from src.models import UploadedFile

app = FastAPI()

UPLOADED_FILES_PATH = 'uploaded_files/'


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.get('/V1/')
async def find(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(UploadedFile))
    files = result.scalars().all()
    return [
        UploadedFile(
            filename=file.filename, date=file.upload_date, uid=file.uid
        )
        for file in files
    ]


@app.post('/v2/upload')
async def upload(
    file: UploadFile = File(...), session: AsyncSession = Depends(get_session)
):
    name = file.filename
    extension = name.split(".")[1]
    file.filename = uuid.uuid4()
    file.filename = str(file.filename) + '.' + f'{extension}'
    with open(f'{UPLOADED_FILES_PATH}{file.filename}', 'wb') as uploaded_file:
        file_content = await file.read()
        uploaded_file.write(file_content)
        uploaded_file.close()
        new_file = UploadedFile(
            uid=file.filename, filename=name, upload_date=date.today()
        )
        session.add(new_file)
        await session.commit()
        await session.refresh(new_file)
        return file.filename, new_file


@app.get("/v1/download/{UUID}")
async def download_file(UUID):
    file_path = f"{UPLOADED_FILES_PATH}{UUID}"
    if os.path.exists(file_path):
        return FileResponse(
            file_path,
            headers={"Content-Disposition": f"attachment; filename={UUID}"},
        )
    else:
        raise HTTPException(status_code=404, detail="File not found")