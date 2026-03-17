import streamlit as st
import pandas as pd
import psycopg2  # Librería para base de datos externa
import hashlib
from fpdf import FPDF
from io import BytesIO
from PIL import Image
from datetime import datetime
import os

# --- CONEXIÓN A BASE DE DATOS EXTERNA ---
def conectar_db():
    # En Streamlit Cloud, agrega DB_URL en la sección "Secrets"
    try:
        conn = psycopg2.connect(st.secrets["DB_URL"])
        return conn
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return None

conn = conectar_db()
if conn:
    c = conn.cursor()

# --- INICIALIZACIÓN DE TABLAS (POSTGRESQL) ---
def iniciar_db():
    c.execute('''CREATE TABLE IF NOT EXISTS equipos (id TEXT PRIMARY KEY, nombre TEXT, categoria TEXT, stock INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios (username TEXT PRIMARY KEY, password TEXT, rol TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS info_empresa (id SERIAL PRIMARY KEY, nombre TEXT, direccion TEXT, telefono TEXT, email TEXT, web TEXT, logo BYTEA)''')
    c.execute('''CREATE TABLE IF NOT EXISTS remitos_maestro (id_remito TEXT PRIMARY KEY, cliente TEXT, fecha_salida DATE, estado TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS remitos_detalle (id_remito TEXT, id_item TEXT, nombre_item TEXT, cant_salida INTEGER, cant_retorno INTEGER)''')
    
    # Usuario Mauro por defecto
    mauro_pass = hashlib.sha256("Ju110520".encode()).hexdigest()
    c.execute("INSERT INTO usuarios (username, password, rol) VALUES ('Mauro', %s, 'Administrador') ON CONFLICT DO NOTHING", (mauro_pass,))
    conn.commit()

if conn: iniciar_db()

# --- [EL RESTO DE LA LÓGICA DE INTERFAZ SE MANTIENE IGUAL A LA ANTERIOR] ---
# Nota: En PostgreSQL se usa %s en lugar de ? para las consultas.
