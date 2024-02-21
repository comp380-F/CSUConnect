# CSUConnect: A Website for Student Organization Events

## Introduction

Website for student organizations at California State Universities to post about their events.

## Features

- Event posting by organizations
- Easy navigation and event discovery
- User authentication for posting events

## Getting Started

### Prerequisites

Before running the application, ensure you have the following installed:

- Python 3.8 or newer
- pip (Python package installer)

### Installation

1. Clone the repository to your local machine:
   ```
   git clone https://github.com/nverkhachoyan/OnlyClubs.git
   ```
2. Navigate to the cloned repository:
   ```
   cd OnlyClubs
   ```
3. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```
   This command installs all the necessary dependencies listed in the [requirements.txt](https://github.com/nverkhachoyan/OnlyClubs/blob/main/requirements.txt) file, including Flask, Flask-Login, Flask-SQLAlchemy, and others.

### Configuration

The application requires a basic configuration to connect to a database. By default, it uses SQLite. The configuration is set in the [config.py](https://github.com/nverkhachoyan/OnlyClubs/blob/main/config.py) file. You can modify the `SQLALCHEMY_DATABASE_URI` to connect to a different database if needed.

### Running the Application

To start the application, run the following command in the terminal:

```
python run.py
```

This command starts a local server on `http://127.0.0.1:8080/` (or `http://localhost:8080/`). Open this URL in your web browser to access the OnlyClubs application.
