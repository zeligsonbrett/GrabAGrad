/*function openNav() {
    document.getElementById("mySidenav").style.width = "300px";
    document.getElementById("main").style.marginLeft = "250px";
  }
  
function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
    document.getElementById("main").style.marginLeft= "0";
} */

function openNav() {
  if(document.getElementById("mySidenav").className.includes("menu-closed")) {
      document.getElementById("mySidenav").style.width = "300px";
      document.getElementById("filter").style.visibility = "visible";
      document.getElementById("mySidenav").classList.add("menu-open");
      document.getElementById("mySidenav").classList.remove("menu-closed");
      document.getElementById("main").style.marginLeft = "315px";
  }

  else{
      document.getElementById("filter").style.visibility = "hidden";
      document.getElementById("mySidenav").style.width = "0";
      document.getElementById("mySidenav").style.boxShadow = "none";
      document.getElementById("mySidenav").classList.remove("menu-open");
      document.getElementById("mySidenav").classList.add("menu-closed");
      document.getElementById("main").style.marginLeft= "20px";
  }    
}