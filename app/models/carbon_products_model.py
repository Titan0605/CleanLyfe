from app.utils.db_utils import get_client, get_collection
from pymongo import MongoClient
from pymongo.collection import Collection
from bson.objectid import ObjectId
from typing import Optional, Dict, Any, List

class CarbonProductsModel:
    def __init__(self) -> None:
        self._client: Optional[MongoClient] = None
        self._products_collection: Optional[Collection] = None
        self._emissions_collection: Optional[Collection] = None

    @property
    def client(self) -> MongoClient:
        if self._client is None:
            self._client = get_client()
        return self._client

    @property
    def products_collection(self) -> Collection:
        if self._products_collection is None:
            self._products_collection = get_collection("carbonProducts")
        return self._products_collection

    @property
    def emissions_collection(self) -> Collection:
        if self._emissions_collection is None:
            self._emissions_collection = get_collection("productsEmissions")
        return self._emissions_collection

    def get_all_products(self) -> List[Dict[str, Any]]:
        products = []
        for product in self.products_collection.find().sort("productName"):
            products.append({
                "id": str(product["_id"]),
                "productName": product["productName"],
                "productType": product["productType"]
            })
        return products

    def get_products_by_ids(self, ids_list: List[str]) -> List[Dict[str, Any]]:
        object_ids = [ObjectId(id_str) for id_str in ids_list]
        query = {"_id": {"$in": object_ids}}
        products = []
        for product in self.products_collection.find(query).sort("productName"):
            products.append({
                "id": str(product["_id"]),
                "productName": product["productName"],
                "productType": product["productType"]
            })
        return products

    def insert_products_emissions(self, emissions: List[Dict[str, Any]]):
        result = self.emissions_collection.insert_many(emissions)
        return [str(_id) for _id in result.inserted_ids]

    def calculate_products_footprint(self, products_data: List[Dict[str, Any]], total_emission: float) -> Dict[str, Any]:
        emission_ids = self.insert_products_emissions(products_data)
        return {
            "totalEmission": total_emission,
            "productsEmissions": emission_ids
        }
