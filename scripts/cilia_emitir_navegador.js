/* CILIA - Emissao pelo navegador (cole no Console do Chrome, LOGADO no Cilia)
   Uso:  emitirCilia(20, '01/06/2026','28/06/2026','RIO GRANDE DO NORTE')
   - Enumera (status=analyzed, SEM o filtro de conclusao na query -> evita timeout),
     filtra os 6 tipos de conclusao no cliente, baixa report.pdf (concorrencia 2 + backoff),
     monta 1 zip (store+crc32) e baixa. Acompanhe em window.__job.
   IDs dos estados:
     AC1 AL2 AP3 AM4 BA5 CE6 DF7 ES8 GO9 MA10 MT11 MS12 MG13 PA14 PB15
     PR16 PE17 PI18 RJ19 RN20 RS21 RO22 RR23 SC24 SP25 SE26 TO27 */
(function(){
  const T=(function(){let c,t=[];for(let n=0;n<256;n++){c=n;for(let k=0;k<8;k++)c=c&1?(0xEDB88320^(c>>>1)):(c>>>1);t[n]=c>>>0;}return t;})();
  const crc32=b=>{let c=0xFFFFFFFF;for(let i=0;i<b.length;i++)c=T[(c^b[i])&0xFF]^(c>>>8);return (c^0xFFFFFFFF)>>>0;};
  const mkUrl=(s,a,e,p)=>{const q=new URLSearchParams();q.set('page',String(p));q.set('search_filters[date_type]','scheduling');q.set('search_filters[date_range][start_date]',a);q.set('search_filters[date_range][end_date]',e);q.set('search_filters[order_option]','scheduling_older');q.append('search_filters[state_id][]',String(s));q.append('search_filters[status_ids][]','analyzed');return 'https://sistema.cilia.com.br/api/surveys/search.json?'+q.toString();};
  const conclOK=t=>{t=(t||'').normalize('NFKC').toUpperCase().trim();return t.startsWith('AUTORIZADO')||t.includes('FINALIZAÇÃO AUTOMÁTICA')||t==='SUPERVISÃO';};
  window.emitirCilia=function(stateId,start,end,label){
    const sleep=ms=>new Promise(r=>setTimeout(r,ms));
    const J={label,phase:'enum',page:0,kept:0,total:0,dl:0,fail:0,zipMB:0,done:false,err:null,fails:[]};window.__job=J;
    (async()=>{try{
      const seen=new Set(),list=[];let page=1,empty=0,g=0;
      while(g++<800){let r;try{r=await fetch(mkUrl(stateId,start,end,page),{headers:{'Accept':'application/json','X-Requested-With':'XMLHttpRequest'},credentials:'include'});}catch(e){await sleep(800);continue;}
        if(r.status===429){await sleep(2000);continue;} if(!r.ok){J.err='enum '+r.status;return;}
        const arr=await r.json(),real=Array.isArray(arr)?arr.filter(x=>x&&x.surveyable_id):[];
        if(!real.length){empty++;if(empty>=3)break;page++;continue;}empty=0;
        for(const it of real){if(seen.has(it.surveyable_id))continue;seen.add(it.surveyable_id);const ib=it.insurer_budget||{};if(!conclOK(ib.current_conclusion_title))continue;list.push({sid:it.surveyable_id,num:ib.number_with_version||String(it.surveyable_id)});}
        J.page=page;J.kept=list.length;page++;await sleep(110);}
      J.total=list.length;J.phase='download';
      const pdfs={};let idx=0;
      const worker=async()=>{while(idx<list.length){const it=list[idx++],name=it.num;let ok=false;
        for(let a=0;a<8&&!ok;a++){try{const rr=await fetch('https://sistema.cilia.com.br/budgets/'+it.sid+'/report.pdf',{credentials:'include'});
          if(rr.status===429){await sleep(1500*(a+1));continue;}if(!rr.ok)throw 0;const buf=new Uint8Array(await rr.arrayBuffer());
          if(String.fromCharCode(buf[0],buf[1],buf[2],buf[3])!=='%PDF'||buf.length<20000)throw 0;pdfs[name]=buf;ok=true;J.dl++;}catch(e){if(a===7){J.fail++;J.fails.push(name);}else await sleep(800);}}
        await sleep(280);}};
      await Promise.all([worker(),worker()]);
      J.phase='zip';const enc=new TextEncoder(),u16=v=>new Uint8Array([v&255,(v>>8)&255]),u32=v=>new Uint8Array([v&255,(v>>8)&255,(v>>16)&255,(v>>>24)&255]);
      const parts=[],cen=[];let off=0,cnt=0;
      for(const name of Object.keys(pdfs).sort()){const d=pdfs[name],fn=enc.encode(name+'.pdf'),c=crc32(d);
        [u32(0x04034b50),u16(20),u16(0),u16(0),u16(0),u16(0),u32(c),u32(d.length),u32(d.length),u16(fn.length),u16(0),fn].forEach(x=>parts.push(x));parts.push(d);
        cen.push(u32(0x02014b50),u16(20),u16(20),u16(0),u16(0),u16(0),u16(0),u32(c),u32(d.length),u32(d.length),u16(fn.length),u16(0),u16(0),u16(0),u16(0),u32(0),u32(off),fn);off+=30+fn.length+d.length;cnt++;}
      let cd=0;cen.forEach(p=>cd+=p.length);const eo=[u32(0x06054b50),u16(0),u16(0),u16(cnt),u16(cnt),u32(cd),u32(off),u16(0)];
      const blob=new Blob(parts.concat(cen,eo),{type:'application/zip'});J.zipMB=Math.round(blob.size/1048576*10)/10;J.zipCount=cnt;
      const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=label+' '+start.replace(/\//g,'.')+' - '+end.replace(/\//g,'.')+' (bruto).zip';document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(a.href),180000);
      J.phase='done';J.done=true;
    }catch(e){J.err=String(e);}})();
    return 'emitindo '+label+' - acompanhe window.__job';
  };
  console.log('Pronto. Ex.: emitirCilia(20,"01/06/2026","28/06/2026","RIO GRANDE DO NORTE")');
})();
