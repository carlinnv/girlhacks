from flask import Flask, render_template, request, url_for, redirect
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import Integer, String
# from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column 
# import discussion

def get_title(): 
    title = request.form.get("")