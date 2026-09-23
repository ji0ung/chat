const conversations=[
 {id:"conv_8F21",user:"usr_5a02…",character:"루나",persona:"Persona v3",policy:"Balanced v2",messages:184,last:"방금",status:"활성"},
 {id:"conv_3A90",user:"usr_91bc…",character:"루나",persona:"Persona v3",policy:"Balanced v2",messages:76,last:"4분 전",status:"활성"},
 {id:"conv_C114",user:"usr_2d77…",character:"하루",persona:"Persona v2",policy:"Conservative v1",messages:312,last:"18분 전",status:"점검"},
 {id:"conv_9D42",user:"usr_104e…",character:"루나",persona:"Persona v2",policy:"Balanced v2",messages:48,last:"31분 전",status:"활성"},
 {id:"conv_B701",user:"usr_a81f…",character:"모아",persona:"Persona v1",policy:"Active v1",messages:129,last:"1시간 전",status:"활성"}
];
const characters=[
 {name:"루나",initial:"L",desc:"다정하고 장난스러운 오래된 친구",persona:"Persona v3",policy:"Balanced v2",chats:"842",success:"91.2%"},
 {name:"하루",initial:"H",desc:"차분하게 일상을 정리하는 동료",persona:"Persona v2",policy:"Conservative v1",chats:"286",success:"84.6%"},
 {name:"모아",initial:"M",desc:"적극적으로 추억을 꺼내는 여행 친구",persona:"Persona v1",policy:"Active v1",chats:"156",success:"79.8%"}
];
const memoryResults=[
 {text:"나는 민트초코 아이스크림을 제일 좋아해.",score:.82},
 {text:"초콜릿보다 상쾌한 맛이 좋다고 했어.",score:.58},
 {text:"부산에서 같이 젤라또를 먹었던 이야기",score:.43}
];
const logs=[
 ["memory_recalled","req_73ac…","루나 · 결과 5개 · 최고 점수 0.82","42ms"],
 ["chat_completed","req_73ac…","응답 생성 완료 · 기억 5개 사용","1.8s"],
 ["memory_recalled","req_18df…","하루 · 결과 2개 · 최고 점수 0.64","38ms"],
 ["http_request_failed","req_b021…","OpenAI 요청 시간 초과 · 재시도 예정","10.0s"],
 ["memory_recalled","req_a99c…","모아 · 임계값 미달 · 결과 없음","31ms"]
];
const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
const apiBase=()=>localStorage.getItem("luna_api_url")||"https://chat-7bf4.onrender.com";
function toast(text){const el=$("#toast");el.textContent=text;el.classList.add("show");setTimeout(()=>el.classList.remove("show"),2200)}
function status(value){return `<span class="status ${value==="점검"?"warn":""}">${value}</span>`}
function renderRows(items,target,compact=false){$(target).innerHTML=items.map(c=>compact?`<tr><td class="id">${c.id}</td><td>${c.character}</td><td class="persona">${c.persona}</td><td>${c.policy}</td><td>${c.last}</td><td>${status(c.status)}</td></tr>`:`<tr><td class="id">${c.id}</td><td>${c.user}</td><td>${c.character}</td><td class="persona">${c.persona}</td><td>${c.policy}</td><td>${c.messages}</td><td>${status(c.status)}</td></tr>`).join("")}
renderRows(conversations.slice(0,4),"#recentConversationRows",true);renderRows(conversations,"#conversationRows");
$("#characterGrid").innerHTML=characters.map(c=>`<article class="character-card"><div class="character-top"><span class="character-avatar">${c.initial}</span><div><h3>${c.name}</h3><small>${c.desc}</small></div></div><div class="character-stats"><div><span>활성 채팅</span><strong>${c.chats}</strong></div><div><span>검색 성공률</span><strong>${c.success}</strong></div></div><div class="card-binding"><span>현재 연결</span><strong>${c.persona}</strong> · ${c.policy}</div></article>`).join("");
$("#logList").innerHTML=logs.map(l=>`<div class="log-row"><div><span class="event">${l[0]}</span></div><span class="request">${l[1]}</span><span class="log-summary">${l[2]}</span><span class="duration">${l[3]}</span></div>`).join("");

