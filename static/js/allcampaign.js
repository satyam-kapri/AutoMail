document.getElementById('create-new').addEventListener('click',()=>{
    window.location.href='/home';
})
let scheduledata = document.currentScript.getAttribute('scheduledata');
// console.log(scheduledata);
scheduledata=JSON.parse(scheduledata);
scheduledata.forEach(element => {
    let schedule=document.createElement('div');
    let name=document.createElement('span');
    let time=document.createElement('span');
    let status=document.createElement('span');
    let button=document.createElement('button');
    name.innerHTML=element.fields.campaign_name;
    let schtime=element.fields.scheduled_time;
    let temp= schtime.split("T");
    time.innerText=temp[0]+" "+temp[1].slice(0,-1);
    status.innerHTML=element.fields.status;
    button.innerHTML="Delete";
    schedule.appendChild(name);
    schedule.appendChild(time);
    schedule.appendChild(status);
    schedule.appendChild(button);
    schedule.classList.add('campaign');
    button.classList.add('campaign-delete');
    name.classList.add('campaign-name');
    time.classList.add('sch-time');
    let currstatus=element.fields.status;
    if(currstatus==="Completed")
    status.classList.add('status-complete');
    else if(currstatus==="Scheduled")
    status.classList.add('status-scheduled');
    else
    status.classList.add('status-failure');
    let content=document.querySelector('.table-contents');
    content.appendChild(schedule);
});
const buttons=document.getElementsByClassName('campaign-delete');
for (let i = 0; i < buttons.length; i++) {
    buttons[i].addEventListener('click', function() {
      const listItem = this.parentNode;
      const cname=listItem.firstChild.innerHTML;
      let data={'campaign_name':cname};
      data=JSON.stringify(data);
      listItem.parentNode.removeChild(listItem);

      fetch('/deletecampaign',{
        method: 'DELETE',
        headers:{'Content-Type':'application/json'},
        body:data,
        });
    });
  }