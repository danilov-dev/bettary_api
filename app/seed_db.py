"""
Скрипт для заполнения базы данных тестовыми данными.
Запуск: python -m app.scripts.seed_db
"""
import asyncio
from datetime import date, time
from random import randint, uniform

from sqlalchemy.future import select

from app.core.database import init_db, async_session_maker
from app.models.product_model import ProductModel, ProductTypes
from app.models.battery import Battery
from app.models.cell import Cell


async def seed_db():
    """Заполнить базу данных тестовыми данными."""

    # Инициализировать таблицы (если ещё не созданы)
    await init_db()

    async with async_session_maker() as session:
        # Проверить, есть ли уже данные
        result = await session.execute(select(ProductModel))
        if result.scalars().first():
            print("База данных уже содержит данные. Очистите её перед запуском, если нужно.")
            return

        # Создать модели продуктов
        product_models = []

        # Модели батарей
        battery_models_data = [
            {"number": "BM-18650", "type": ProductTypes.BATTERY, "voltage": 3.7, "capacity": 2600, "height": 65.0, "weight": 45.0, "length": 18.0},
            {"number": "BM-21700", "type": ProductTypes.BATTERY, "voltage": 3.7, "capacity": 4800, "height": 70.0, "weight": 68.0, "length": 21.0},
            {"number": "BM-14500", "type": ProductTypes.BATTERY, "voltage": 3.7, "capacity": 800, "height": 50.0, "weight": 20.0, "length": 14.0},
        ]

        for data in battery_models_data:
            pm = ProductModel(**data)
            session.add(pm)
            product_models.append(pm)

        # Модели ячеек
        cell_models_data = [
            {"number": "CM-L100", "type": ProductTypes.CELL, "voltage": 3.2, "capacity": 100, "height": 10.0, "weight": 5.0, "length": 10.0},
            {"number": "CM-L200", "type": ProductTypes.CELL, "voltage": 3.2, "capacity": 200, "height": 15.0, "weight": 8.0, "length": 12.0},
            {"number": "CM-L500", "type": ProductTypes.CELL, "voltage": 3.2, "capacity": 500, "height": 20.0, "weight": 15.0, "length": 15.0},
        ]

        for data in cell_models_data:
            pm = ProductModel(**data)
            session.add(pm)
            product_models.append(pm)

        await session.flush()
        print(f"Создано {len(product_models)} моделей продуктов")

        # Создать батареи
        batteries = []
        for i in range(10):
            model = product_models[i % 3]  # Использовать только модели батарей
            battery = Battery(
                barcode=f"BATT-{2024000 + i}",
                capacity=model.capacity + uniform(-50, 50),
                time_charged=time(hour=randint(0, 23), minute=randint(0, 59)),
                time_discharged=time(hour=randint(0, 23), minute=randint(0, 59)),
                tested_at=date(2024, randint(1, 12), randint(1, 28)),
                product_model_id=model.id
            )
            session.add(battery)
            batteries.append(battery)

        await session.flush()
        print(f"Создано {len(batteries)} батарей")

        # Создать ячейки
        cells = []
        for i in range(20):
            model = product_models[3 + (i % 3)]  # Использовать только модели ячеек
            cell = Cell(
                barcode=f"CELL-{2024000 + i}",
                capacity=model.capacity + uniform(-10, 10),
                time_charged=time(hour=randint(0, 23), minute=randint(0, 59)),
                time_discharged=time(hour=randint(0, 23), minute=randint(0, 59)),
                tested_at=date(2024, randint(1, 12), randint(1, 28)),
                product_model_id=model.id,
                battery_id=batteries[i % len(batteries)].id if i < 15 else None  # Привязать к батарее первые 15
            )
            session.add(cell)
            cells.append(cell)

        await session.flush()
        print(f"Создано {len(cells)} ячеек")

        await session.commit()
        print("\n✅ База данных успешно заполнена тестовыми данными!")
        print(f"   - Моделей продуктов: {len(product_models)}")
        print(f"   - Батарей: {len(batteries)}")
        print(f"   - Ячеек: {len(cells)}")


if __name__ == "__main__":
    asyncio.run(seed_db())