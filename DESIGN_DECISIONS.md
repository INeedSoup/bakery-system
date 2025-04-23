# Design Decisions

A concise overview of the key architectural and implementation choices made in this project.

---

## 1. FastAPI for Backend

- **Why?**  
  - Modern, async-ready, with built-in validation and Swagger UI.  
  - Excellent developer ergonomics (type hints, Pydantic schemas).  

- **Benefits:**  
  - Auto-generated API docs at `/docs`.  
  - Clear request/response models with Pydantic.  
  - Easy to Dockerize and health-check.

---

## 2. PostgreSQL with Docker Volume

- **Why?**  
  - Reliable, ACID-compliant relational DB for product & order data.  

- **Setup:**  
  - Environment variables for credentials & DB name.  
  - Volume `db_data` for persistence across restarts.  
  - Healthcheck using `pg_isready`.

---

## 3. RabbitMQ for Message Queue

- **Why?**  
  - Decouples order placement from processing; allows for scaling workers.  
  - Management UI simplifies monitoring.

- **Integration:**  
  - `pika` library publishes JSON messages.  
  - Durable queue ensures messages survive broker restarts.

---

## 4. React Frontend (Plain CSS)

- **Why?**  
  - Familiar stack, zero-dependency styling avoids Tailwind complexity.  
  - Separation of concerns: UI in React, API in FastAPI.

- **Deployment:**  
  - Multi-stage Docker build:  
    1. Build React bundle  
    2. Serve with Nginx  
  - Build-arg `REACT_APP_API_URL` injects backend URL at compile time.

---

## 5. Docker Compose Orchestration

- **Why?**  
  - Single command brings up all services.  
  - Shared network for service-to-service DNS.

- **Features:**  
  - `depends_on` with `service_healthy`.  
  - Healthchecks on every container.  
  - Resource constraints for isolation.

---

## 6. Health Checks

- **Database:** `pg_isready`  
- **Backend:** `/health` endpoint  
- **RabbitMQ:** `rabbitmq-diagnostics ping`  
- **Frontend:** `wget --spider http://localhost/` 

> **Benefit:** Early detection of failures and automatic restarts.

---

## 7. Resource Limits

- **Compose fields:** `mem_limit`, `cpus`  
- **Deploy fields:** `deploy.resources` for future Swarm/K8s  
- **Rationale:** Prevent any one container from starving the host or peers.

---

## 8. CORS Configuration

- **Why?**  
  - Frontend at `localhost:3000` must call API on `localhost:8000`.  
- **Implementation:**  
  ```python
  app.add_middleware(
      CORSMiddleware,
      allow_origins=["http://localhost:3000"],
      allow_methods=["*"],
      allow_headers=["*"],
      allow_credentials=True,
  )
