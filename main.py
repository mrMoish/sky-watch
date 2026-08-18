from src.api import AeroplanesAPI

def user_interaction() -> None:
    """Взаимодействовать с пользователем через консоль."""

    country = input("Введите название страны: ").strip()

    api = AeroplanesAPI()

    try:
        api.get_aeroplanes(country)
    except Exception as error:
        print(f"Не удалось получить данные: {error}")
