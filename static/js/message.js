console.log("hi");

try{
const schedule=document.querySelector('.notify-schedule');
schedule.lastChild.addEventListener('click',()=>{schedule.style.display="none";document.querySelector('.notify-schedule-bg').style.display="none";});

notifymsg.lastChild.addEventListener('click',()=>{notifymsg.style.display="none";})}
catch{
   console.log("error in notify-schedule msg");
}
try{
const msgsuccess=document.querySelector('.msgsuccess');
msgsuccess.lastChild.addEventListener('click',()=>{msgsuccess.style.display="none";});}
catch{
console.log("error in msgsuccess");
}
try{
const msgpending=document.querySelector('.msgpending');
msgpending.lastChild.addEventListener('click',()=>{msgpending.style.display="none";});}
catch{
   console.log("error in msgpending");
}
