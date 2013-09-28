from flask import Flask, render_template, redirect, send_from_directory
from hsaudiotag import auto
from flask_bootstrap import Bootstrap
from os import listdir
from os.path import join, isdir
app = Flask(__name__ , static_path='/static', static_url_path='/static')
Bootstrap(app)
musicDir = "./music/"

@app.route('/static/<subdir>/<path:filename>/')
def static_subdir(subdir=None, filename=None):

    directory = "./static/" + subdir
    return send_from_directory(directory, filename)

@app.route("/playall/")
@app.route("/playall/<directory>/")
def playall(directory=None):
    if not directory:
        currentdir = musicDir
    else:
        currentdir = join(musicDir, directory)
    directoryList =  [ d for d in listdir(currentdir) ]
    return render_template('playall.html', directoryList=directoryList, relativedir=directory, currentdir=currentdir[2:])

@app.route("/play/music/<filename>/")
@app.route("/play/music/<directory>/<filename>/")
@app.route("/play/music/<directory1>/<directory>/<filename>/")
def play(filename=None, directory=None, directory1=None):
    if not directory:
        currentdir = musicDir
    elif not directory1:
        currentdir = join(musicDir, directory)
    else:
        currentdir = join(musicDir, join(directory1, directory))
    myfile = auto.File(join(currentdir,filename))
    name = myfile.title
    artist = myfile.artist
    album = myfile.album
    return render_template('player.html', name=name, filename=filename,
                           album=album, artist=artist)

@app.route("/")
@app.route("/<directory>/")
@app.route("/<directory1>/<directory>/")
@app.route("/<directory2>/<directory1>/<directory>/")
def mainroute(directory=None, directory1=None, directory2=None):
    if directory2:
        relativedir = join(directory2, join(directory1, directory))
    elif directory1:
        relativedir = join(directory1, directory)
    elif directory:
        relativedir = directory
    else:
        relativedir = None
    
    if relativedir:
        currentdir = join(musicDir, relativedir)
        if not isdir(currentdir):
            return redirect ("/play/"+currentdir)
    else:
        currentdir = "music"
        relativedir = ""

    directoryList =  [ d for d in listdir(currentdir) ]
    return render_template('dirlist.html',directoryList=directoryList, relativedir=relativedir, currentdir=currentdir)

if __name__ == "__main__":
    app.debug = True
    app.run()
