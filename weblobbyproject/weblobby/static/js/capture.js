// Original: http://coderthoughts.blogspot.co.uk/2013/03/html5-video-fun.html
// Adaptado por: Neuton Martins Costa

var video;
var dataURL;
var webcamStream;

// Inicializa de acordo com o navegador
function setup() {
    navigator.myGetMedia = (navigator.getUserMedia ||
    navigator.webkitGetUserMedia ||
    navigator.mozGetUserMedia ||
    navigator.msGetUserMedia);
    navigator.myGetMedia({ video: true }, connect, error);
}

// Conecta o fluxo a tag "video" para dar feedback quando for tirar a foto
function connect(stream) {
    video = document.getElementById('video');
    video.src = window.URL ? window.URL.createObjectURL(stream) : stream;
    video.play();
    webcamStream = stream;
}

// Fecha o fluxo da webcam, importante para não deixar a webcam ativa o tempo todo
function closestream() {
	webcamStream.stop();
}

// Loga os erros no console
function error(e) {
	console.log(e);
}

// Captura a imagem efetivamente, coloca a imagem em base64 num campo oculto do form.
// Além disso gera uma miniatura prévia.
function captureImage() {
    var canvas = document.createElement('canvas');
    canvas.id = 'hiddenCanvas';
    
    // Adiciona o canvas ao corpo do documento
    document.body.appendChild(canvas);
    document.getElementById('canvasHolder').appendChild(canvas);
    
    var ctx = canvas.getContext('2d');

    // Guarda em diferentes resoluções dependendo da proporção
    if (video.videoWidth/video.videoHeight == 4/3) {
        canvas.width = 640;
        canvas.height = 480;
    }
    else if (video.videoWidth/video.videoHeight == 16/9) {
        canvas.width = 640;
        canvas.height = 360;
    }
    else if (video.videoWidth/video.videoHeight == 16/10) {
        canvas.width = 640;
        canvas.height = 400;
    }
    else {
        return;
    }

    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    
    // Converte o canvas para dataurl
    // Guarda como JPEG, fator de compressão 0.9
    dataURL = canvas.toDataURL('image/jpeg', 0.9);
    // Coloca a imagem na miniatua de prévia
    document.getElementById('thumbnailPreview').src = dataURL;
    // Coloca a imagem em base64 no campo oculto do form
    document.getElementById('id_image_path').value = dataURL;
    
    closestream();
    $('#pictureModal').modal('toggle')
}

// Registra para acionar os eventos no momento adequado.
document.getElementById('takePictureBtn').addEventListener("click", setup);
document.getElementById('storePictureModal').addEventListener("click", captureImage);
document.getElementById('closePictureModal').addEventListener("click", closestream);
document.getElementById('cancelPictureModal').addEventListener("click", closestream);