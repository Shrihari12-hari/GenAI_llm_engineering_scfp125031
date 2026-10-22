
import asyncio
from typing import Type
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool


class StockInput(BaseModel):
    product_name: str = Field(description="Name of the product")


class ProductStockTool(BaseTool):
    name: str = "check_product_stock"
    description: str = "Check the available stock of a product."
    args_schema: Type[BaseModel] = StockInput

    async def _arun(self, product_name: str) -> str:
        stock = {
            "laptop": 10,
            "mouse": 25,
            "keyboard": 0,
            "monitor": 7
        }

        await asyncio.sleep(1)

        quantity = stock.get(product_name.lower())

        if quantity is None:
            return f"{product_name} was not found."

        if quantity == 0:
            return f"{product_name} is out of stock."

        return f"{product_name}: {quantity} units available."

    def _run(self, product_name: str) -> str:
        return asyncio.run(self._arun(product_name))


async def main():
    stock_tool = ProductStockTool()

    result = await stock_tool.ainvoke({
        "product_name": "laptop"
    })

    print(result)


if __name__ == "__main__":
    asyncio.run(main())
