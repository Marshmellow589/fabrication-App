# Fabrication Inspection Management System

A FastAPI-based application for managing fabrication inspection records.

## Features

- Material Inspection Management
- RESTful API
- CSV Import/Export
- SQLAlchemy ORM
- Pydantic Validation

## Installation

1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate virtual environment: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Run the application: `uvicorn app.main:app --reload`

## API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation.

## Endpoints

### Material Inspection
- `GET /api/v1/material/` - Get all material records
- `POST /api/v1/material/` - Create new material record
- `GET /api/v1/material/{unique_piece_id}` - Get material by unique ID
- `PUT /api/v1/material/{unique_piece_id}` - Update material record
- `DELETE /api/v1/material/{unique_piece_id}` - Delete material record
- `POST /api/v1/material/import` - Import from CSV
- `GET /api/v1/material/export/csv` - Export to CSV
