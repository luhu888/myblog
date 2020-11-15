$(document).ready(function(){
    const signButton=$("#signUpForActivity")
    signButton.click(()=>{
        let actionVal=$(signButton.children()[0]).val()
        let userName=$('#username').text()
        let info={"username":userName,"action":actionVal}
        $.post("/new_user/activity/1.html",info,()=>{
            location.reload();
        })
    })

})