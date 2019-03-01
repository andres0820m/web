
var q1Keyworks="comportamiento inteligente";
var goodOnes =0;
var badOnes=0;
function check() {
radianChecks();
textCheck();
lookCheckBox(document.getElementsByName("rta"));
check12();
h=document.getElementById("myNumber").value;
if(h==1997)
{
goodOnes++;
}
alert("Tuviste "+goodOnes+" de 20 preguntas");

goodOnes=0;
badOnes=0;
}

function radianChecks() {
var q;
q=document.getElementsByName("3");
lookRadio(1,q);
q=document.getElementsByName("4");
lookRadio(2,q);
q=document.getElementsByName("6");
lookRadio(0,q);
q=document.getElementsByName("7");
lookRadio(0,q);
q=document.getElementsByName("8");
lookRadio(3,q);
q=document.getElementsByName("9");
lookRadio(0,q);
q=document.getElementsByName("10");
lookRadio(0,q);
q=document.getElementsByName("12");
lookRadio(0,q);
q=document.getElementsByName("13");
lookRadio(2,q);
q=document.getElementsByName("15");
lookRadio(0,q);
q=document.getElementsByName("16");
lookRadio(0,q);
q=document.getElementsByName("17");
lookRadio(2,q);
q=document.getElementsByName("18");
lookRadio(1,q);
q=document.getElementsByName("19");
lookRadio(2,q);

}
function textCheck() {
  x=document.getElementById("text1").value;
  lookText(x,q1Keyworks);
  x=document.getElementById("text2").value;
  lookText(x,"si");
  x=document.getElementById("text6").value;
  lookText(x,"no");
}

function lookText(element,q1Keywork) {
  if(element.search(q1Keywork)!=-1)
  goodOnes++;
  else {
    badOnes++;
  }
}
function lookRadio(index,element) {
  if (element[index].checked) {
  goodOnes++;
}else {
  badOnes++;
}
}
function lookCheckBox(element) {
if (element[0].checked&&element[2].checked&&element[3].checked&&element[5].checked) {
if (element[1].checked||element[4].checked||element[6].checked) {
badOnes++;
}else {
  goodOnes++;
}

}
}
function lookText2(element,q1Keywork) {
  if(element.search(q1Keywork)!=-1)
  return true;
  else {
    return false;
  }
}
function check12()
{
  x=document.getElementById("text3").value;
  if(lookText2(x,"es"))
  {
    x=document.getElementById("text4").value;
    if (lookText2(x,"la")) {
    x=document.getElementById("text5").value;
    if(lookText2(x,"artificial"))
    {
    goodOnes++;
  }
  }else {
    badOnes++;
  }
  }else {
    badOnes++;
  }

}
