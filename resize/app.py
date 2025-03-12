# app.py
# Goal: Retourner l'image redimensionnée avec le nom d'origine en forçant l'extension à ".jpg",
# car le format de sortie est toujours JPEG.

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
import subprocess
import tempfile
import os
import io

app = FastAPI()

@app.post("/resize")
async def resize_image(file: UploadFile = File(...)):
    # Créer des fichiers temporaires pour l'entrée et la sortie
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as input_file:
        input_path = input_file.name
        input_file.write(await file.read())
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as output_file:
        output_path = output_file.name
    
    # Appeler le script rsz.py pour redimensionner l'image
    try:
        subprocess.run(["python", "rsz.py", input_path, output_path], check=True)
    except subprocess.CalledProcessError as e:
        return {"error": f"Erreur lors du redimensionnement : {e}"}
    
    # Lire l'image redimensionnée
    with open(output_path, "rb") as f:
        image_data = f.read()
    
    # Supprimer les fichiers temporaires
    os.remove(input_path)
    os.remove(output_path)
    
    # Forcer l'extension à .jpg, car le résultat est toujours en JPEG
    original_filename = file.filename
    base, _ = os.path.splitext(original_filename)
    final_filename = f"{base}.jpg"
    
    # Retourner l'image redimensionnée avec le nom de fichier approprié
    response = StreamingResponse(io.BytesIO(image_data), media_type="image/jpeg")
    response.headers["Content-Disposition"] = f"attachment; filename={final_filename}"
    return response
