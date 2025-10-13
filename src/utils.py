from typing import List, Dict, Any

def validate_stock_data(data: List[Dict[str, Any]]) -> bool:
    """
    Verinin geçerli olup olmadığını kontrol eder.
    Örneğin: her satırda 'symbol' ve 'price' alanı olmalı.
    """
    if not data:
        return False
    required_keys = {'symbol', 'price'}
    for row in data:
        if not required_keys.issubset(row.keys()):
            return False
    return True

def format_stock_data(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Veriyi standart formata çevirir (örnek: price'ı float yapar).
    """
    for row in data:
        if 'price' in row:
            row['price'] = convert_to_float(row['price'])
    return data

def parse_csv_row(row: List[str], headers: List[str]) -> Dict[str, Any]:
    """
    CSV satırını dict olarak döndürür.
    """
    return {header: value for header, value in zip(headers, row)}

def convert_to_float(value: Any) -> float:
    """
    Değeri float'a çevirir. Hata durumunda 0 döner.
    """
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0

def is_data_updated(old_data: List[Dict[str, Any]], new_data: List[Dict[str, Any]]) -> bool:
    """
    Yeni veri eski veriden farklı mı kontrol eder.
    """
    return old_data != new_data
