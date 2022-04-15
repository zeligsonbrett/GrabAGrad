const heightOutput = document.querySelector('#height');
const widthOutput = document.querySelector('#width');

function reportWindowSize() {
  if(window.innerWidth >= 780){
    if(document.getElementById("mySidenav").style.width != "40px"){
      document.getElementById("mySidenav").style.width = "330px";
      document.getElementById("mySidenav").style.height = "calc(100vh - 50px)";
      document.getElementById("details").style.width = "calc(100vw - 400px)";
      document.getElementById("details").style.height = "calc(100vh - 90px)";
      document.getElementById("main").style.marginLeft = "315px";
      document.getElementById("mySidenav").classList.add("menu-open");
      document.getElementById("filter").style.visibility = "visible";
    }
  }

  else{
    if(document.getElementById("mySidenav").style.height != "90px"){
      document.getElementById("mySidenav").style.height = "470px";
      document.getElementById("mySidenav").style.boxShadow = "none";
      document.getElementById("mySidenav").style.width = "100vw";
      document.getElementById("main").style.marginLeft= "0px";
      document.getElementById("mySidenav").classList.add("menu-open");
      document.getElementById("filter").style.visibility = "visible";
      document.getElementById("details").style.width = "90vw";
      document.getElementById("details").style.height = "calc(100vh - 150px)";
    }
  }
  document.getElementById("sortby").style.height="40px";
}

window.onresize = reportWindowSize;

function openNav() {
  if(document.getElementById("mySidenav").className.includes("menu-closed")) {
      document.getElementById("filter").style.visibility = "visible";
      document.getElementById("mySidenav").classList.add("menu-open");
      document.getElementById("mySidenav").classList.remove("menu-closed");
      document.getElementById("sortby").style.height="40px";
      
      if (window.innerWidth > 780){
        document.getElementById("mySidenav").style.width = "330px";
        document.getElementById("details").style.width = "calc(100vw - 400px)";
        document.getElementById("details").style.height = "calc(100vh - 90px)";
        document.getElementById("main").style.marginLeft = "315px";
        document.getElementById("mySidenav").style.height = "calc(100vh - 50px)";
      }
      else{
        document.getElementById("mySidenav").style.height = "470px";
        document.getElementById("mySidenav").style.width = "100vw";
        document.getElementById("details").style.width = "90vw";
        document.getElementById("details").style.height = "calc(100vh - 150px)";
        document.getElementById("main").style.marginLeft = "0";
        
      }
  }

  else{
      document.getElementById("mySidenav").classList.remove("menu-open");
      document.getElementById("mySidenav").classList.add("menu-closed");  
      document.getElementById("filter").style.visibility = "hidden";
      document.getElementById("sortby").style.height="0";
      document.getElementById("mySidenav").style.boxShadow = "none";

      if (window.innerWidth > 780){
        document.getElementById("mySidenav").style.width = "40px";
        document.getElementById("mySidenav").style.height = "calc(100vh - 50px)";
        document.getElementById("details").style.width = "calc(100vw - 110px)";
        document.getElementById("details").style.height = "calc(100vh - 90px)";
        document.getElementById("main").style.marginLeft= "20px";
        
      }
      else{
        document.getElementById("mySidenav").style.height = "90px";
        //document.getElementById("details").style.height = "calc(100vh - 400px)";
        document.getElementById("details").style.width = "90vw";
      }      
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

function showCard(){
  document.getElementById("card-mockup").style.visibility = "visible";    
}

function changeName(input){
  var elementValue = input.value;
  console.log(input.id);
  if (elementValue == "") elementValue = '...';
  else if (elementValue.length > 15 && input.id == "name") elementValue = elementValue.substring(0, 10) + "...";
  //else if (elementValue.length > 100 && input.id == "research-focus") elementValue = elementValue.substring(0, 100) + "...";
  else if (elementValue.length > 20) elementValue = elementValue.substring(0, 20) + "...";
	document.getElementById(input.id + "Card").innerHTML = elementValue;
}
