from config.settings import app_settings


def normalize_phone_number(value: str):
    if value.startswith("+98") and value[3] == 0:
        value = f"{app_settings.phone_number_region_code}{value[4:]}"
    elif value.startswith("0"):
        value = f"{app_settings.phone_number_region_code}{value[1:]}"

    return value
