function md(text){return text.replace(/```(.*?)```/gs,"<pre>$1</pre>").replace(/\*\*(.*?)\*\*/g,"<b>$1</b>").replace(/\*(.*?)\*/g,"<i>$1</i>").replace(/\n/g,"<br>");}
const chat=document.getElementById("chat");
const input=document.getElementById("msg");
function add(text,type){const d=document.createElement("div");d.className="msg "+type;d.innerHTML=md(text);chat.appendChild(d);chat.scrollTop=chat.scrollHeight;}
async function send(){const message=input.value.trim();if(!message)return;add(message,"user");input.value="";add("⏳ جاري التفكير…","bot");const res=await fetch("/api/chat",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({message})});const data=await res.json();chat.removeChild(chat.lastChild);add(data.message,"bot");}
input.onkeydown=e=>{if(e.key==="Enter"&&!e.shiftKey){e.preventDefault();send();}};
function toggleMode(){document.body.classList.toggle("dark");}
