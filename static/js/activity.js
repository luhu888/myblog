$(document).ready(function(){
    $('.persons ul li .substitute').each((index,element)=>{
       if( $(element).text()==="False"){
           $(element).text('正式')
       }else if( $(element).text()==="True"){
           $(element).text('替补')
       }
    })
})