
$(document).ready(function(){
    const fullList=$("main ul li p span em")
    fullList.each((index,element)=>{
        $(element).text()
        if($(element).text()==="True"){
            $(element).text("满员").prev().addClass("full")
        }else{
            $(element).text("未满员").removeClass("full")
        }
    })
})
