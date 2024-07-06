let fd;

let flag=1;
function handlepack(){
    
    if(flag)
    {document.querySelector('.animated-mail').classList.remove('animated-mail_open');
    document.querySelector('.letter').classList.remove('letter_open');
    document.querySelector('.top-fold').classList.remove('top-fold_open');
    document.querySelector('#pack-mail').innerHTML='Unpack';
    document.querySelector('#deliver').style.display='flex';
    flag=0;
}
    else{
      document.querySelector('.animated-mail').classList.add('animated-mail_open');
    document.querySelector('.letter').classList.add('letter_open');
    document.querySelector('.top-fold').classList.add('top-fold_open');
    document.querySelector('#pack-mail').innerHTML='Confirm and pack';
    document.querySelector('#deliver').style.display='none';
    flag=1;
    }

}

document.getElementById('designemailbtn').addEventListener("click",handledesignemail);
// document.getElementById('previewbtn').addEventListener("click",handlepreview);
document.getElementById('attach_file').addEventListener("change",handleimgupload);
function handledesignemail(e){
e.preventDefault();
document.getElementById('secondframe').scrollIntoView({behavior:"smooth"});
}

let imgurl;let emailimg;
function handleimgupload(e){
   
    const imageFiles = e.target.files;
    const imageFilesLength = imageFiles.length;
    if (imageFilesLength > 0) {
        emailimg=imageFiles[0];
        let imageSrc = URL.createObjectURL(imageFiles[0]);
        imgurl=imageSrc;
        document.getElementById('attach_file_name').innerHTML=imageFiles[0].name;
}}


document.querySelector('#recieverfile').addEventListener('change',fileupload);
let sheetData,file;
function fileupload(e){
    console.log("ok");
     file=e.target.files[0];
    var allowedExtensions = /(\.xlsx)$/i;    
    if( file && allowedExtensions.exec(file.name))
   {document.querySelector('.uploadfilewrapper').innerText=file.name;
   const reader = new FileReader();
   reader.onload = (event) => {
     const data = new Uint8Array(event.target.result);
     const workbook = XLSX.read(data, { type: 'array' });
     const sheetName = workbook.SheetNames[0];
     const worksheet = workbook.Sheets[sheetName];
      sheetData = XLSX.utils.sheet_to_json(worksheet, { header: 1 });
     };
    reader.readAsArrayBuffer(file);
   }
   else
   alert("please upload in excel format");
}




const form2=document.getElementById('secondframeform');
form2.addEventListener('submit',(e)=>{
    e.preventDefault();
  
    fd=new FormData(form2);
    fd.append('img',emailimg);
    fd.append('excelfile',file);

    let message=document.getElementById('message').value;
    const regExp = /\{(.*?)\}/g;
    const array=message.match(regExp);
    let matches=[];
    if(array){
     matches = [...array];}
    if(matches.length>0){
    for(let i=0;i<matches.length;i++){
    
    message=message.replaceAll(matches[i],(m)=>{
    let j=-1;
    let key=matches[i].substr(1,matches[i].length-2);
    for(let x=0;x<sheetData[0].length;x++){
       
       if(sheetData[0][x].toLowerCase()===key.toLowerCase()){
           j=x;break;
       }
    }
   
    if(j!==-1)
    {
       return sheetData[1][j];
    }
   
   })
 }
}
const attach_link=document.getElementById('attach_link').value;
const buttonname=document.getElementById('buttonname').value;
const poster_link=document.getElementById('poster_link').value;
let buttonelem="";
if(buttonname!="")
  buttonelem=`<a href="${attach_link}"><button style="width:auto;height:30px;background:orange;border:none;color:white;border-radius:5px;position:relative;left:33%">${buttonname}</button></a>`;
const templatecontent=`<div style="background:white;border-radius:10px;min-height:200px;width:200px;margin:auto;"><img src="${poster_link}" style="max-width:200px"/>${message}<br>${buttonelem}</div>`;
const htmltemplate=`<div style='background:#fcf4eb;min-height:200px;max-height:300px;overflow-y:scroll;'>${templatecontent}</div>`;

document.querySelector('.letter-title').innerHTML=document.getElementById('subject').value;
document.querySelector('.letter-context').innerHTML=htmltemplate;
document.querySelector('.letter-poster').style.backgroundImage=`url(${imgurl})`;
document.getElementById('thirdframe').scrollIntoView({behavior:"smooth"});

});
    
    

