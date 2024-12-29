# Swift Car Django Project

Welcome to the **Swift Car Django** project repository! This project forms the backend foundation for a car rental platform. The platform includes three main components:

1. **Backend**: Powered by Django (this repository).
2. **Client-Side for Customers**: A React.js application allowing users to browse, rent, and manage car bookings.
3. **Admin-Side Interface**: A React.js application for administrators to manage cars, clients, and operations efficiently.

This project is the result of a collaborative effort. Special thanks to my collaborators **Nossair SEDKi** and **Mohammed Amine EL METNI** for their invaluable contributions.

---

## Links to Other Repositories

- **Client-Side for Customers**: [Swift Car Customer App](https://github.com/Y7T007/swift-car-reactjs-frontend)
- **Admin-Side Interface**: [Swift Car Admin Panel](https://github.com/Y7T007/swift-car-managers)

---

## Features of the Backend

- User authentication and authorization.
- Car listing and booking management.
- APIs for client and admin operations.
- Integration with third-party payment gateways.
- Scalable database design with Django ORM.

---

## Getting Started

Follow these steps to set up the project on your local machine:

### 1. Clone the Repository

```bash
git clone https://github.com/Y7T007/swift_car.git
cd swift_car
```

### 2. Set Up a Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

- On Windows:

```bash
.\venv\Scripts\activate
```

- On macOS/Linux:

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Set Up Local Environment Variables

Create a `.env` file in the root directory and add necessary environment variables (e.g., database credentials, secret keys, etc.).

### 6. Run Migrations

```bash
python manage.py migrate
```

### 7. Start the Development Server

```bash
python manage.py runserver
```

Now you can access the development server locally at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

---

## Contribution

This project welcomes contributions! If you'd like to improve or extend the platform, feel free to fork the repository and open a pull request.

---

## Acknowledgments

This project wouldn't have been possible without the incredible teamwork and dedication of:

- **Nossair SEDKi**
- **Mohammed Amine EL METNI**

Thank you both for your support and contributions!

---

## License

This project is licensed under the [MIT License](LICENSE).
