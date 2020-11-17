$(document).ready(function(){
    init()
    const signButton=$("#signUpForActivity")
    signButton.click(()=>{
        let actionVal=$(signButton.children()[0]).val()
        let userName=$('#username').text()
        let info={"username":userName,"action":actionVal}
        $.post(window.location.pathname,info,()=>{

            // $(".pop p").text(text)
            // text应该取页面最新的返回值或者py文件的返回值
                let text=$(".pop p").text()
                $(".pop p").text(text)
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