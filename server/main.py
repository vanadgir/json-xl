from fastapi import FastAPI, Request, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.encoders import jsonable_encoder
import xlsxwriter
import io
import logging
import re
from typing import Any

logger = logging.getLogger("uvicorn.error")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def sanitize_filename(filename: str) -> str:
    """Sanitize the filename to prevent path traversal and enforce .xlsx extension."""
    filename = re.sub(r"[^\w\-.]", "_", filename)
    if not filename.endswith(".xlsx"):
        filename += ".xlsx"
    return filename

def json_to_excel(data: Any) -> io.BytesIO:
    """
    Convert JSON data (list of dicts or dict) to an Excel file in memory.
    Returns a BytesIO object.
    """
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()
    try:
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
        return output
    except Exception as e:
        logger.error(f"Excel generation failed: {e}")
        raise

@app.post("/convert")
async def convert_json_to_excel(request: Request, filename: str = Query("output.xlsx")):
    """
    Convert posted JSON to an Excel file and return as a download.
    Accepts a JSON body (list of dicts or dict) and a filename query param.
    """
    try:
        json_data = await request.json()
    except Exception:
        logger.warning("Invalid JSON received.")
        raise HTTPException(status_code=400, detail="Invalid JSON format.")
    data = jsonable_encoder(json_data)
    if not data:
        raise HTTPException(status_code=400, detail="No data provided.")
    try:
        output = json_to_excel(data)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to generate Excel file.")
    safe_filename = sanitize_filename(filename)
    return StreamingResponse(
        output,
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': f'attachment; filename="{safe_filename}"'}
    )
