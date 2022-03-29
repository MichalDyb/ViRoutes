/*jshint esversion: 6 */
// ^^ Wskazanie wersji skryptu JavaScript


function setCopyright() {
    var copyright = document.getElementById('footer_copyright');
    var date = new Date().getFullYear();
    copyright.innerHTML = '&copy; ' + date + ' Michał Dybaś oraz Karpacka Państwowa Uczelnia w Krośnie';
}

function showTime(){
    var date = new Date();
    var hours = date.getHours();
    var minutes = date.getMinutes(); 
    var seconds = date.getSeconds(); 
    hours = (hours < 10) ? '0' + hours : hours;
    minutes = (minutes < 10) ? '0' + minutes : minutes;
    seconds = (seconds < 10) ? '0' + seconds : seconds;
    var time = hours + ':' + minutes + ':' + seconds;
    document.getElementById('page_header_clock').innerText = time;
    document.getElementById('page_header_clock').textContent = time;
    setTimeout(showTime, 1000);
}

function hideShowTopLink() {
    var link_button = document.getElementById('link_to_top');
    if (window.pageYOffset > 0) { 
        link_button.style.display = 'flex'; 
    }
    else { 
        link_button.style.display = 'none'; 
    }
}

var showCollapsedMenuIntervalId = null;
var hideCollapsedMenuIntervalId = null;
var close = true;
function showHideCollapsedMenu() {
    var menu = document.getElementById('page_header_collapsed_menu');
    if(close == true) {
        close = false;
        clearInterval(hideCollapsedMenuIntervalId);
        showCollapsedMenuIntervalId = setInterval(frame, 10);
        var pos = menu.offsetLeft;
        function frame() {
            for (var i = 0; i < 20; i++) {
                if (pos >= 0) {
                    clearInterval(showCollapsedMenuIntervalId);
                } 
                else {
                    pos++; 
                    menu.style.left = pos + 'px'; 
                }
            }
        }
    }
    else {
        close = true;
        clearInterval(showCollapsedMenuIntervalId);
        hideCollapsedMenuIntervalId = setInterval(frame, 10);
        var pos = menu.offsetLeft;
        function frame() 
        {
            for (var i = 0; i < 20; i++) {
                if (pos <= -240) {
                    Object.keys(document.getElementsByClassName('page_header_collapsed_menu_content_description_dynamic')).forEach(key => {
                        document.getElementsByClassName('page_header_collapsed_menu_content_description_dynamic')[key]
                            .classList.remove('page_header_collapsed_menu_content_description_show_links');
                    });
                    clearInterval(hideCollapsedMenuIntervalId);
                } 
                else {
                    pos--; 
                    menu.style.left = pos + 'px'; 
                }
            }
        }
    }
}

Object.keys(document.getElementsByClassName('page_header_collapsed_menu_content_description_dynamic')).forEach(key => {
    document.getElementsByClassName('page_header_collapsed_menu_content_description_dynamic')[key].addEventListener('click', function() {
        this.classList.toggle('page_header_collapsed_menu_content_description_show_links');
    });
});
window.addEventListener('load', function() {
    setCopyright();
    hideShowTopLink();
    showTime();
});
window.addEventListener('scroll', function() {
    hideShowTopLink();
});
document.getElementById('link_to_top').addEventListener('click', function() {
    window.scrollTo(0,0);
    hideShowTopLink();
});
document.getElementById('page_header_menu_button').addEventListener('click', function() {
    showHideCollapsedMenu();
});