
var form = document.forms['productDetails'];

form.onsubmit = function (e){
    e.preventDefault();
    var orders = JSON.parse(localStorage.getItem('orders'));
    var total = localStorage.getItem('total');

    if(orders === null || orders === undefined){
        localStorage.setItem('orders', JSON.stringify([]));
        orders = JSON.parse(localStorage.getItem('orders'));
    }

    if(total === null || total === undefined){
        localStorage.setItem('total', 0);
        total = localStorage.getItem('total');
    }

    //var select =document.getElementById("id16").value; funciona

    var select =document.getElementsByName("idtd");
    console.log(select.item(0))


    //window.alert(idTallaDisponible+ '  -  '+quantity);
    window.alert("hola "+select.item(0));

}