from flaskblog import create_app

app = create_app()

if __name__ == '__main__':
    # start the app in debug mode
    app.run(debug=True)
