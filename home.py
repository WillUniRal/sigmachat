from __main__ import app
import sqlite3 as mysql
from flask import Flask, render_template, jsonify, request, redirect
from tables import credentials
import bcrypt

@app.route('/home', methods = ['GET'])
def home():
    return render_template('home.html')

print("name")