from server import create_app, db
import time



app = create_app("prod")
with app.app_context():
    db.create_all()
    db.session.commit()
app.run(host='0.0.0.0', port=8081, debug=True)