function relativeTime(value){const seconds=Math.max(0,(Date.now()-new Date(value).getTime())/1000);if(seconds<60)return "방금";if(seconds<3600)return `${Math.floor(seconds/60)}분 전`;if(seconds<86400)return `${Math.floor(seconds/3600)}시간 전`;return `${Math.floor(seconds/86400)}일 전`}
async function loadOverview(){
  $(".last-sync").textContent="동기화 중…";
  try{
    const response=await fetch(`${apiBase()}/admin/overview`);
    if(!response.ok)throw new Error(`요청 실패 (${response.status})`);
    const data=await response.json();
    $("#metricConversations").textContent=data.conversation_count.toLocaleString();
    $("#metricMemories").textContent=data.memory_count.toLocaleString();
    $("#metricUsers").textContent=data.user_count.toLocaleString();
    $("#metricEvaluation").textContent=data.evaluation_average===null?"-":`${data.evaluation_average.toFixed(1)}`;
    $("#metricEvaluationCount").textContent=`${data.evaluation_count}건`;
    const live=(data.conversations||[]).map(c=>({id:c.conversation_id.slice(0,12),user:`${c.user_id.slice(0,8)}…`,character:"루나",persona:"현재 프롬프트",policy:"Memory MVP",messages:c.messages,last:relativeTime(c.last_activity),status:"활성"}));
    renderRows(live.slice(0,4),"#recentConversationRows",true);renderRows(live,"#conversationRows");
    $(".last-sync").textContent="마지막 동기화 · 방금";
  }catch(error){$(".last-sync").textContent="동기화 실패";toast(`운영 데이터 로드 실패: ${error.message}`)}
}
const titles={overview:"운영 현황",characters:"캐릭터",conversations:"연결된 채팅",policy:"기억 감도",logs:"검색 로그"};
function showView(name){$$('.nav-item').forEach(b=>b.classList.toggle('active',b.dataset.view===name));$$('.view').forEach(v=>v.classList.toggle('active',v.id===`view-${name}`));$("#pageTitle").textContent=titles[name];history.replaceState(null,"",`#${name}`)}
$$('.nav-item').forEach(b=>b.addEventListener('click',()=>showView(b.dataset.view)));$$('[data-jump]').forEach(b=>b.addEventListener('click',()=>showView(b.dataset.jump)));
const threshold=$("#threshold"),topK=$("#topK"),weights=$$('.weight');
function updateControls(){$("#thresholdOutput").textContent=Number(threshold.value).toFixed(2);$("#topKOutput").textContent=`${topK.value}개`;let total=0;weights.forEach(w=>{w.nextElementSibling.textContent=`${w.value}%`;total+=Number(w.value)});const totalEl=$("#weightTotal");totalEl.textContent=`${total}%`;totalEl.style.color=total===100?"#27a77a":"#df6875"}
threshold.addEventListener('input',updateControls);topK.addEventListener('input',updateControls);weights.forEach(w=>w.addEventListener('input',updateControls));
const presets={conservative:{threshold:.48,topK:3,w:[78,14,6,2]},balanced:{threshold:.35,topK:5,w:[70,15,10,5]},active:{threshold:.24,topK:8,w:[58,17,17,8]}};
$$('[data-preset]').forEach(b=>b.addEventListener('click',()=>{const p=presets[b.dataset.preset];$$('[data-preset]').forEach(x=>x.classList.toggle('active',x===b));threshold.value=p.threshold;topK.value=p.topK;weights.forEach((w,i)=>w.value=p.w[i]);updateControls();renderExperiment()}));
function resultCard(item,i,changed=false){return `<div class="result-card ${changed?'changed':''}"><div class="result-top"><strong>#${i+1}</strong><span>${Math.round(item.score*100)}점</span></div><p>${item.text}</p><div class="mini-bar"><i style="width:${item.score*100}%"></i></div></div>`}
function renderExperiment(){const sensitivity=1-Number(threshold.value),limit=Number(topK.value);const exp=memoryResults.map((x,i)=>({...x,score:Math.min(.98,x.score+(sensitivity-.65)*.23+(limit-5)*.012-i*.004)})).filter(x=>x.score>=Number(threshold.value)).slice(0,limit);$("#currentResults").innerHTML=memoryResults.map((x,i)=>resultCard(x,i)).join('');$("#experimentResults").innerHTML=exp.map((x,i)=>resultCard(x,i,Math.abs(x.score-memoryResults[i]?.score)>.01)).join('')||'<div class="result-card"><p>임계값을 넘은 기억이 없습니다.</p></div>';const delta=exp.length-memoryResults.length;$("#impactText").textContent=delta===0?`검색 결과 수는 같고, 최소 유사도 ${Number(threshold.value).toFixed(2)} 기준으로 순위를 다시 계산했습니다.`:`현재보다 기억을 ${Math.abs(delta)}개 ${delta>0?'더 사용':'덜 사용'}할 것으로 예상됩니다.`}
renderExperiment();
$("#runSimulation").addEventListener('click',()=>{renderExperiment();toast('실험 정책으로 다시 계산했습니다')});$("#queryRun").addEventListener('click',()=>{renderExperiment();toast('테스트 메시지를 분석했습니다')});
$("#conversationSearch").addEventListener('input',e=>{const q=e.target.value.toLowerCase();renderRows(conversations.filter(c=>Object.values(c).some(v=>String(v).toLowerCase().includes(q))),"#conversationRows")});
$("#newPersonaButton").addEventListener('click',()=>$("#personaDialog").showModal());$("#saveDraft").addEventListener('click',()=>setTimeout(()=>toast('페르소나 초안을 저장했습니다'),0));
$("#refreshButton").addEventListener('click',()=>loadOverview());$("#publishButton").addEventListener('click',()=>toast('설정 발행 기능은 다음 단계에서 연결됩니다'));
const hash=location.hash.slice(1);if(titles[hash])showView(hash);
loadOverview();
