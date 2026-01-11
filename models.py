from app import db

class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<Customer {self.company_name}>"
    
class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    order_name = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<Order {self.order_name}>"
    
class Part(db.Model):
    __tablename__ = "parts"

    id = db.Column(db.Integer, primary_key=True)
    external_part_number = db.Column(db.String(100), nullable=False)
    external_part_name = db.Column(db.String(255), nullable=False)
    revision_number = db.Column(db.String(50), nullable=False)
    approval_engineer = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<Part {self.external_part_number} rev {self.revision_number}>"