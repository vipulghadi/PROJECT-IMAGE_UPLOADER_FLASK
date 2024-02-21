from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
import uuid
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///images.db'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
upload_folder = os.path.join('static', 'uploads')
 
app.config['UPLOAD_FOLDER'] = upload_folder
db=SQLAlchemy(app)
file_formats=["jpeg","png","svg"]

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100))
    filepath=db.Column(db.String(200))
    
    def __str__(self):
        return self.filename
    

with app.app_context():
    db.create_all()
    
# Ensure that the uploads directory exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])




@app.route("/",methods=["GET","POST"])
@app.route("/<id>",methods=["GET","POST"])
def main(id=None):
    all_images=Image.query.all()
    
    if request.method=="POST":
        # check user uploaded valid file or not 
        if 'file' in request.files:
            file=request.files["file"]
            if not file:
                return redirect(request.url)
            else:
                # if file exist then we have to save it in db
                filename = secure_filename(str(uuid.uuid4()))
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                new_image = Image(filename=filename,filepath=file_path)
                db.session.add(new_image)
                db.session.commit()
                return redirect(request.url)
            
        else : 
            print("not present")
            return redirect(request.url)
    
    return render_template("Home.html",images=all_images)

@app.route("/delete/<id>",methods=["GET","POST"])
def delete_image(id):
    id=int(id)
    print("insode delete")
    try:
        print("in try block")
        image_object=Image.query.get(id)
        
        if os.path.exists(image_object.filepath):
            os.remove(image_object.filepath)
        if image_object:
            db.session.delete(image_object)
            db.session.commit()
    
        return redirect(url_for("main"))
    
    except Exception as e :
        print(e)
        
        return redirect(url_for("main"))
    
    

if __name__=="__main__":
    app.run(debug=True)
        
