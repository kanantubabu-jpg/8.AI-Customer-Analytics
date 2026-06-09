"""
Product recommendation engine based on customer segment.
"""


class RecommendationEngine:
    """Map customer segments to product recommendations."""

    SEGMENT_PRODUCTS = {
        "Budget Conscious": [
            {"name": "Basic Essentials Pack", "category": "Home", "price": 29.99},
            {"name": "Economy Wireless Earbuds", "category": "Electronics", "price": 19.99},
            {"name": "Value Fitness Band", "category": "Sports", "price": 24.99},
        ],
        "Standard Shoppers": [
            {"name": "Smart Home Starter Kit", "category": "Home", "price": 79.99},
            {"name": "Casual Wear Collection", "category": "Clothing", "price": 59.99},
            {"name": "Bluetooth Speaker Pro", "category": "Electronics", "price": 49.99},
        ],
        "Premium Loyalists": [
            {"name": "Premium Noise-Cancel Headphones", "category": "Electronics", "price": 199.99},
            {"name": "Designer Jacket Line", "category": "Clothing", "price": 149.99},
            {"name": "Smart Fitness Watch", "category": "Sports", "price": 179.99},
        ],
        "High-Value Champions": [
            {"name": "Executive Laptop Bundle", "category": "Electronics", "price": 1299.99},
            {"name": "Luxury Home Automation", "category": "Home", "price": 899.99},
            {"name": "Pro Sports Equipment Set", "category": "Sports", "price": 599.99},
        ],
    }

    DEFAULT_PRODUCTS = [
        {"name": "Featured Product Bundle", "category": "General", "price": 99.99},
        {"name": "Seasonal Offer Pack", "category": "General", "price": 69.99},
        {"name": "Customer Favorites Kit", "category": "General", "price": 79.99},
    ]

    def get_recommendations(self, segment: str) -> list[dict]:
        """Return product recommendations for a given segment."""
        return self.SEGMENT_PRODUCTS.get(segment, self.DEFAULT_PRODUCTS)

    def format_recommendations(self, segment: str) -> str:
        """Format recommendations as a comma-separated string for storage."""
        products = self.get_recommendations(segment)
        return ", ".join(p["name"] for p in products)
