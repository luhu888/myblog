$(document).ready(function(){
    init()
    const signButton=$("#signUpForActivity")
    let actionVal=$(signButton.children()[0]).val()

    //给到字段值判断是否可以取消，不可取消的话置灰，点击给到不可取消的tips
    //if(actionVal==="cancel"&& xxx===false){
    // signButton.addClass("disabled")
    // }

    signButton.click(()=>{

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
                $(".pop").fadeIn(200).delay(600).fadeOut(200)
                $(".mask").fadeIn(200).delay(600).fadeOut(200)
                setTimeout(()=>{location.reload()},1000);
        })
        // 按钮和定时器两种样式
        // $(".pop button").click(()=>{
        //     $(".pop").fadeOut(200)
        //     $(".mask").fadeOut(200)
        //     location.reload()
        // })
    })
})
function init() {
    $(".pop").hide()
    $(".mask").hide()
}