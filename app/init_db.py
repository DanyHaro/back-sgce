from app import create_app, db

app = create_app()

# Aquí estamos activando el contexto de la aplicación para que funcione con SQLAlchemy
with app.app_context():
    try:
        db.create_all()
        print("Tables created successfully!")
    except Exception as e:
        print(f"Error creating tables: {e}")
