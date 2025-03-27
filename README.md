# Prashnova E-Commerce Platform

Prashnova is a Flask-based e-commerce platform with user authentication, cart functionality, product management, and email notifications. The backend is powered by PostgreSQL and deployed on **Vercel**.

## 🚀 Features

- User authentication (registration & login)
- Secure password hashing with bcrypt
- Cart management system
- PostgreSQL database integration
- Flask-Mail for email notifications
- Fully deployed using **Vercel** with Railway PostgreSQL

---

## 🛠️ Tech Stack

- **Backend:** Flask, Flask-Login, Flask-SQLAlchemy
- **Database:** PostgreSQL (Railway)
- **Frontend:** HTML, CSS, JavaScript
- **Deployment:** Vercel, Railway.app

---

## 📌 Installation & Setup

### 1️⃣ Clone the Repository

```bash
  git clone https://github.com/imprashanttts/prashnova.git
  cd prashnova
```

### 2️⃣ Install Dependencies

```bash
  pip install -r requirements.txt
```

### 3️⃣ Configure PostgreSQL

Set up a PostgreSQL database using [Railway.app](https://railway.app/) and update the connection string in `config.py`:

```python
SQLALCHEMY_DATABASE_URI = "postgresql://postgres:<password>@<host>:<port>/railway"
SECRET_KEY = "your_secret_key"
```

### 4️⃣ Run the Application Locally

```bash
  python app.py
```

The app will run on **[http://127.0.0.1:5000/](http://127.0.0.1:5000/)**

---

## 🚀 Deployment on Vercel

### 1️⃣ Install Vercel CLI

```bash
  npm install -g vercel
```

### 2️⃣ Link Project to Vercel

```bash
  vercel login
  vercel
```

### 3️⃣ Configure `vercel.json`

```json
{
  "version": 2,
  "builds": [
    { "src": "app.py", "use": "@vercel/python" }
  ],
  "routes": [
    { "src": "/(.*)", "dest": "app.py" }
  ],
  "env": {
    "SQLALCHEMY_DATABASE_URI": "postgresql://postgres:<password>@<host>:<port>/railway",
    "SECRET_KEY": "your_secret_key"
  }
}
```

### 4️⃣ Deploy

```bash
  vercel --prod
```

---

## 🐛 Debugging Issues

- Check logs:
  ```bash
  vercel logs <your-vercel-project-url>
  ```
- Common Errors:
  - **StringDataRightTruncation**: Check if your database column length is enough.
  - **Invalid Salt**: Ensure bcrypt hashes are stored correctly.
  - **Internal Server Error**: Check `vercel logs` for details.

---

## 📌 To-Do & Future Plans

- Improve UI for a better user experience
- Add admin panel for better product & user management
- Implement search & filter functionality
- Enhance security & performance optimizations

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to change.

---

## 📧 Contact

For any queries, reach out to **Prashant** at prashu8511\@gmail.com.

---

## 📜 License

This project is licensed under the MIT License.

---

