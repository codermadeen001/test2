## Crop Tracker

Live Application: https://crop-tracker-ui.onrender.com 


### Structure

crop_tracker_app/
├── crop_tracker_ui/          # Vue 3 application
│   ├── src/                  # Source code
│   ├── public/               # Static assets
│   ├── package.json          # Dependencies
│   └── vite.config.js        # Vite configuration
├── crop_tracker/             # Django application
│   ├── crop_tracker/         # Project settings
│   ├── fields/               # Fields module
│   ├── users/                # Authentication module
│   └── requirements.txt      # Python dependencies
└── README.md                 # This document



## Task Overview

A farm crop management system for tracking agricultural fields, monitoring crop growth stages, and automatically identifying at-risk fields based on configurable time thresholds.



## Technology Stack

| Layer | Technology |
|-------|------------|
| Frontend | Vue 3 |
| Backend | Django |
| Database | PostgreSQL (Online) |
| Deployment | Render (Static Site + Web Service) |
| Additional Packages | Axios, Vue Router |



## Design Decisions

- Frontend Framework: Vue 3 selected for reactive UI and component-based architecture.
- Backend Framework: Django chosen for robust ORM, light weight and built-in administrative interface.
- Color Theme: Green and white to align with agricultural domain branding.
- Hosting: Free-tier services used; performance limitations are acknowledged.



## Setup Instructions

### Frontend (Vue 3)

Execute the following commands from the `frontend` directory:

```bash
# Install base dependencies
npm install

# Install required packages
npm install axios vue-router@4

# Start development server
npm run dev

The application will be available at http://localhost:3000.


## Backend (Django)
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Apply database migrations
python manage.py migrate  #can skip

# Start Django development server
python manage.py runserver

The API will be available at http://localhost:8000.




### ADMIN CREDENTIALS
email: Syeundainnocent@gmail.com
password: demo123_Admin



### Field Status Logic
Step 1: Evaluate current stage
        If stage == "Harvested":
            Status = "Completed" (Terminal state)
        Else:
            Proceed to Step 2

Step 2: Calculate elapsed days
        days_since_planting = Current_Date - planting_date

Step 3: Apply stage-specific threshold
        If days_since_planting > threshold[current_stage]:
            Status = "At Risk"
        Else:
            Status = "Active"

### Assumtions
- Free-tier hosting services are used, application may exhibit slower response times.
- Free-tier PostgreSQL database is used, connection pooling and concurrent request handling are limited.