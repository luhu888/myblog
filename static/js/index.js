
$(document).ready(function(){
    const fullList=$("main ul li p span em")
    fullList.each((index,element)=>{
        $(element).text()
        if($(element).text()==="True"){
            $(element).text("已订满").prev().addClass("full")
        }else{
            $(element).text("报名中").removeClass("full")
        }
    })
})
