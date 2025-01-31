'''Script to populate the database with some initial data.
   In reality you would probably create a separate editor or a tool for importing data from elsewhere,
   but for CM1102 we'll just use this script to populate the database.'''

from app import app, db, Products

products = [
    { "name": "Self-help books", "price": "5.99", "description": "Books in the self-help genre.", "image": "selfhelpbook.jpg", "envimpact": "Low" },
    { "name": "Macbooks", "price": "1999", "description": "Laptops created by Apple.", "image": "macbook.jpg", "envimpact": "High" },
    { "name": "Audiobooks", "price": "20.99", "description": "Files containing the audio of an entire book.", "image": "audiobook.jpg", "envimpact": "High" },
    { "name": "Web development frameworks", "price": "1.99", "description": "Pre-designed collection of tools, libraries, and best practices that make it easier to create and maintain websites.", "image": "webframeworks.jpg", "envimpact": "Very high" }
]

# Bear in mind this script does NOT run the app
# instead we use app.app_context() which Flask provides to allow us to use the app's configuration and extensions
with app.app_context():
    db.create_all()
    
    for product in products:
        newTech = Products(name=product["name"], price=product["price"], description=product["description"], image=product["image"], env_impact=product["envimpact"])
        db.session.add(newTech)
    
    db.session.commit()