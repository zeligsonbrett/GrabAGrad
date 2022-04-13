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
      document.getElementById("mySidenav").style.width = "360px";
      document.getElementById("filter").style.visibility = "visible";
      document.getElementById("mySidenav").classList.add("menu-open");
      document.getElementById("mySidenav").classList.remove("menu-closed");
      document.getElementById("main").style.marginLeft = "315px";
      document.getElementById("sort").style.height="40px";
      document.getElementById("sort").style.marginTop="40px";
      document.getElementById("search").style.height="80px";
      document.getElementById("details").style.width = "calc(100vw - 425px)";
  }

  else{
      document.getElementById("mySidenav").classList.remove("menu-open");
      document.getElementById("mySidenav").classList.add("menu-closed");  
      document.getElementById("filter").style.visibility = "hidden";
      document.getElementById("mySidenav").style.width = "0";
      document.getElementById("sort").style.height="0";
      document.getElementById("search").style.height="0";
      document.getElementById("mySidenav").style.boxShadow = "none";
      
      document.getElementById("main").style.marginLeft= "20px";
      document.getElementById("details").style.width = "calc(100vw - 110px)";
  }    
}

function details() {
  if(document.getElementById("details").className.includes("details-closed")) {
      document.getElementById("details").style.visibility = "visible";
      document.getElementById("details").classList.add("details-open");
      document.getElementById("details").classList.remove("details-closed");
  }

  else{
      document.getElementById("details").style.visibility = "hidden";
      document.getElementById("details").classList.remove("details-open");
      document.getElementById("details").classList.add("details-closed");
  }   
}

function changeName(input){
  var elementValue = input.value;
  if (elementValue == "") elementValue = '...';
  if (elementValue.length > 12 && input.id == "name") elementValue = elementValue.substring(0, 10) + "...";
  if (elementValue.length > 20) elementValue = elementValue.substring(0, 20) + "...";
	document.getElementById(input.id + "Card").innerHTML = elementValue;
}
