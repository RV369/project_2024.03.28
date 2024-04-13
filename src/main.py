import os
import uuid
from datetime import date

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.db import get_session, init_db
from src.models import UploadedFile

app = FastAPI()

UPLOADED_FILES_PATH = 'uploaded_files/'


@app.on_event('startup')
async def on_startup():
    await init_db()


class FileSchema(BaseModel):
    uid: str
    filename: str
    date: str


@app.get('/V1/find', response_model=list[FileSchema])
async def find(
    filename: str = None,
    date: str = None,
    UUID: str = None,
    session: AsyncSession = Depends(get_session),
):
    try:
        result = await session.execute(select(UploadedFile))
        find = result.scalars().all()
        if filename and not date and not UUID:
            result = await session.execute(
                select(UploadedFile).filter(UploadedFile.filename == filename),
            )
            find = result.scalars().all()
        elif date and not filename and not UUID:
            result = await session.execute(
                select(UploadedFile).filter(UploadedFile.upload_date == date),
            )
            find = result.scalars().all()
        elif UUID and not filename and not date:
            result = await session.execute(
                select(UploadedFile).filter(UploadedFile.uid == UUID),
            )
            find = result.scalars().all()
        elif filename and date and not UUID:
            result = await session.execute(
                select(UploadedFile).filter(
                    UploadedFile.filename == filename,
                    UploadedFile.upload_date == date,
                ),
            )
            find = result.scalars().all()
        elif filename and UUID and not date:
            result = await session.execute(
                select(UploadedFile).filter(
                    UploadedFile.filename == filename,
                    UploadedFile.uid == UUID,
                ),
            )
            find = result.scalars().all()
        elif UUID and date and not filename:
            result = await session.execute(
                select(UploadedFile).filter(
                    UploadedFile.uid == UUID,
                    UploadedFile.upload_date == date,
                ),
            )
            find = result.scalars().all()
        elif filename and date and UUID:
            result = await session.execute(
                select(UploadedFile).filter(
                    UploadedFile.filename == filename,
                    UploadedFile.upload_date == date,
                    UploadedFile.uid == UUID,
                ),
            )
            find = result.scalars().all()
    except Exception as e:
        raise HTTPException(f'{e}', detail='Ошибка запроса базы данных')
    return [
        FileSchema(uid=c.uid, filename=c.filename, date=c.upload_date)
        for c in find
    ]


@app.post('/v2/upload')
async def upload(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session),
):
    try:
        name = file.filename
        extension = name.split('.')[1]
        file.filename = uuid.uuid4()
        file.filename = str(file.filename) + '.' + f'{extension}'
        with open(
            f'{UPLOADED_FILES_PATH}{file.filename}',
            'wb',
        ) as uploaded_file:
            file_content = await file.read()
            uploaded_file.write(file_content)
            uploaded_file.close()
            new_file = UploadedFile(
                uid=file.filename,
                filename=name,
                upload_date=str(date.today()),
            )
            session.add(new_file)
            await session.commit()
            await session.refresh(new_file)
    except Exception as e:
        raise HTTPException(f'{e}', detail='Ошибка загрузки файла')
    return file.filename


@app.get('/v1/download/{UUID}')
async def download_file(UUID):
    try:
        file_path = f'{UPLOADED_FILES_PATH}{UUID}'
        if os.path.exists(file_path):
            return FileResponse(
                file_path,
                headers={
                    'Content-Disposition': f'attachment; filename={UUID}',
                },
            )
        else:
            raise HTTPException(
                status_code=404, detail='Искомый файл отсутствует',
            )
    except Exception as e:
        raise HTTPException(f'{e}', detail='Ошибка скачивания файла')
