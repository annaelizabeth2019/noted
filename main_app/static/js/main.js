var navDrop = document.getElementsByClassName('.dropdown-trigger');
M.Dropdown.init(navDrop, {
    hover: true,
    coverTrigger: false,
    closeOnClick: false
});

var sideNav = document.querySelectorAll('.sidenav');
M.Sidenav.init(sideNav);

// initialize the parallax elements
var parallaxEls = document.querySelectorAll('.parallax');
function initParallax(instances) {
    if (instances.length > 0) {
        for(var i = 0; i < instances.length; i++) {
            M.Parallax.init(instances[i]);
        }
    }
}
initParallax(parallaxEls)
