# SwiftLink – Microservice-Style URL Shortener

SwiftLink is a secure and production-ready URL shortening API built with **FastAPI**, designed for real-world use. It features authentication, click tracking, QR code generation, and analytics—making it a complete backend solution.

**Live App:** [https://swiftlink-4y8p.onrender.com](https://swiftlink-4y8p.onrender.com)  
**API Docs:** [https://swiftlink-4y8p.onrender.com/docs](https://swiftlink-4y8p.onrender.com/docs)

---

## Features

- User Registration and Login with JWT authentication
- Authenticated short URL creation
- Click tracking and last accessed timestamp
- QR code generation (base64 and downloadable PNG)
- Secure redirect via shortened links
- SQLite backend with SQLAlchemy ORM
- Fully documented Swagger interface

---

## Tech Stack

- **Backend:** FastAPI, SQLAlchemy, Pydantic
- **Authentication:** OAuth2 with JWT
- **Database:** SQLite (can be upgraded to PostgreSQL)
- **Utilities:** qrcode, bcrypt, PIL
- **Deployment:** Render

---

## Authentication

Use the `/auth/login` endpoint to receive an access token:

Then, click **"Authorize"** in the Swagger UI and paste your token for authenticated routes.

---

## Example Usage

1. Register a new user  
   POST /auth/register`

2. Login and obtain a JWT token  
   POST /auth/login`

3. Create a shortened URL  
   POST /shorten/shorten` (Authorized)

4. Access the original link  
   GET /<short_key>`

5. Download QR code  
   GET /shorten/qr/<short_key>/download`

6. View analytics  
   GET /analytics/me/analytics` (Authorized)

---

## Project Setup (Local Development)

``bash
git clone https://github.com/Pranav4555/SwiftLink.git
cd SwiftLink
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload

Author
Pranav Baitule
Email: pranavbaitule27@gmail.com
GitHub: github.com/Pranav4555
LinkedIn: linkedin.com/in/pranavbaitule


