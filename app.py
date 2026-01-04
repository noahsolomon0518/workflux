from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json

app = Flask(__name__)

# In-memory storage (will be replaced with a database later)
parts = []
material_cache = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/parts')
def parts_list():
    return render_template('parts.html', parts=parts)

@app.route('/api/parts', methods=['GET', 'POST'])
def handle_parts():
    if request.method == 'POST':
        data = request.json
        part = {
            'id': len(parts) + 1,
            'name': data.get('name'),
            'dimensions': data.get('dimensions'),
            'operations': data.get('operations'),
            'tolerances': data.get('tolerances'),
            'material_type': data.get('material_type'),
            'stock_recommendation': calculate_stock_size(data),
            'created_at': datetime.now().isoformat()
        }
        parts.append(part)
        return jsonify(part), 201
    return jsonify(parts)

@app.route('/api/parts/<int:part_id>', methods=['GET', 'DELETE'])
def handle_part(part_id):
    part = next((p for p in parts if p['id'] == part_id), None)
    if not part:
        return jsonify({'error': 'Part not found'}), 404
    
    if request.method == 'DELETE':
        parts.remove(part)
        return '', 204
    return jsonify(part)

@app.route('/optimization')
def optimization():
    optimized_groups = optimize_stock_usage(parts)
    return render_template('optimization.html', groups=optimized_groups)

@app.route('/api/optimize', methods=['POST'])
def optimize():
    optimized_groups = optimize_stock_usage(parts)
    return jsonify(optimized_groups)

def calculate_stock_size(part_data):
    """Calculate required stock size based on part dimensions and operations"""
    dims = part_data.get('dimensions', {})
    ops = part_data.get('operations', {})
    
    # Base dimensions
    length = float(dims.get('length', 0))
    diameter = float(dims.get('diameter', 0)) if dims.get('diameter') else None
    width = float(dims.get('width', 0)) if dims.get('width') else None
    height = float(dims.get('height', 0)) if dims.get('height') else None
    
    # Operation allowances
    lathe_ops = ops.get('lathe', {})
    milling_ops = ops.get('milling', {})
    
    # Calculate stock requirements
    stock_length = length
    stock_diameter = diameter if diameter else None
    stock_width = width
    stock_height = height
    
    # Add lathe allowances
    if lathe_ops:
        chuck_grip = float(lathe_ops.get('chuck_grip', 0))
        buffer_clearance = float(lathe_ops.get('buffer_clearance', 0))
        cutoff_thickness = float(lathe_ops.get('cutoff_thickness', 0))
        face_thickness = float(lathe_ops.get('face_thickness', 0))
        
        stock_length += chuck_grip + buffer_clearance + cutoff_thickness + face_thickness
        
        if stock_diameter:
            # Add material for turning
            stock_diameter += float(lathe_ops.get('turning_allowance', 0))
    
    # Add milling allowances
    if milling_ops:
        stock_length += float(milling_ops.get('length_allowance', 0))
        if stock_width:
            stock_width += float(milling_ops.get('width_allowance', 0))
        if stock_height:
            stock_height += float(milling_ops.get('height_allowance', 0))
    
    return {
        'length': round(stock_length, 3),
        'diameter': round(stock_diameter, 3) if stock_diameter else None,
        'width': round(stock_width, 3) if stock_width else None,
        'height': round(stock_height, 3) if stock_height else None,
        'material_type': part_data.get('material_type')
    }

def optimize_stock_usage(parts_list):
    """Group parts that can use the same stock size for cost optimization"""
    if not parts_list:
        return []
    
    groups = []
    used_parts = set()
    
    for i, part in enumerate(parts_list):
        if i in used_parts:
            continue
            
        stock = part.get('stock_recommendation', {})
        group = {
            'stock_size': stock,
            'parts': [part],
            'cost_savings': 0
        }
        
        # Find compatible parts
        for j, other_part in enumerate(parts_list):
            if j <= i or j in used_parts:
                continue
                
            other_stock = other_part.get('stock_recommendation', {})
            
            # Check if parts can share stock (within tolerance)
            if can_share_stock(stock, other_stock):
                group['parts'].append(other_part)
                used_parts.add(j)
        
        used_parts.add(i)
        
        # Calculate potential savings
        if len(group['parts']) > 1:
            group['cost_savings'] = estimate_savings(group['parts'])
        
        groups.append(group)
    
    return groups

def can_share_stock(stock1, stock2, tolerance=0.125):
    """Check if two stock sizes are compatible (within tolerance)"""
    if stock1.get('material_type') != stock2.get('material_type'):
        return False
    
    # For round stock
    if stock1.get('diameter') and stock2.get('diameter'):
        dia_diff = abs(stock1['diameter'] - stock2['diameter'])
        # Smaller part can use larger stock
        return dia_diff <= tolerance and stock1['diameter'] >= stock2['diameter']
    
    # For rectangular stock
    if stock1.get('width') and stock2.get('width'):
        width_diff = abs(stock1['width'] - stock2['width'])
        height_diff = abs(stock1.get('height', 0) - stock2.get('height', 0))
        return width_diff <= tolerance and height_diff <= tolerance
    
    return False

def estimate_savings(parts_group):
    """Estimate cost savings from using common stock"""
    # Placeholder - will integrate with material provider pricing later
    base_savings = len(parts_group) * 15  # $15 per part simplified
    return round(base_savings, 2)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
