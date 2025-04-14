## 🚐Community Platform
![Django](https://img.shields.io/badge/Django-4.2-darkgreen?style=for-the-badge) ![Python](https://img.shields.io/badge/Python-3.12.9-blue?style=for-the-badge) ![Celery](https://img.shields.io/badge/Celery-5.4.0-lightgreen?style=for-the-badge) ![Redis](https://img.shields.io/badge/Redis-5.2.1-red?style=for-the-badge)


## Description project
A powerful full-stack backend system for managing vehicle bookings, user roles (drivers & customers), automated cleanup, real-time data visualization, and more. Built using Django, DRF, GraphQL, Celery, Redis, Plotly, and deployed via Docker on Railway.

🚀Deploy on Railway The project is deployed on Railway. To check the operation of the site, go to the link: 🔗[Community Platform](https://community-platform-production-95de.up.railway.app/)

## 🚀 Functional
✔️ User system with roles:
- Member: base user, can make orders, upgraded member, can register vehicles & create trips
- Moderator: reviews user upgrade requests
- Administrator: admin-assigned for advanced access
✔️ Vehicle Management (CRUD) ✔️ Trip Creation & Order Booking ✔️ Automated Database Cleanup (orders/trips deleted after 3 days past trip end) – powered by Celery & Redis ✔️ User Reviews & average driver rating ✔️ GraphQL API with JWT authentication and CRUD for Orders, Members, Bookings, Vehicle ✔️ Real-time Bar Charts with Plotly (consumes DRF JSON) ✔️ AWS S3 for media and static files ✔️ Dockerized app for easy deployment ✔️ CHosted on Railway

## 🛠️ Technologies
- **Django**
- **PostgreSQL**
- **Celery + Redis**
- **Celery**
- **Django REST Framework (DRF)**
- **Docker + Docker Container**
- **AWS S3**
- **GraphQL**
- **Plotly + requests**
- **Railway Deploy**

## 🔐 Authentication & Roles
- **JWT authentication via GraphQL**
- **Role requests sent to Moderator, who can approve/deny**
- **Admin can assign Admin role via admin panel**

## 📈 Plotly Integration
Data visualized with Plotly bar charts (e.g. bookings by vehicle)
JSON data fetched from DRF views and parsed into graphs

## ♻️ Auto Cleanup : Deletes expired Orders and Trips 3 days after trip end

## 📦 Installation and local launch
1️⃣ Cloning the repository
```bash
git clone https://github.com/AMuhailo/Community-Platform.git
cd Community-Platform.git
```

2️⃣ Virtual environment
```bash
python -m venv venv
source venv/bin/activate    # for macOS and Linux
venv\Scripts\activate       # for Windows
```

3️⃣ Installing dependencies
```bash
pip install -r requirements.txt
```

4️⃣ Setting Environment Variables
To run locally, you need to create an .env file in the root folder:
```bash
ENVIRONMENT=local
SECRET_KEY=your_secret_key
DATABASE_URL=your-url
REDIS_URL=your-url
EMAIL_HOST=your-host
EMAIL_HOST_USER=your-user-email
EMAIL_HOST_PASSWORD=your-user-password
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_STORAGE_BUCKET_NAME=your-aws-name
```

⚠️ Don`t upload .env to GitHub!
It needs to be added to .gitignore.

5️⃣ Starting the server
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
The site is now available at http://127.0.0.1:8000.

## ⚡Launching Celery
To allow Celery to run tasks in the background, start it like this:
```bash
docker pull redis
docker run -it --rm --name redis -p 6973:6973 redis
celery -A warehouse worker --loglevel=info
```

##  📋 Prerequisites 
Ensure you have the following installed:
- **Docker**
- **Docker Compose**
- **Railway deployment**

6️⃣ Build and run the project with Docker Compose:
```bash
docker-compose up --build
```

## 🐋 Docker Containers
The project uses the following containers:
- **community-web**: Django application
- **community-datebase**: PostgreSQL database
- **community-redis**: Redis server for Celery tasks
- **community-celery**: Celery worker for background tasks

## 🔗 Useful commands
💾 Creating a database backup
```bash
python manage.py dumpdata --indent=2 --output=management/fixtures/db_backup.json
```

♻️ Database recovery
```bash
python manage.py loaddata db_backup.json
```

## 📩 Contacts
If you have any questions, suggestions, problems with the project, ideas or proposals - please contact 📧 Email: amuhailo25@gmail.com 👨‍💻 GitHub: AMuhailo