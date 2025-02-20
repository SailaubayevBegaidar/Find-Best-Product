# Find Best Product

A web application that helps users find the best product deals by comparing prices across different sources.

## Features
- Product price comparison
- User authentication
- Product search and filtering
- Automated data collection from various sources
- Best deals recommendations

## Tech Stack
- Backend: Python/Flask
- Database: MongoDB
- Frontend: HTML, CSS, JavaScript
- Authentication: JWT
- Data Collection: Web Scraping (BeautifulSoup4)

## Setup Instructions
1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Create `.env` file with required environment variables
6. Run the application: `python app.py`

## API Endpoints
- POST /register - User registration
- POST /login - User authentication
- GET /products - Get all products
- POST /products - Add new product
- PUT /products/<id> - Update product
- DELETE /products/<id> - Delete product

## Database Schema
- Users Collection
- Products Collection
- Price History Collection
