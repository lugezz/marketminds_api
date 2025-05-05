from datetime import datetime

import pandas as pd


def get_datetime_from_str(date_str: str, format_str: str = '%Y-%m-%dT%H:%M:%S.%fZ') -> datetime | None:
    """ Convertir un valor de tipo str a datetime.
    :param date_str: La fecha en formato string en un formato como "2006-10-19T00:00:00.000Z"
    """
    if date_str:
        # Convertir la cadena a un objeto datetime
        date_obj = pd.to_datetime(date_str, format=format_str, errors='coerce')
        if pd.isna(date_obj):
            return None
        else:
            dt_with_tz = date_obj.to_pydatetime()
            return dt_with_tz
    else:
        return None


def si_no_a_bool(value: str) -> bool:
    """ Convertir un valor de tipo str a bool.
    """
    if value.lower() == "si":
        return True
    elif value.lower() == "no":
        return False
    else:
        return None


def serialize_specific_value(value):
    resp = value
    if not isinstance(value, (str, int, float, datetime)):
        resp = str(value)
    elif isinstance(value, datetime):
        resp = value.strftime('%Y-%m-%d')
    return resp


def dict_all_serialized(data_dict: dict) -> dict:
    """ Function to ensure all values in the dictionary are JSON serializable. """
    def serialize_dict(this_dict):
        for key, value in this_dict.items():
            if isinstance(value, dict):
                this_dict[key] = serialize_dict(value)
            elif isinstance(value, list):
                this_dict[key] = [serialize_specific_value(item) for item in value]
            else:
                this_dict[key] = serialize_specific_value(value)
        return this_dict

    return serialize_dict(data_dict)
