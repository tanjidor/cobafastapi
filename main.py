from fastapi import FastAPI, Request, UploadFile, HTTPException, Form, status
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated

import aiofiles
from io import StringIO
import utils

app = FastAPI() 
app.mount("/gambar", StaticFiles(directory="gambar"), name="gambar")
app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
async def main():
    return {'messages': 'api grafik pakDosen'}

@app.post('/upload')
async def upload(file: UploadFile, titel: Annotated[str, Form()]):
    try:
        contents = await file.read()
        async with aiofiles.open(file.filename, 'wb') as f:
            await f.write(contents)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='There was an error uploading the file',
        )
    finally:
        await file.close()
    # print(type(contents))
    s = str(contents, 'utf-8')
    data = StringIO(s)
    df = utils.cleaning_data(data)
    jing, tod = utils.get_tabel_data(df)
    utils.fakultas_bar(tod)
    utils.draw_tabel(jing, 'fakultas', 'Absensi Dosen Fakultas Teknik\n{}'.format(titel))
    jing, tod = utils.get_tabel_data(df, prodi='Teknik Informatika')
    utils.draw_tabel(jing, 'prodi', 'Absensi Dosen Prodi Teknik Informatika\n{}'.format(titel), nama_file='tabel-ti')
    jing, tod = utils.get_tabel_data(df, prodi='Teknik Sipil')
    utils.draw_tabel(jing, 'prodi', 'Absensi Dosen Prodi Teknik Sipil\n{}'.format(titel), nama_file='tabel-ts')
    jing, tod = utils.get_tabel_data(df, prodi='Teknik Industri')
    utils.draw_tabel(jing, 'prodi', 'Absensi Dosen Prodi Teknik Industri\n{}'.format(titel), nama_file='tabel-tind')
    return {'messages': 'Uploaded'}

@app.get('/persentase-fakultas')
async def persentase_fak(request: Request):
    img = 'persentase-kehadiran-fakultas.png' 
    return {'img_url': request.url_for('gambar', path=img)}

@app.get('/tabel-fakultas')
async def tabel_fak(request: Request):
    img = 'tabel-fakultas.png' 
    return {'img_url': request.url_for('gambar', path=img)}

@app.get('/tabel-ti')
async def tabel_ti(request: Request):
    img = 'tabel-ti.png' 
    return {'img_url': request.url_for('gambar', path=img)}

@app.get('/tabel-ts')
async def tabel_ts(request: Request):
    img = 'tabel-ts.png' 
    return {'img_url': request.url_for('gambar', path=img)}

@app.get('/tabel-tind')
async def tabel_tind(request: Request):
    img = 'tabel-tind.png' 
    return {'img_url': request.url_for('gambar', path=img)}

