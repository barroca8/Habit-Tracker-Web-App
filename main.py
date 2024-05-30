from app import app, create_initial_habits

if __name__ == '__main__':
    create_initial_habits()
    app.run(debug=True)
