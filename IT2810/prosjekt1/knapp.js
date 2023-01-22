var hiddenDiv = $("#kravDok");
console.log("her");
$("#button").on("click", function (event){

    if(hiddenDiv.is(":hidden")){
        hiddenDiv.show();        
    }
    else{
        hiddenDiv.hide();
    }

} )

--$("#knapp").click(function() {
--    alert( "Handler for called." );
--});