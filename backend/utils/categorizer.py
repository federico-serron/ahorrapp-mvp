"""Categorización automática de transacciones"""

def categorize_transaction(description):
    """Categoriza transacción y detecta ingreso vs gasto"""
    desc_lower = description.lower()
    
    income_keywords = [
        'sueldo', 'salario', 'pago', 'ingreso', 'venta', 
        'bonus', 'ganancia', 'reembolso', 'comisión'
    ]
    
    is_income = any(kw in desc_lower for kw in income_keywords)
    trans_type = 'income' if is_income else 'expense'
    
    categories = {
        'Alimentacion': ['café', 'comida', 'desayuno', 'almuerzo', 'cena', 'restaurant'],
        'Transporte': ['taxi', 'bus', 'uber', 'gasolina', 'metro', 'tren'],
        'Entretenimiento': ['cine', 'película', 'juego', 'música', 'bar', 'pub'],
        'Salud': ['farmacia', 'medicina', 'doctor', 'médico', 'hospital', 'gym'],
        'Servicios': ['internet', 'teléfono', 'electricidad', 'agua', 'gas'],
        'Compras': ['ropa', 'zapatos', 'tienda', 'regalo', 'amazon'],
        'Ingresos': income_keywords,
    }
    
    category = 'Otros'
    for cat, keywords in categories.items():
        if any(kw in desc_lower for kw in keywords):
            category = cat
            break
    
    return category, trans_type
