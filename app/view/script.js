const heightOutput = document.querySelector('#height');
const widthOutput = document.querySelector('#width');
/*let saved_n = ""
let saved_a = ""
let saved_y = ""
let saved_u = ""
let saved_m = ""
let saved_e = ""
let saved_p = ""
let saved_r = "" 
let saved_i = ""
*/

function reportWindowSize() {
  if(window.innerWidth >= 780){
    document.getElementById("top-right-img").src = "/view/expandedLogo.png";
    document.getElementById("top-right-img").style.width = "180px";
  }

  else{
    document.getElementById("top-right-img").src = "/view/favicon.ico";
    document.getElementById("top-right-img").style.width = "35px";
  }
  
  if(document.getElementById("mySidenav") != null) {
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
        document.getElementById("mySidenav").style.height = "490px";
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
    document.getElementById("form-id").style.height="100%";
  }
  else{
    document.getElementById("details").style.width = "95vw";
    document.getElementById("details").style.height = "calc(100vh - 100px)";
  }
}

window.onresize = reportWindowSize;

function openNav() {
  if(document.getElementById("mySidenav").className.includes("menu-closed")) {
      document.getElementById("filter").style.visibility = "visible";
      document.getElementById("mySidenav").classList.add("menu-open");
      document.getElementById("mySidenav").classList.remove("menu-closed");
      document.getElementById("sortby").style.height="40px";
      document.getElementById("form-id").style.height="100%";
      
      if (window.innerWidth > 780){
        document.getElementById("mySidenav").style.width = "330px";
        document.getElementById("details").style.width = "calc(100vw - 400px)";
        document.getElementById("details").style.height = "calc(100vh - 90px)";
        document.getElementById("main").style.marginLeft = "315px";
        document.getElementById("mySidenav").style.height = "calc(100vh - 50px)";
      }
      else{
        document.getElementById("mySidenav").style.height = "490px";
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
      document.getElementById("form-id").style.height="0";
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
  document.querySelector('#mockup-btn').textContent = "Close Mockup";    
  document.getElementById("mockup-btn").setAttribute('onclick', 'closeCard()')
  document.getElementById("mockup-btn").style.backgroundColor = "#FFB98B";
  document.getElementById("mockup-btn").style.color = "black"; 
}

function closeCard(){
  document.getElementById("card-mockup").style.visibility = "hidden"; 
  document.querySelector('#mockup-btn').textContent = "See Your Profile Card";  
  document.getElementById("mockup-btn").setAttribute('onclick', 'showCard()');
  document.getElementById("mockup-btn").style.backgroundColor = "black";
  document.getElementById("mockup-btn").style.color = "white";
}
/*
function saveData(){
  saved_n = document.getElementById("name").value;
  saved_a = document.getElementById("academic-dept").value;
  saved_y = document.getElementById("years-worked").value;
  saved_u = document.getElementById("undergrad-institution").value;
  saved_m = document.getElementById("masters-institution").value;
  saved_e = document.getElementById("email").value;
  saved_p = document.getElementById("phone-number").value;
  saved_r = document.getElementById("research-focus").value;
  saved_i = document.getElementById("industries").value;
//    var field = input.id;
//  if (field == "academic-dept") return {{grad.get_acad_dept()}};
//  else if (field == "years-worked") return {{grad.get_years_worked()}};
//  else if (field == "undergrad-institution") return {{grad.get_undergrad_university()}};
//  else if (field == "masters-institution") return {{grad.get_masters_university()}};
//  else if (field == "email") return {{grad.get_contact()}};
//  else if (field == "phone-number") return {{grad.get_contact()}};
//  else if (field == "research-focus") return {{grad.get_research_focus()}};
//  else if (field == "industries") return {{grad.get_industries()}};
} */

function changeName(input){
  var elementValue = input.value;
  if (elementValue.length == 0) {
    elementValue = '';
  }
  else if (elementValue.length > 8 && input.id == "first-name") elementValue = elementValue.substring(0, 6) + "...";
  //else if (elementValue.length > 100 && input.id == "research-focus") elementValue = elementValue.substring(0, 100) + "...";
  else if (elementValue.length > 20) elementValue = elementValue.substring(0, 20) + "...";
	document.getElementById(input.id + "Card").innerHTML = elementValue;
}
