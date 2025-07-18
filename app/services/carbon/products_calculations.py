from typing import List, Dict, Union
from enum import Enum

class EmissionFactor(Enum):
    # Cárnicos
    BEEF = ("beef", 27.0)
    PORK = ("pork", 12.1)
    CHICKEN = ("chicken", 6.9)
    # Lácteos
    MILK = ("milk", 1.34)
    CHEESE = ("cheese", 9.8)
    # Frutas y verduras
    LOCAL_PRODUCE = ("local_produce", 0.5)
    GREENHOUSE_PRODUCE = ("greenhouse_produce", 2.1)
    IMPORTED_PRODUCE = ("imported_produce", 3.3)
    # Ropa y textiles
    TSHIRT = ("tshirt", 2.1)
    JEANS = ("jeans", 8.5)
    SHOES = ("shoes", 5.2)
    # Electrónicos
    SMARTPHONE = ("smartphone", 75.0)
    LAPTOP = ("laptop", 230.0)
    TV = ("tv", 360.0)
    # Limpieza
    DETERGENT = ("detergent", 1.2)
    SOFTENER = ("softener", 0.8)
    CLEANER = ("cleaner", 0.6)

    def __init__(self, id: str, factor: float):
        self.id = id
        self.factor = factor

    @staticmethod
    def from_id(id: str):
        for item in EmissionFactor:
            if item.id == id:
                return item
        raise ValueError(f"Invalid product_type: {id}")


class TransportAdjust(Enum):
    LOCAL = ("local", 0.0)
    REGIONAL = ("regional", 0.2)
    NATIONAL = ("national", 0.4)
    INTERNATIONAL = ("international", 0.8)

    def __init__(self, id: str, adj_value: float):
        self.id = id
        self.adj_value = adj_value

    @staticmethod
    def from_id(id: str):
        for item in TransportAdjust:
            if item.id == id:
                return item
        raise ValueError(f"Invalid transport: {id}")


class PackagingAdjust(Enum):
    NONE = ("none", 0.0)
    MINIMAL = ("minimal", 0.1)
    EXCESSIVE = ("excessive", 0.3)

    def __init__(self, id: str, adj_value: float):
        self.id = id
        self.adj_value = adj_value

    @staticmethod
    def from_id(id: str):
        for item in PackagingAdjust:
            if item.id == id:
                return item
        raise ValueError(f"Invalid packaging: {id}")


class RefrigerationAdjust(Enum):
    AMBIENT = ("ambient", 0.0)
    REFRIGERATED = ("refrigerated", 0.2)
    FROZEN = ("frozen", 0.4)

    def __init__(self, id: str, adj_value: float):
        self.id = id
        self.adj_value = adj_value

    @staticmethod
    def from_id(id: str):
        for item in RefrigerationAdjust:
            if item.id == id:
                return item
        raise ValueError(f"Invalid refrigeration: {id}")


def calculate_product_emission(
    product_type: Union[str, EmissionFactor],
    quantity: float,
    transport: Union[str, TransportAdjust],
    packaging: Union[str, PackagingAdjust],
    refrigeration: Union[str, RefrigerationAdjust]
) -> float:
    if isinstance(product_type, str):
        try:
            factor_enum = EmissionFactor.from_id(product_type)
        except ValueError:
            factor = 0
        else:
            factor = factor_enum.factor
    elif isinstance(product_type, EmissionFactor):
        factor = product_type.factor
    else:
        factor = 0

    if isinstance(transport, str):
        try:
            transport_enum = TransportAdjust.from_id(transport)
        except ValueError:
            transport_adj = 0
        else:
            transport_adj = transport_enum.adj_value
    elif isinstance(transport, TransportAdjust):
        transport_adj = transport.adj_value
    else:
        transport_adj = 0

    if isinstance(packaging, str):
        try:
            packaging_enum = PackagingAdjust.from_id(packaging)
        except ValueError:
            packaging_adj = 0
        else:
            packaging_adj = packaging_enum.adj_value
    elif isinstance(packaging, PackagingAdjust):
        packaging_adj = packaging.adj_value
    else:
        packaging_adj = 0

    if isinstance(refrigeration, str):
        try:
            refrigeration_enum = RefrigerationAdjust.from_id(refrigeration)
        except ValueError:
            refrigeration_adj = 0
        else:
            refrigeration_adj = refrigeration_enum.adj_value
    elif isinstance(refrigeration, RefrigerationAdjust):
        refrigeration_adj = refrigeration.adj_value
    else:
        refrigeration_adj = 0

    return quantity * factor * (1 + transport_adj + packaging_adj + refrigeration_adj)

def calculate_products_total(products: List[Dict]) -> Dict:
    total_emission = 0.0
    products_emissions = []
    for prod in products:
        emission = calculate_product_emission(
            prod['product_type'],
            float(prod['quantity']),
            prod['transport'],
            prod['packaging'],
            prod['refrigeration']
        )
        products_emissions.append({
            'carbonProductId': prod.get('product_id'),
            'quantity': prod['quantity'],
            'totalProductEmission': round(emission, 2)
        })
        total_emission += emission
    return {
        'totalEmission': round(total_emission, 2),
        'productsEmissions': products_emissions
    }