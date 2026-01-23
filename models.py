from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    ForeignKey,
)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import declarative_base, relationship

db = SQLAlchemy()

class Customer(db.Model):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    company_name = Column(String(255), nullable=False)

    def __repr__(self):
        return f"<Customer {self.company_name}>"
    
class Group(db.Model):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True)
    group_name = Column(String(255), nullable=False)
    def __repr__(self):
        return f"<Group {self.group_name}>"
    
class BaseStock(db.Model):
    __tablename__ = "base_stocks"

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    group = relationship("Group", backref="base_stocks")
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    customer = relationship("Customer", backref="base_stocks")
    external_part_number = Column(String(100), nullable=False)
    external_part_name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    extra_parts = Column(Integer, nullable=False, default=0)  
    revision_number = Column(String(50), nullable=False)
    approval_engineer = Column(String(255), nullable=True)

    def __repr__(self):
        return f"<Part {self.external_part_number} rev {self.revision_number}>"
    

class LatheStock(db.Model):
    __tablename__ = "lathe_stocks"

    id = Column(Integer, ForeignKey("base_stocks.id"), primary_key=True)
    base_stock = relationship("BaseStock", backref="lathe_stocks")
    overall_outer_dimensions = Column(Float, nullable=False)   # e.g. diameter (in or mm)
    overall_length = Column(Float, nullable=False)
    bar_or_slug = Column(String(20), nullable=False)  
    workholding_grip = Column(Float, nullable=True)  
    clearance = Column(Float, nullable=True)
    cutoff_blade_width = Column(Float, nullable=True)
    clean_axial_stock = Column(Float, nullable=True)
    clean_radial_stock = Column(Float, nullable=True)
    round_outer_dimensions = Column(Float, nullable=True)
    round_length = Column(Float, nullable=True)

    def __repr__(self):
        return f"<LatheStock {self.overall_outer_dimensions} x {self.overall_length}>"