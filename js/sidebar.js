$(document).ready(function () {
    $("#sidebar").mCustomScrollbar({
        theme: "minimal"
    });

    $('#sidebar-toggle').on('click', function () {
        $('#sidebar, #content, #sidebar-toggle').toggleClass('active');
        $('.collapse.in').toggleClass('in');
        $('a[aria-expanded=true]').attr('aria-expanded', 'false');
    });
});

function iwanttogo(){
    let config={}

        config.method='GET'
        config.header={'Content-Type':'application/json','Accept':'application/json'}
        let post_string="/spaa?restid="+restid

        fetch(post_string,config)
            .then(function (response){
                return response.json()
            })
            .catch(error => {
                console.error("error: ", error)
            })
            .then(myJson=>{
                console.log(myJson)

            })

}

function wtf(){
    let config={}

    config.method='GET'
    config.header={'Content-Type':'application/json','Accept':'application/json'}
    let get_string="/userinfo?restid="+"abcde"

    fetch(get_string,config)
        .then(function (response){
            return response.json()
        })
        .catch(error => {
            console.error("error: ", error)
        })
        .then(myJson=>{
            console.log(myJson)

        })
}