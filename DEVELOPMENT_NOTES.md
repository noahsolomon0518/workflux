# Development Notes & Next Steps

## Current Implementation Status

### ✅ Completed Features

1. **Core Stock Calculation Engine**
   - Calculates required stock sizes based on finished dimensions
   - Accounts for lathe operations (chuck grip, buffer, cutoff, facing, turning allowance)
   - Accounts for milling operations (length, width, height allowances)
   - Supports round and rectangular stock

2. **User Interface**
   - Clean, modern web interface
   - Part entry form with dynamic fields
   - Parts list view
   - Optimization flowchart visualization

3. **Optimization Algorithm**
   - Groups parts by compatible stock sizes
   - Estimates cost savings
   - Visual flowchart representation

## 🔨 Immediate Next Steps

### Priority 1: Database Integration
**Why**: Currently using in-memory storage - data is lost on restart

**Implementation**:
```python
# Install SQLAlchemy
pip install Flask-SQLAlchemy

# In app.py, add:
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stock_selector.db'
db = SQLAlchemy(app)

# Uncomment models in models.py
# Run migrations:
with app.app_context():
    db.create_all()
```

### Priority 2: Material Provider Integration
**Why**: Get real-time pricing instead of estimates

**Potential Providers**:
- McMaster-Carr (web scraping or API if available)
- Online Metals (has API)
- Metals Depot
- SpeedyMetals

**Implementation Pattern**:
```python
# Create providers/mcmaster.py
import requests

def get_material_price(material_type, dimensions):
    # API call or web scraping
    # Return price per foot/unit
    pass

# Create providers/aggregator.py
def get_best_price(material_type, dimensions):
    providers = [mcmaster, onlinemetals, metalsdepot]
    prices = []
    for provider in providers:
        try:
            price = provider.get_material_price(material_type, dimensions)
            prices.append({
                'provider': provider.name,
                'price': price,
                'lead_time': provider.lead_time
            })
        except:
            continue
    return min(prices, key=lambda x: x['price'])
```

### Priority 3: Enhanced Optimization
**Why**: Current algorithm is basic - can be much smarter

**Improvements**:
```python
def optimize_stock_usage_advanced(parts_list):
    # Consider:
    # 1. Material utilization % (minimize waste)
    # 2. Multiple parts from single bar (nesting)
    # 3. Mixed material orders (volume discounts)
    # 4. Lead time optimization
    # 5. Preferred supplier consolidation
    
    # Use bin packing algorithms
    # Consider cutting patterns
    # Account for saw kerf/waste
    pass
```

## 🚀 Feature Ideas

### Short Term (Next Month)
1. **Export Functionality**
   - PDF reports of optimization
   - Excel/CSV export of parts list
   - Shopping list generation

2. **User Preferences**
   - Default tolerances
   - Preferred suppliers
   - Shop-specific settings (chuck sizes, standard tooling)

3. **Material Library**
   - Expand material types
   - Custom material definitions
   - Material properties database

### Medium Term (1-3 Months)
1. **Inventory Management**
   - Track on-hand stock
   - Use existing material before purchasing
   - Low stock alerts

2. **Work Order Integration**
   - Link parts to jobs
   - Track material usage per job
   - Job costing

3. **Supplier Management**
   - Supplier database
   - Historical pricing
   - Performance tracking

### Long Term (3-6 Months)
1. **CAD Integration**
   - Import STEP files
   - Auto-detect dimensions
   - Feature recognition (holes, threads, etc.)

2. **Machine Scheduling**
   - Link parts to machines
   - Capacity planning
   - Job scheduling

3. **Mobile App**
   - Shop floor access
   - Barcode scanning
   - Material receipt

## 🐛 Known Issues & Limitations

1. **Stock Type Compatibility**
   - Currently assumes compatible parts have same stock type
   - Should handle rectangular → round conversions where viable

2. **Tolerance Propagation**
   - Doesn't account for tolerance stack-up
   - Could be smarter about critical dimensions

3. **Multi-Material Parts**
   - No support for assemblies
   - Can't handle welded multi-material parts

4. **Pricing**
   - No quantity discounts
   - No shipping cost calculation
   - No supplier-specific pricing tiers

## 💡 Algorithm Improvements

### Stock Optimization
Current algorithm uses simple diameter matching. Better approach:

```python
def advanced_stock_matching(parts):
    """
    Use graph theory to find optimal groupings
    - Nodes = parts
    - Edges = compatibility score
    - Find minimum spanning tree
    """
    
    # Build compatibility matrix
    compatibility = build_compatibility_matrix(parts)
    
    # Cluster parts by:
    # 1. Material type (hard constraint)
    # 2. Stock size (soft constraint with cost)
    # 3. Lead time requirements
    # 4. Quantity needed
    
    # Use k-means or hierarchical clustering
    groups = cluster_parts(parts, compatibility)
    
    return groups
```

### Cost Calculation
```python
def calculate_true_cost(part, stock_size):
    """
    More accurate cost calculation
    """
    # Base material cost
    material_cost = get_material_cost(stock_size)
    
    # Waste cost (material you're removing)
    waste_volume = calculate_waste(part, stock_size)
    waste_cost = waste_volume * material_cost_per_volume
    
    # Setup cost (larger stock = longer setup)
    setup_cost = estimate_setup_cost(stock_size)
    
    # Tooling wear (harder materials = more cost)
    tooling_cost = estimate_tooling_cost(part.material, part.operations)
    
    return material_cost + waste_cost + setup_cost + tooling_cost
```

## 📊 Data to Track (Future Analytics)

Once you have a database, track:
1. Material utilization % by material type
2. Average cost savings per optimization
3. Supplier price trends
4. Lead time accuracy
5. Inventory turnover
6. Most common part types
7. Machine utilization

## 🔐 Security Considerations

Before production deployment:
1. Add user authentication (Flask-Login)
2. Implement CSRF protection
3. Input validation and sanitization
4. Rate limiting on API endpoints
5. HTTPS enforcement
6. Database backup strategy

## 📚 Recommended Libraries

- **Flask-SQLAlchemy**: Database ORM
- **Flask-Login**: User authentication
- **Flask-WTF**: Form handling & CSRF
- **Celery**: Background tasks (price updates)
- **Redis**: Caching material prices
- **APScheduler**: Scheduled jobs
- **Pandas**: Data analysis and exports
- **Plotly**: Interactive charts
- **PyPDF2**: PDF generation
- **openpyxl**: Excel export

## 🎯 Target Market Considerations

Since this is for startup shops:
1. Keep UI simple - shop floor users aren't software experts
2. Mobile-friendly - often accessed from shop floor
3. Fast performance - can't wait for calculations
4. Offline capability would be valuable
5. Integration with common shop tools (calipers, CMMs)

## 📞 Support & Resources

- Flask Documentation: https://flask.palletsprojects.com/
- SQLAlchemy: https://www.sqlalchemy.org/
- Material Supplier APIs:
  - Online Metals: https://www.onlinemetals.com/
  - McMaster-Carr: (no public API - would need scraping)
- Optimization Algorithms:
  - Bin Packing: https://en.wikipedia.org/wiki/Bin_packing_problem
  - Cutting Stock: https://en.wikipedia.org/wiki/Cutting_stock_problem

---

**Last Updated**: December 2024
**Version**: 0.1.0
**Status**: Prototype/MVP
