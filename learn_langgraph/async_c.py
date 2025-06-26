import asyncio
from pydantic import BaseModel,Field
from pydantic.types import Annotated
class Config(BaseModel):
    name: str |int 
    age: int |None = 20
    weight: Annotated[int |None, Field(description="weight in kg", ge=0, le=100)] = 75

async def main():
    config = Config(name="John", age=30, )
    print(config)

if __name__ == "__main__":
    asyncio.run(main())

