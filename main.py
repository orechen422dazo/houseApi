import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
from typing import List

app = FastAPI()

class Property(BaseModel):
    id: int
    name: str
    age: int
    size: float
    type: str
    image: str

properties = [
    Property(id=1, name="サンシャインマンション", age=5, size=65.5, type="マンション", image="house1.png"),
    Property(id=2, name="グリーンヒルズ", age=10, size=75.0, type="マンション", image="house2.png"),
    Property(id=3, name="オーシャンビュー", age=2, size=85.5, type="マンション", image="house3.png"),
]

@app.get('/')
async  def first_page():
    return '最初のページです'

@app.get("/properties", response_model=List[Property])
async def get_all_properties():
    return properties

@app.get("/properties/{property_id}", response_model=Property)
async def get_property(property_id: int):
    for prop in properties:
        if prop.id == property_id:
            return prop
    raise HTTPException(status_code=404, detail="Property not found")

@app.get("/images/{image_name}")
async def get_image(image_name: str):
    image_path = f"Image/{image_name}"
    if os.path.exists(image_path):
        return FileResponse(image_path)
    raise HTTPException(status_code=404, detail="Image not found")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)