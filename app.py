<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">

    <script src="https://code.jquery.com/jquery-3.7.1.min.js" integrity="sha256-/JqT3SQfawRcv/BIHPThkBvs0OEvtFFmqPF/lYI/Cxo=" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery-validate/1.19.5/jquery.validate.min.js"></script>
    <script src="https://js.pusher.com/7.0/pusher.min.js"></script>

    <title>Inscripción a Curso</title>
</head>
<body>
    <div class="container">
        <!-- Formulario para inscribirse a un curso -->
        <form method="post" id="frmInscripciones" class="formulario">
            <div class="mb-1">
                <label id="lblNombreCurso" for="slNombreCurso">Nombre Curso:</label>
                <select name="slNombreCurso" id="slNombreCurso" class="form-control" required="true">
                    <option value="">Seleccione un curso</option>
                    <option value="prueba ahumada rodriguez">Prueba Ahumada Rodriguez</option>
                    <option value="curso2">Curso 2</option>
                </select>
            </div>
            <div class="mb-1">
                <label id="lblTelefono" for="txtTelefono">Teléfono:</label>
                <input type="text" name="txtTelefono" id="txtTelefono" class="form-control" required="true" minlength="10" maxlength="10" pattern="\d{10}" title="El teléfono debe tener 10 dígitos">
            </div>
            <div class="text-end">
                <button id="btnGuardarFA" name="btnGuardarFA" class="btn btn-dark">Guardar</button>
            </div>
        </form>

        <!-- Tabla para mostrar los datos registrados -->
        <h3 class="mt-4">Datos Registrados</h3>
        <table class="table table-sm">
            <thead>
                <tr>
                    <th>Curso</th>
                    <th>Teléfono</th>
                </tr>
            </thead>
            <tbody id="tbodyInscripciones">
                <!-- Aquí se mostrarán los datos desde el servidor -->
            </tbody>
        </table>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>

    <script>
        // Inicializa Pusher
        const pusher = new Pusher('99c33b12a2923c937f2d', {
            cluster: 'mt1'
        });
        const channel = pusher.subscribe('canalInscripciones');

        // Cuando se recibe un nuevo evento
        channel.bind('nuevaInscripcion', function(data) {
            agregarInscripcion(data.curso, data.telefono);
        });

        window.addEventListener("load", function (event) {
            // Función para agregar una inscripción a la tabla
            function agregarInscripcion(curso, telefono) {
                $("#tbodyInscripciones").append(`
                    <tr>
                        <td>${curso}</td>
                        <td>${telefono}</td>
                    </tr>
                `);
            }

            // Validación del formulario
            $("#frmInscripciones").validate({
                messages: {
                    slNombreCurso: {
                        required: "Seleccione un curso"
                    },
                    txtTelefono: {
                        required: "Ingrese su número de teléfono",
                        minlength: "El teléfono debe tener 10 dígitos",
                        maxlength: "El teléfono debe tener 10 dígitos",
                        digits: "El teléfono debe contener solo números"
                    }
                }
            });

            // Envío de datos al servidor
            $("#frmInscripciones").submit(function (event) {
                event.preventDefault();

                $.post("/inscripciones/guardar", $(this).serialize(), function (respuesta) {
                    console.log(respuesta);
                    // Actualizar la tabla después de guardar
                    buscarInscripciones();
                });
            });

            // Función para obtener los datos registrados de la tabla y mostrarlos en la tabla
            function buscarInscripciones() {
                $.get("/inscripciones/buscar", function (respuesta) {
                    $("#tbodyInscripciones").html(""); // Limpiamos el contenido anterior

                    // Recorremos los datos devueltos y los añadimos a la tabla
                    respuesta.forEach(function(inscripciones) {
                        $("#tbodyInscripciones").append(`
                            <tr>
                                <td>${inscripciones[1]}</td>
                                <td>${inscripciones[2]}</td>
                            </tr>
                        `);
                    });
                });
            }

            // Llamar a la función para cargar los datos al cargar la página
            buscarInscripciones();
        });
    </script>    
</body>
</html>
