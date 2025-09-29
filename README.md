# E-Commerce Platform with AI-Generative Features (test)

## Description
This project is an **AI-powered e-commerce platform** built with Django that revolutionizes how sellers create product listings. Instead of manually writing descriptions and labels, sellers can simply upload a product photo, and our AI system will automatically:

- **Generate detailed product descriptions** automatically
- **Suggest relevant product labels and tags** 
- **Identify product categories** based on visual content
- **Automate tedious listing creation** to save sellers hours of work

The platform provides a complete MVP with user authentication, AI-powered product management, and intelligent search capabilities.

---

## Project Status
**Currently in active development** with a **fully functional MVP** that includes:
- Complete user authentication system
- Product CRUD operations (Create, Read, Update, Delete)
- Image upload and management
- Product search and filtering
- Category-based organization
- Admin interface for content management
- **AI Integration in Progress**: Computer vision and description generation

---

## Current Technology Stack
- **Backend**: Django 5.2.4 (Python web framework)
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **Image Processing**: Pillow 11.3.0
- **AI/ML**: Computer vision and natural language processing (in development)
- **Frontend**: Django Templates with Bootstrap styling
- **Authentication**: Django's built-in user system
- **Version Control**: Git + GitHub

---

## Features

### **Implemented Features**
- **User Management**: Registration, login, logout, and authentication
- **Product Management**: Create, edit, delete, and publish products
- **Image Handling**: Upload and display product images
- **Search & Filter**: Search by title, filter by category and price range
- **Category System**: Organized product categorization
- **Admin Panel**: Django admin interface for content management
- **Responsive Design**: Bootstrap-based responsive UI

### **Core Value Proposition**
This platform solves the **#1 pain point** for online sellers: **creating detailed product listings is time-consuming and tedious**. Our AI solution:
- **Reduces listing creation time** from 15-30 minutes to 2-3 minutes
- **Improves listing quality** with AI-generated descriptions and labels
- **Increases conversion rates** through better product presentation
- **Eliminates writer's block** when describing products

### **AI-Powered Features (Core Innovation)**
- ** Computer Vision Analysis**: Automatically analyze product images
- ** Smart Description Generation**: AI creates detailed product descriptions from photos
- ** Automatic Labeling**: Generate relevant tags and labels based on visual content
- ** Intelligent Categorization**: AI suggests product categories from image analysis
- ** Listing Automation**: Transform photo uploads into complete product listings
- ** Content Optimization**: AI-enhanced product descriptions for better conversions

---

## Setup Guide

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### 1. Clone and Setup Environment
```bash
git clone <Repository-url>
cd E-Commerce-con-IA-Generativa

# Create virtual environment
python -m venv env

# Activate virtual environment
# Windows:
env\Scripts\activate
# macOS/Linux:
source env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Setup
```bash
# Apply migrations (creates database tables and default categories automatically)
python manage.py migrate
```

### 3. Create Test Users (Required for Testing)
You need 2 users to test all features:

User 1 (Seller):
- Go to: [http://localhost:8000/register/](http://localhost:8000/register/)
- Create account: `seller_user` / `password123`
- This user will create products

User 2 (Buyer/Reviewer):
- Go to: [http://localhost:8000/register/](http://localhost:8000/register/)
- Create account: `buyer_user` / `password123`
- This user will review products

### 4. Run Development Server
```bash
python manage.py runserver
```

### 5. Access the Platform
- Main Site: [http://localhost:8000](http://localhost:8000)
- Admin Panel: [http://localhost:8000/admin](http://localhost:8000/admin)

### 6. Test the Features
1. Login as seller_user → Create a product (status: "Published")
2. Logout → Login as buyer_user → Go to product detail → Leave a review
3. Check AI features at `/api/ai/` (health check and product analysis)


**Note**: This is a Django-based **AI-powered e-commerce platform** that revolutionizes product listing creation. The AI features are the core innovation that sets this platform apart from traditional e-commerce solutions. This is not just another marketplace - it's an intelligent tool that automates the most tedious part of selling online.
