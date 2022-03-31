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

function details() {
  if(document.getElementById("details").className.includes("details-closed")) {
      document.getElementById("details").style.width = "45%";
      document.getElementById("details").style.visibility = "visible";
      document.getElementById("details").classList.add("details-open");
      document.getElementById("details").classList.remove("details-closed");
  }

  else{
      document.getElementById("details").style.width = "0";
      document.getElementById("details").style.boxShadow = "none";
      document.getElementById("details").style.visibility = "hidden";
      document.getElementById("details").classList.remove("details-open");
      document.getElementById("details").classList.add("details-closed");
  }   
}