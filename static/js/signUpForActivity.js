$(document).ready(function(){
    init()
    const signButton=$("#signUpForActivity")
    signButton.click(()=>{
        let actionVal=$(signButton.children()[0]).val()
        let userName=$('#username').text()
        let info={"username":userName,"action":actionVal}
        $.post(window.location.pathname,info,()=>{
            let text="{{ txt }}"
            // $(".pop p").text(text)
           $(".pop p").text("报名成功")
                $(".pop").fadeIn(200)
                $(".mask").fadeIn(200)
            console.log(text)
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