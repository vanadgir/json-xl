from fastapi import FastAPI, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.encoders import jsonable_encoder
import xlsxwriter
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 127.0.0.1:5500 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/convert")
async def convert_json_to_excel(request: Request, filename: str = Query("output.xlsx")):
    json_data = await request.json()
    data = jsonable_encoder(json_data)

    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()

    # turn keys, values into headers, rows
    if isinstance(data, list) and data:
        headers = data[0].keys()
        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num, header)
        for row_num, item in enumerate(data, start=1):
            for col_num, (key, value) in enumerate(item.items()):
                worksheet.write(row_num, col_num, str(value))
    elif isinstance(data, dict):
        for row_num, (key, value) in enumerate(data.items()):
            worksheet.write(row_num, 0, key)
            worksheet.write(row_num, 1, str(value))
    else:
        worksheet.write(0, 0, "Invalid JSON format")

    workbook.close()
    output.seek(0)
    
    if not filename.endswith(".xlsx"):
        filename += ".xlsx"

    return StreamingResponse(
        output,
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': f'attachment; filename="{filename}"'}
    )
