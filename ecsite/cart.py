from dataclasses import dataclass, field
from typing import Dict
from django.db.models.query import QuerySet


@dataclass
class Cart:
    items: Dict[int, int] = field(default_factory=dict)

    def add(self, product_id: int, quantity: int = 1) -> None:
        if product_id in self.items:
            self.items[product_id] += quantity
        else:
            self.items[product_id] = quantity

    def get_quantity(self, product_id: int) -> int:
        return self.items.get(product_id, 0)

    def would_exceed_quantity(self, product_id: int, add_quantity: int, stock: int) -> bool:
        total_quantity = self.get_quantity(product_id) + add_quantity
        return total_quantity > stock

    def remove(self, product_id: int) -> None:
        if product_id in self.items:
            del self.items[product_id]

    def clear(self) -> None:
        self.items.clear()

    def get_products(self, product_model) -> QuerySet:
        return product_model.objects.filter(id__in=self.items.keys())

    def __len__(self) -> int:
        return sum(self.items.values())

    def to_dict(self) -> dict:
        return {
            'items': {str(k): v for k, v in self.items.items()}
        }

    @classmethod
    def from_dict(cls, session_data: dict) -> 'Cart':
        cart = cls()
        if session_data and 'items' in session_data:
            cart.items = {
                int(k): v for k, v in session_data['items'].items()
            }
        return cart
