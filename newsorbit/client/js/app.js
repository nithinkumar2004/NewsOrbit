const API_BASE = localStorage.getItem('apiBase') || 'http://localhost:10000';
const firebaseConfig = {
  apiKey: "YOUR_FIREBASE_API_KEY",
  authDomain: "YOUR_PROJECT.firebaseapp.com",
  projectId: "YOUR_PROJECT_ID",
  appId: "YOUR_APP_ID",
};
firebase.initializeApp(firebaseConfig);

const toastEl = document.getElementById('appToast');
const toastBody = document.getElementById('toastBody');
const toast = toastEl ? new bootstrap.Toast(toastEl) : null;

function showToast(message){if(toastBody){toastBody.textContent=message;toast.show();}}
function token(){return localStorage.getItem('token');}
function authHeader(){return {Authorization:`Bearer ${token()}`};}
function toggleDarkMode(){document.body.classList.toggle('light');localStorage.setItem('light',document.body.classList.contains('light'));}
if(localStorage.getItem('light')==='true') document.body.classList.add('light');

async function firebaseGoogleLogin(){
  const provider=new firebase.auth.GoogleAuthProvider();
  const result=await firebase.auth().signInWithPopup(provider);
  const idToken=await result.user.getIdToken();
  return backendLogin(idToken);
}

async function firebasePhoneLogin(phoneNumber, appVerifier){
  const confirmation = await firebase.auth().signInWithPhoneNumber(phoneNumber, appVerifier);
  return confirmation;
}

async function backendLogin(idToken){
  const res=await axios.post(`${API_BASE}/auth/firebase-login`,{idToken});
  localStorage.setItem('token',res.data.access_token);
  localStorage.setItem('user',JSON.stringify(res.data.user));
  showToast('Login success');
  return res.data;
}
