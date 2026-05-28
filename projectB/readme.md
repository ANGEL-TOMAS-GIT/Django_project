# Warehouse Management System (Project B)

[![Django](https://img.shields.io/badge/Django-4.2-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.14-red.svg)](https://www.django-rest-framework.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)](https://www.docker.com/)
[![Coverage](https://img.shields.io/badge/Coverage-84%25-brightgreen.svg)](https://coverage.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Overview

Warehouse Management System (Project B) is a microservice that handles inventory management, stock movements, analytics, and real-time stock tracking. It communicates with Project A (Bookstore) via REST API to provide accurate inventory data.

## ✨ Features

### Core Features
- ✅ **Inventory Management** - Warehouses, Stock, Movements
- ✅ **Real-time Stock Tracking** - Available, Reserved quantities
- ✅ **Analytics & Reports** - Daily reports, Stock alerts
- ✅ **JWT Authentication** - Secure API access
- ✅ **Role-Based Permissions** - Admin, Manager, Staff, Viewer
- ✅ **Async Tasks** - Celery for background jobs
- ✅ **Caching** - Redis for performance
- ✅ **i18n Support** - English, Spanish, Ukrainian, Arabic (RTL)

### API Features
- ✅ RESTful API with Django REST Framework
- ✅ Swagger/ReDoc Interactive Documentation
- ✅ JWT Token Authentication
- ✅ Pagination & Filtering
- ✅ Permission-based Access Control
- ✅ Request/Response Caching

### Admin Features
- ✅ Django Admin Interface
- ✅ Custom Admin Panels
- ✅ Real-time Dashboard with Bootstrap 5
- ✅ Data Export (CSV/JSON)

## 🚀 Quick Start

### Prerequisites

```bash
Docker Desktop 4.20+
Python 3.12+ (for local development)
PostgreSQL 15+ (if not using Docker)
Redis 7+ (if not using Docker)