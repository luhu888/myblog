console.log('222')

$(document).ready(function(){
    $('.persons ul li .substitute').each((index,element)=>{
       if( $(element).text()==="False"){
           $(element).text('正式')
       }else{
           $(element).text('替补')
       }
    })
})