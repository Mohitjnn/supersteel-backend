from bson import ObjectId
from fastapi import status, File, UploadFile, APIRouter
from api.models.products import CreateProduct
from api.Routes.utils import getResponse, riseHttpExceptionIfNotFound
from api.helpers.save_picture import save_picture, delete_picture
from api.Services import usersService as service

productRoutes = APIRouter()
base = "/products/"
UploadImage = f"{base}image-upload/"

_notFoundMessage = "Could not find product with the given Id."


@productRoutes.get(base)
async def getAll():
    return await service.getAllProducts()


@productRoutes.get(base + "{id}")
async def getById(id: str):
    return await resultVerification(id)


@productRoutes.post(base)
async def insertProduct(data: CreateProduct):
    return await service.insertProduct(data)


@productRoutes.put(base + "{id}", status_code=status.HTTP_204_NO_CONTENT)
async def updateProduct(id: str, data: CreateProduct):
    await resultVerification(id)
    done: bool = await service.updateProduct(id, data)
    return getResponse(
        done, errorMessage="An error occurred while updating the product information."
    )


@productRoutes.delete(base + "{id}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteProduct(id: str):
    product = await resultVerification(id)
    # Delete associated images
    for image in product["images"]:
        delete_picture(image["imageSrc"])
    done: bool = await service.deleteProduct(id)
    return getResponse(done, errorMessage="There was an error.")


@productRoutes.post(UploadImage + "{id}", status_code=status.HTTP_204_NO_CONTENT)
async def uploadProductImage(id: str, color: str, file: UploadFile = File(...)):
    product = await resultVerification(id)
    imageUrl = save_picture(file=file, folderName=f"products/{id}", fileName=color)
    done = await service.saveProductImage(id, color, imageUrl)
    return getResponse(
        done, errorMessage="An error occurred while saving the product image."
    )


# Helpers
async def resultVerification(id: str) -> dict:
    result = await service.getById(ObjectId(id))
    await riseHttpExceptionIfNotFound(result, message=_notFoundMessage)
    return result
