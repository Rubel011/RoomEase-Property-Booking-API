from mongoengine import Document, StringField, FloatField, IntField, BooleanField, DateTimeField


class Booking(Document):
    user = StringField(required=True)  # Reference to User
    property = StringField(required=True)  # Reference to Property
    check_in = DateTimeField(required=True)
    check_out = DateTimeField(required=True)
    total_price = FloatField(required=True)
    status = StringField(default="pending")
    # Add more fields as needed
