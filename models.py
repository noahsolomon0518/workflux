"""
Database models for future implementation with SQLAlchemy
This file is not currently used but shows the planned database structure
"""

from datetime import datetime
# from flask_sqlalchemy import SQLAlchemy
# db = SQLAlchemy()

"""
Uncomment when ready to implement database:

class Part(db.Model):
    __tablename__ = 'parts'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    part_number = db.Column(db.String(100), unique=True)
    material_type = db.Column(db.String(100), nullable=False)
    stock_type = db.Column(db.String(50))  # round, rectangular, plate
    
    # Dimensions
    length = db.Column(db.Float, nullable=False)
    diameter = db.Column(db.Float)
    width = db.Column(db.Float)
    height = db.Column(db.Float)
    
    # Tolerances
    general_tolerance = db.Column(db.Float)
    tight_tolerance = db.Column(db.Float)
    
    # Stock requirements
    stock_length = db.Column(db.Float)
    stock_diameter = db.Column(db.Float)
    stock_width = db.Column(db.Float)
    stock_height = db.Column(db.Float)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Relationships
    operations = db.relationship('Operation', back_populates='part', cascade='all, delete-orphan')
    stock_group_id = db.Column(db.Integer, db.ForeignKey('stock_groups.id'))
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'part_number': self.part_number,
            'material_type': self.material_type,
            'dimensions': {
                'length': self.length,
                'diameter': self.diameter,
                'width': self.width,
                'height': self.height
            },
            'stock_recommendation': {
                'length': self.stock_length,
                'diameter': self.stock_diameter,
                'width': self.stock_width,
                'height': self.stock_height
            }
        }


class Operation(db.Model):
    __tablename__ = 'operations'
    
    id = db.Column(db.Integer, primary_key=True)
    part_id = db.Column(db.Integer, db.ForeignKey('parts.id'), nullable=False)
    operation_type = db.Column(db.String(50), nullable=False)  # lathe, milling, welding
    
    # Lathe specific
    chuck_grip = db.Column(db.Float)
    buffer_clearance = db.Column(db.Float)
    cutoff_thickness = db.Column(db.Float)
    face_thickness = db.Column(db.Float)
    turning_allowance = db.Column(db.Float)
    
    # Milling specific
    length_allowance = db.Column(db.Float)
    width_allowance = db.Column(db.Float)
    height_allowance = db.Column(db.Float)
    
    # General
    sequence_number = db.Column(db.Integer)
    notes = db.Column(db.Text)
    
    # Relationships
    part = db.relationship('Part', back_populates='operations')


class StockGroup(db.Model):
    __tablename__ = 'stock_groups'
    
    id = db.Column(db.Integer, primary_key=True)
    material_type = db.Column(db.String(100), nullable=False)
    stock_length = db.Column(db.Float)
    stock_diameter = db.Column(db.Float)
    stock_width = db.Column(db.Float)
    stock_height = db.Column(db.Float)
    
    estimated_cost = db.Column(db.Float)
    estimated_savings = db.Column(db.Float)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    parts = db.relationship('Part', backref='stock_group')


class MaterialPrice(db.Model):
    __tablename__ = 'material_prices'
    
    id = db.Column(db.Integer, primary_key=True)
    material_type = db.Column(db.String(100), nullable=False)
    supplier = db.Column(db.String(200))
    
    # Dimensions
    length = db.Column(db.Float)
    diameter = db.Column(db.Float)
    width = db.Column(db.Float)
    height = db.Column(db.Float)
    
    # Pricing
    price_per_unit = db.Column(db.Float)
    price_per_foot = db.Column(db.Float)
    minimum_order = db.Column(db.Float)
    lead_time_days = db.Column(db.Integer)
    
    # Metadata
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    in_stock = db.Column(db.Boolean, default=True)


class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password_hash = db.Column(db.String(200))
    company = db.Column(db.String(200))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    parts = db.relationship('Part', backref='creator')


class Inventory(db.Model):
    '''For future MRP functionality'''
    __tablename__ = 'inventory'
    
    id = db.Column(db.Integer, primary_key=True)
    material_type = db.Column(db.String(100), nullable=False)
    
    # Stock dimensions
    length = db.Column(db.Float)
    diameter = db.Column(db.Float)
    width = db.Column(db.Float)
    height = db.Column(db.Float)
    
    # Inventory tracking
    quantity = db.Column(db.Integer, default=0)
    location = db.Column(db.String(200))
    lot_number = db.Column(db.String(100))
    
    # Costs
    unit_cost = db.Column(db.Float)
    total_value = db.Column(db.Float)
    
    # Dates
    received_date = db.Column(db.DateTime)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Alerts
    reorder_point = db.Column(db.Integer, default=5)
    reorder_quantity = db.Column(db.Integer, default=10)


class PurchaseOrder(db.Model):
    '''For future MRP functionality'''
    __tablename__ = 'purchase_orders'
    
    id = db.Column(db.Integer, primary_key=True)
    po_number = db.Column(db.String(100), unique=True)
    supplier = db.Column(db.String(200))
    
    total_cost = db.Column(db.Float)
    status = db.Column(db.String(50))  # pending, ordered, received
    
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    expected_delivery = db.Column(db.DateTime)
    received_date = db.Column(db.DateTime)
    
    notes = db.Column(db.Text)
"""
