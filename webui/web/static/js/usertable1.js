
function openNav() {
  document.getElementById("mySidenav").style.width = "250px";
}

function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
}

var modal = document.getElementById("myModal");
var modal2 = document.getElementById("myModal2");
// Get the button that opens the modal
//var btn = document.getElementById("open")
var btns = document.getElementsByName("open");
for (let i = 0; i < btns.length; i++)
{
  btns[i].onclick = function() {
    modal.style.display = "block";
  }
}

var btns2 = document.getElementsByName("edit");
for (let i = 0; i < btns.length; i++)
{
  btns2[i].onclick = function() {
    modal2.style.display = "block";
  }
}

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];
var span2 = document.getElementsByClassName("close")[1];
var close3 = document.getElementById("save")
// When the user clicks on <span> (x), close the modal
span.onclick = function() {
    modal.style.display = 'none';
}

span2.onclick = function() {
    modal2.style.display = 'none';
}

close3.onclick = function() {
    modal2.style.display = 'none';
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  } else if (event.target == modal2) {
    modal2.style.display = "none";
  }
}

//var delete = document.getElementById("delete")
//delete.onclick = function() {
//    }