function handledeliver(){
        if(document.querySelector('#recieverfile').files[0]==null){
          document.querySelector('.msgpending').style.display='flex';
          document.querySelector('.msgpending').querySelector('p').innerText="Recipients file not found!";
          return;}

        const subject= document.getElementById('subject').value;
        const datetime=document.getElementById('schedule-datetime').value;
        const campaignname=document.getElementById('campaign_name').value;
        const attach_link=document.getElementById('attach_link').value;
        const buttonname=document.getElementById('buttonname').value;

        if(campaignname==""){
          document.querySelector('.msgpending').style.display='flex';
          document.querySelector('.msgpending').querySelector('p').innerText="Campaign name not given!";
          return;}
        if(datetime==""){
        document.querySelector('.msgpending').style.display='flex';
        document.querySelector('.msgpending').querySelector('p').innerText="datetime not selected!";
        return;}

        let buttonelem="";
        if(buttonname!="")
        buttonelem=`<div style="margin-left:45%;"><a href="${attach_link}"><button style="width:auto;height:30px;background:orange;border:none;color:white;border-radius:5px;margin-left:45%;">${buttonname}</button></a></div>`;
        const poster_link=document.getElementById('poster_link').value;
        const message=document.getElementById('message').value;
        const templatecontent=`<div style="background:white;border-radius:10px;min-height:50%;width:70%;margin:auto;"><img src="${poster_link}" style="max-width:100%"/><div style="font-size:15px;font-family:cursive;padding:10px">${message}</div><br>${buttonelem}</div>`;
        const htmltemplate=`<div style="background:#fcf4eb;min-height:50%">${templatecontent}</div>`;
         fd.append('subject',subject);
         fd.append('message',htmltemplate);
         fd.append('schedule-datetime',datetime);
         fd.append('campaign-name',campaignname);
         
      
         sendmail(fd);
     }
async function sendmail(data){
 
        document.querySelector('.msgpending').style.display='flex';
        document.querySelector('.msgpending').querySelector('p').innerText="Scheduling your mail!";   
         const res=await fetch('/sendmail', {
             method: 'POST',
             body:data,
             });
         const resdata=await res.json();
         console.log(resdata);
         document.querySelector('.msgpending').style.display='none';
        
         window.location.href='/allcampaigns';
}
promptform=document.getElementById('promptform');
promptform.addEventListener("submit",(e)=>
{   e.preventDefault();
    promptinput=new FormData(promptform);
    sendprompt(promptinput);
});
   
async function sendprompt(promptinput){
 
  document.getElementsByClassName('typewriter')[0].style.display='block';
   const res=await fetch('/promptendp',{
    method:'POST',
    body:promptinput
   });
   const resdata=await res.json();
   document.getElementsByClassName('typewriter')[0].style.display='none';
  
   writeanimation(resdata.email);

}
function writeanimation(text){
     let message=document.getElementById('message');
      let charIndex = 0;
      const typingInterval = setInterval(() => {
        if (charIndex < text.length) {
          message.value += text.charAt(charIndex);
          charIndex++;
        }
        else {
            clearInterval(typingInterval);}
      }, 30);
}
  


document.querySelector('.attach_link_wrapper').addEventListener('click',()=>{
  document.getElementById('attach_link').style.display='block';
  document.getElementById('buttonname').style.display='block';
})
document.querySelector('.attach_poster_wrapper').addEventListener('click',()=>{
  document.getElementById('poster_link').style.display='block';

})
document.querySelector('.attach_file_wrapper').addEventListener('click',()=>{
  document.getElementById('attach_file_name').style.display='block';

})