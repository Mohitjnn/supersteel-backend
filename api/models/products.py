from typing import List, Optional
from pydantic import BaseModel, Field


class Color(BaseModel):
    name: str
    hexCode: str
    material: str
    weight: str
    details: List[str]


class Image(BaseModel):
    color: str
    imageSrc: str


class CreateProduct(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    subtitle: str
    price: float
    BestSeller: bool
    category: str
    type: str
    colors: List[Color]
    images: List[Image]
