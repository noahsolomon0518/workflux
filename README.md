# Stock Size Selector

A Flask-based web application for calculating optimal stock sizes for machined parts with built-in optimization for cost savings.

## Features

### Current Implementation (v0.1)

- **Part Entry Form**: Input part dimensions, material type, and required operations
- **Multi-Operation Support**: 
  - Lathe operations (chuck grip, buffer clearance, cutoff thickness, facing)
  - Milling operations (length, width, height allowances)
  - Welding/joining flags
- **Automatic Stock Calculation**: Intelligently calculates required stock sizes based on:
  - Finished part dimensions
  - Operation-specific allowances
  - Material type
- **Stock Optimization**: Groups parts with compatible stock sizes to minimize costs
- **Visual Flowchart**: Shows optimization groups with cost savings estimates
- **Parts Management**: List, view, and delete parts

## Installation

1. Install Python 3.8 or higher

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser to `http://localhost:5000`

## Usage

### Adding a Part

1. Navigate to "New Part"
2. Enter part name and select material type
3. Choose stock type (round, rectangular, or plate)
4. Input finished part dimensions
5. Set tolerance requirements
6. Select applicable operations (lathe, milling, welding)
7. Fill in operation-specific allowances
8. Click "Calculate Stock Size"

### Viewing Optimization

1. Navigate to "Optimization" tab
2. View grouped parts that can share stock sizes
3. See estimated cost savings for each group
4. Flowchart shows stock-to-part relationships

## Roadmap

### Phase 1: Enhanced Features (Next)
- [ ] Database integration (SQLite/PostgreSQL)
- [ ] Material provider API integration for real-time pricing
- [ ] Export optimization reports (PDF/Excel)
- [ ] User authentication and multi-user support
- [ ] Part revision history

### Phase 2: MRP Features
- [ ] Inventory tracking
- [ ] Purchase order generation
- [ ] Supplier management
- [ ] Material lead time tracking
- [ ] Low stock alerts
- [ ] Batch/lot tracking

### Phase 3: ERP Expansion
- [ ] Job/work order management
- [ ] Shop floor scheduling
- [ ] Time tracking integration
- [ ] Customer management
- [ ] Quoting system
- [ ] Invoice generation

### Phase 4: Advanced Optimization
- [ ] Machine learning for cost prediction
- [ ] Multi-material optimization
- [ ] Waste reduction analytics
- [ ] Historical cost trending
- [ ] Preferred supplier recommendations

### Phase 5: Integration & API
- [ ] CAD file import (STEP, IGES)
- [ ] ERP system integrations (QuickBooks, etc.)
- [ ] Mobile app
- [ ] REST API for third-party tools
- [ ] Webhooks for automation

## Technical Architecture

### Current Stack
- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **Storage**: In-memory (temporary)

### Planned Stack
- **Database**: PostgreSQL with SQLAlchemy ORM
- **API Integration**: Requests library for material providers
- **Caching**: Redis for material pricing
- **Background Jobs**: Celery for optimization tasks
- **Frontend**: React (optional future enhancement)

## Contributing

This is a startup-focused project. Key areas for contribution:

1. Material provider API integrations
2. Cost optimization algorithms
3. UI/UX improvements
4. Database schema design
5. Testing and documentation

## License

Proprietary - All rights reserved

## Contact

For questions or feature requests, please contact the development team.
