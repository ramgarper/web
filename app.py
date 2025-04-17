import sqlitecloud
from flask import Flask, render_template, request

app = Flask(__name__)

DATABASE_URL = "sqlitecloud://cwp5upgjhz.g4.sqlite.cloud:8860/my-vessel?apikey=pMS6KmQ7pfKA6kztZkKsbb63zPle46bjdzCNwAajV1I"

def get_db_connection():
    conn = sqlitecloud.connect(DATABASE_URL)
    return conn

@app.route('/', methods=['GET', 'POST'])
def buscar_barco():
    caracteristicas = None
    foto_barco = None   # <--- Defínela aquí SIEMPRE
    if request.method == 'POST':
        nombre = request.form['nombre']
        conn = get_db_connection()
        cursor = conn.execute("SELECT * FROM caracteristicas WHERE LOWER(nombreDelBarco) = LOWER(?)", (nombre,))
        row = cursor.fetchone()
        conn.close()
        if row:
            campos = [
                'id', 'nombreDelBarco', 'Tamaño', 'altillos', 'puente/chimenea',
                'picos', 'pasaElPuente', 'tochos', 'gap', 'cautivos', 'recogerMaterial'
            ]
            caracteristicas = dict(zip(campos, row))
            nombre_archivo = f"{caracteristicas['nombreDelBarco'].lower()}.jpg"
            foto_barco = f"barcos/{nombre_archivo}"
    return render_template('buscar.html', caracteristicas=caracteristicas, foto_barco=foto_barco)




if __name__ == '__main__':
    app.run(debug=True)
