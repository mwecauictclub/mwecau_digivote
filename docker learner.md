
---

## **1️⃣ Docker Basics**

These are foundational—you must be very comfortable with them.

1. **Images vs Containers**

   * Image = blueprint (like a recipe)
   * Container = running instance (like a cooked meal)
   * `docker images` → list images
   * `docker ps` → list running containers
   * `docker ps -a` → list all containers

2. **Basic Commands**

   * Build image:

     ```bash
     docker build -t myapp:latest .
     ```
   * Run container:

     ```bash
     docker run -d -p 8000:8000 myapp:latest
     ```
   * Stop/remove container:

     ```bash
     docker stop <container_id>
     docker rm <container_id>
     ```
   * Remove image:

     ```bash
     docker rmi <image_id>
     ```

3. **Dockerfile Skills**

   * Writing efficient Dockerfiles:

     * Start from official Python image (`python:3.11-slim`)
     * Install system dependencies (`apt-get install`)
     * Copy your project files
     * Install Python dependencies (`pip install`)
     * Use `CMD` or `ENTRYPOINT` to start your app
   * Layer caching: understand which steps trigger rebuilds

4. **Volumes**

   * Mount code for live development:

     ```yaml
     volumes:
       - .:/app
     ```
   * Persist data (PostgreSQL/MySQL)

5. **Networking**

   * Containers communicate via **service names** in Docker Compose
   * Map container ports to host ports

---

## **2️⃣ Docker Compose**

Essential for multi-container apps (Django + Celery + Redis + DB)

1. **Services**

   * One service per container (web, worker, db, cache)

2. **Dependencies**

   * `depends_on` ensures order, but **does not wait for readiness** (use wait-for-it scripts if needed)

3. **Commands**

   * Build & start:

     ```bash
     docker compose up --build
     ```
   * Background:

     ```bash
     docker compose up -d
     ```
   * Stop all:

     ```bash
     docker compose down
     ```

4. **Scaling**

   * Run multiple workers for Celery:

     ```bash
     docker compose up --scale celery=3
     ```

---

## **3️⃣ Python-specific Skills**

1. **Dependency Management**

   * Use `requirements.txt` or `poetry`
   * Always install inside the image (`pip install --no-cache-dir -r requirements.txt`)

2. **Environment Variables**

   * Use `.env` file for secrets / config
   * Access in Docker Compose:

     ```yaml
     environment:
       - DEBUG=1
       - DATABASE_URL=mysql://user:pass@db:3306/mydb
     ```

3. **Celery + Redis**

   * Separate worker and broker (Redis) containers
   * Use service names (`redis:6379`) for broker URL
   * Optional: Celery Beat container for scheduled tasks

4. **Database**

   * Use official images: `postgres`, `mysql`
   * Use volumes to persist data offline:

     ```yaml
     volumes:
       - db_data:/var/lib/mysql
     ```

---

## **4️⃣ Best Practices for Python Apps**

1. **One process per container**

   * Gunicorn in web container
   * Celery worker separate
   * Redis / DB as separate containers

2. **Non-root user**

   * Avoid running as root (`USER django_user`)

3. **Lightweight images**

   * Prefer `python:3.11-slim` over `python:3.11`
   * Remove build dependencies after installing packages

4. **Rebuild strategies**

   * Only rebuild when necessary (cache layers efficiently)

5. **Debugging**

   * Logs: `docker compose logs`
   * Shell into container:

     ```bash
     docker compose exec web bash
     ```

---

## **5️⃣ Advanced / Nice-to-Have Skills**

1. **Multi-stage builds**

   * Separate build and runtime layers (smaller final image)

2. **Healthchecks**

   * Ensure containers are ready before starting dependent services

3. **CI/CD Integration**

   * Build Docker images in GitHub Actions / GitLab CI

4. **Offline development**

   * Prebuild images with all dependencies
   * Use volumes for code changes

5. **Security**

   * Avoid storing secrets in images
   * Use `.env` and Docker secrets for sensitive configs

---

### **Recommended Learning Path for a Python Developer**

1. Learn basic Docker commands and Dockerfile syntax.
2. Practice containerizing a **Flask app**: single container, Gunicorn, expose port.
3. Upgrade to **Django app** + database container (Postgres/MySQL).
4. Add **Celery + Redis**, learn how to scale workers.
5. Learn Docker Compose fully (multi-container apps).
6. Explore **multi-stage builds**, healthchecks, and offline development setups.

---
