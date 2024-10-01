from flask import Flask, render_template, request
import pusher
import mysql.connector
import datetime
import pytz

# Conexión a la base de datos
con = mysql.connector.connect(
    host="185.232.14.52",
    database="u760464709_tst_sep",
    user="u760464709_tst_sep_usr",
    password="dJ0CIAFF="
)

app = Flask(__name__)

# Configuración de Pusher
pusher_client = pusher.Pusher(
    app_id="1873320",
    key="99c33b12a2923c937f2d",
    secret="3de27c12dd4f28811cde",
    cluster="mt1",
    ssl=True
)

# Ruta principal para mostrar la página de inscripciones
@app.route("/")
def index():
    return render_template("inscripciones.html")

# Ruta para guardar la inscripción a un curso
@app.route("/inscripcion/guardar", methods=["POST"])
def inscripcion_guardar():
    nombre_curso = request.form["slNombreCurso"]
    telefono = request.form["txtTelefono"]

    if not con.is_connected():
        con.reconnect()

    # Insertar los datos en la base de datos
    cursor = con.cursor()
    sql = "INSERT INTO tst0_cursos (Nombre_Curso, Telefono) VALUES (%s, %s)"
    val = (nombre_curso, telefono)
    cursor.execute(sql, val)
    con.commit()

    # Enviar evento con Pusher
    pusher_client.trigger("canalInscripciones", "nuevaInscripcion", {
        "curso": nombre_curso,
        "telefono": telefono
    })

    con.close()
    return "Inscripción guardada con éxito"

# Ruta para buscar las inscripciones registradas
@app.route("/inscripcion/buscar", methods=["GET"])
def inscripcion_buscar():
    if not con.is_connected():
        con.reconnect()

    # Recuperar los datos de la base de datos
    cursor = con.cursor()
    cursor.execute("SELECT * FROM tst0_cursos")
    registros = cursor.fetchall()

    con.close()
    return registros

if __name__ == "__main__":
    app.run(debug=True)
