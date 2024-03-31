from mongoengine import Document, StringField, FloatField, IntField, BooleanField, DateTimeField


class Property(Document):
    title = StringField(required=True)
    description = StringField()
    address = StringField(required=True)
    city = StringField(required=True)
    state = StringField(required=True)
    country = StringField(required=True)
    price = FloatField(required=True)
    max_guests = IntField(required=True)
    bedrooms = IntField()
    bathrooms = IntField()
    amenities = StringField()
    host_id = StringField(required=True)  # Reference to User
    property_type = StringField(
        choices=["Apartment", "House", "Unique Homes"], default="House")
    is_available = BooleanField(default=True)
    created_at = DateTimeField()
