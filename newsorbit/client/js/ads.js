async function createCampaign(e){
  e.preventDefault();
  const payload={
    title:adTitle.value,
    image:adImage.value,
    country:adCountry.value,
    category:adCategory.value,
    budget:Number(adBudget.value),
  };
  try{
    await axios.post(`${API_BASE}/ads`,payload,{headers:authHeader()});
    showToast('Campaign created');
    loadMyAds();
  }catch(err){showToast(err.response?.data?.detail||'Failed to create ad');}
}

async function loadMyAds(){
  const table=document.getElementById('adRows');
  const analytics=document.getElementById('analytics');
  const res=await axios.get(`${API_BASE}/ads/mine`,{headers:authHeader()});
  table.innerHTML=res.data.map(a=>`<tr><td>${a.title}</td><td>${a.country}</td><td>${a.category}</td><td>${a.budget}</td><td>${a.spent||0}</td><td>${a.impressions}</td><td>${a.clicks}</td><td>${a.status}</td></tr>`).join('');
  const stats=await axios.get(`${API_BASE}/ads/analytics`,{headers:authHeader()});
  analytics.textContent=`Campaigns: ${stats.data.campaigns} | Impressions: ${stats.data.totalImpressions} | Clicks: ${stats.data.totalClicks} | Revenue: $${Number(stats.data.revenue||0).toFixed(2)}`;
}
