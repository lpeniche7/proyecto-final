var objXMLHTTP = new XMLHttpRequest();

objXMLHTTP.open('GET', 'http://127.0.0.1:5000/miApi/mensaje/');

objXMLHTTP.addEventListener('load', completado);
objXMLHTTP.addEventListener('error', manejarError);
objXMLHTTP.addEventListener('progress', progreso);
objXMLHTTP.addEventListener('abort', abortado);

objXMLHTTP.send();


function manejarError(evt)
{
    console.log('ocurrio un error.');
}

function progreso(evt)
{
    var procentaje = evt.loaded / evt.total * 100;
    console.log(procentaje);
}


function abortado(evt)
{
    console.log('cancelado');
}




function completado(evt)
{

    var data =  JSON.parse(this.response);

    console.log(data);

    var info="";

    for(var i =0; i < data.length; i++)
    {
        var mensaje = data[i];
        info += "<div class= 'mensaje'><p class='asunto'>" +mensaje.asunto + "</p>"
        info += "<p class='contenidoMensaje'>" +mensaje.mensaje + "</p>"
        info += "<p class='usuario'>" +mensaje.usuario + "</p></div>"
        
    }

   

    

    document.getElementById('respuesta').innerHTML= info;

}