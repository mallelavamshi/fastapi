from fastapi import APIRouter, HTTPException
from ..models.schemas import ProcessRequest, ProcessResponse
from ..core.image_processor import (
    get_image_files, process_google_drive_link, process_image,
    create_excel_with_images, convert_to_pdf
)
import os
import tempfile
import shutil

router = APIRouter()

@router.post("/process-images", response_model=ProcessResponse)
async def process_images(request: ProcessRequest):
    try:
        if request.input_type == "local_folder":
            if not os.path.exists(request.path):
                raise HTTPException(status_code=404, detail="Folder not found")
            folder_path = request.path
            image_files = get_image_files(folder_path)
            output_dir = folder_path
            
        else:  # Google Drive
            output_dir = os.path.join(os.path.expanduser("~"), "Downloads")
            temp_dir, image_files = process_google_drive_link(request.path)
            folder_path = temp_dir

        if not image_files:
            raise HTTPException(status_code=404, detail="No image files found")

        results = []
        for image_file in image_files:
            if request.input_type == "local_folder":
                full_path = os.path.join(folder_path, image_file)
            else:
                full_path = image_file
            
            response = process_image(full_path, request.api_key)
            
            results.append({
                'Image_Name': os.path.basename(full_path),
                'Image_Path': full_path,
                'API_Response': response
            })

        excel_path = create_excel_with_images(results, output_dir)
        pdf_path = convert_to_pdf(excel_path, output_dir)

        return ProcessResponse(
            excel_path=excel_path,
            pdf_path=pdf_path,
            message="Processing completed successfully"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        if request.input_type == "google_drive" and 'temp_dir' in locals():
            shutil.rmtree(temp_dir)