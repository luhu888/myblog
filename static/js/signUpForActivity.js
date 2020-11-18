$(document).ready(function(){
    init()
    const signButton=$("#signUpForActivity")
    signButton.click(()=>{
        let actionVal=$(signButton.children()[0]).val()
        let userName=$('#username').text()
        let info={"username":userName,"action":actionVal}
        $.post(window.location.pathname,info,(result)=>{
            //result是string类型
            let index1=result.indexOf('<div class="pop">')
            let length=('<div class="pop">').length
            let index2=result.indexOf('<button id="tipsEndFlag">')
            let text=result.substring(index1+length,index2)
            let index3=text.indexOf('<p>')
            let index4=text.indexOf('</p>')
            let text2=text.substring(index3+3,index4)
            $(".pop p").text(text2)
                $(".pop").fadeIn(200)
                $(".mask").fadeIn(200)

        })
        $(".pop button").click(()=>{
            $(".pop").fadeOut(200)
            $(".mask").fadeOut(200)
            location.reload()
        })
    })
})
function init() {
    $(".pop").hide()
    $(".mask").hide()
}