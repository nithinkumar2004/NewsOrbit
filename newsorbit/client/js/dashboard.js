async function loadNews(){
  const country=document.getElementById('country').value;
  const category=document.getElementById('category').value;
  const grid=document.getElementById('newsGrid');
  grid.innerHTML='<div class="skeleton col-12"></div><div class="skeleton col-12"></div>';
  try{
    await axios.post(`${API_BASE}/news/refresh`,{country,categories:[category]},{headers:authHeader()});
    const res=await axios.get(`${API_BASE}/news?country=${country}&category=${category}`,{headers:authHeader()});
    renderNewsWithAds(res.data.news,res.data.ads,grid,category);
  }catch(e){showToast(e.response?.data?.detail||'Failed to load news');}
}

function renderNewsWithAds(news,ads,grid,category){
  grid.innerHTML='';
  let adIndex=0;
  news.forEach((item,i)=>{
    if(i>0 && i%5===0 && ads[adIndex]){
      const ad=ads[adIndex++];
      const adCol=document.createElement('div');adCol.className='col-md-6 fade-in';
      adCol.innerHTML=`<div class="glass p-3"><small>Sponsored</small><h5>${ad.title}</h5><img src="${ad.image}" class="img-fluid rounded"/><button class="btn btn-sm btn-info mt-2" onclick="trackAd('${ad._id||ad.id}','click')">Visit</button></div>`;
      grid.appendChild(adCol);trackAd(ad._id||ad.id,'impression');
    }
    const sentimentClass=item.sentiment==='positive'?'bg-success':item.sentiment==='negative'?'bg-danger':'bg-secondary';
    const col=document.createElement('div');col.className='col-md-6 col-lg-4 fade-in';
    col.innerHTML=`<div class="glass p-3 news-card h-100"><span class="badge ${sentimentClass} sentiment-badge">${item.sentiment}</span><span class="badge bg-warning text-dark">Importance ${item.importance}</span><h5 class="mt-2">${item.rewrittenHeadline}</h5><p>${item.summary}</p><div>${item.tags.map(t=>`<span class='badge bg-dark me-1'>${t}</span>`).join('')}</div><a href="${item.originalUrl}" target="_blank" class="btn btn-sm btn-outline-light mt-2">Source</a></div>`;
    grid.appendChild(col);
  });
}

async function trackAd(adId,eventType){
  if(!adId) return;
  await axios.post(`${API_BASE}/ads/track`,{adId,eventType},{headers:authHeader()});
}
