$(document).ready(function(){
    const signButton=$("#signUpForActivity")
    signButton.click(()=>{
        let actionVal=$(signButton.children()[0]).val()
        let userName=$('#username').text()
        let info={"username":userName,"action":actionVal}
        $.post(window.location.pathname,info,()=>{
            location.reload();
        })
    })
})