# 🥐 Bakery System

A Docker-based microservices application for managing bakery products and orders, featuring:

- **PostgreSQL** for data persistence  
- **FastAPI** backend with 3 core endpoints  
- **RabbitMQ** message queue for order events  
- **React** frontend (plain CSS)  
- **Docker Compose** for orchestration  
- Health checks, resource limits, and CORS configuration  

---

## 📐 Architecture

![System Architecture Diagram](Architecture.png)



> **Services:**  
> 1. `db` (PostgreSQL)  
> 2. `backend` (FastAPI + SQLAlchemy)  
> 3. `rabbitmq` (AMQP + Management UI)  
> 4. `frontend` (React + Nginx)  

All services communicate over a user-defined Docker bridge network. Orders placed via the API are published to RabbitMQ for eventual processing.

---

## 🚀 Quickstart

1. **Clone & configure**  
   ```bash
   git clone git@github.com:<your-username>/bakery-system.git
   cd bakery-system
   cp backend/.env.example backend/.env
   cp frontend/.env.example frontend/.env
   
2. **Build and Run**
   ```bash
   docker compose build --no-cache
   docker compose up -d

3. **Verify Services**
   ```bash
   docker-compose ps
   docker stats

4. **Open UIs**
   - API docs (Swagger): http://localhost:8000/docs
   - Frontend: http://localhost:3000
   - RabbitMQ management: http://localhost:15672 (guest/guest)

5. **Shut Down**
   ```bash
   docker-compose down

---

## 🚧 API Reference
![API Reference](API_Reference.png)

---

## 🛠️ Frontend
1. **Local Development**
   ```bash
   cd frontend
   npm install
   npm start
- Runs on http://localhost:3000
- Uses REACT_APP_API_URL from frontend/.env

2. **Dockerized**
   - Build-arg REACT_APP_API_URL is set to http://localhost:8000 at build time
   - Seved by Ngnix on port 80 inside the container, mapped to host 3000

   
