from src.api import AeroplanesAPI
from src.aeroplane import Aeroplane
from operator import attrgetter


def user_interaction() -> None:
    """Взаимодействовать с пользователем через консоль."""

    country = input("Введите название страны: ").strip()

    api = AeroplanesAPI()

    try:
        raw_states = api.get_aeroplanes(country)
    except Exception as error:
        print(f"Не удалось получить данные: {error}")
        return
    aeroplanes = Aeroplane.cast_to_object_list(raw_states)

    while True:
        str_top_n_raw = input("Введите количество самолётов для вывода в топ N: ").strip()
        try:
            top_n_raw = int(str_top_n_raw)
            break
        except ValueError:
            print("🚨 Укажите число")
    aeroplanes.sort(key=attrgetter("altitude"), reverse=True)
    for i in range(top_n_raw):
        print(aeroplanes[i])

    print()

    input_origin_country = input("Получить самолеты по стране их регистрации. Введите страну регистрации:").strip()

    result = [ aeroplane for aeroplane in aeroplanes if aeroplane.origin_country.lower() == input_origin_country.lower()]

    for aeroplane in result:
        print(aeroplane)

if __name__ == "__main__":
    user_interaction()
