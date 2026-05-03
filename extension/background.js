// Background service worker to make API calls to our Python backend
const BACKEND_BASE_URL = 'https://kawach-ey6v.onrender.com';

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "checkPhishing") {
    fetch(`${BACKEND_BASE_URL}/api/phishing/check`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ url: request.url })
    })
    .then(response => response.json())
    .then(data => sendResponse(data))
    .catch(error => {
      console.error('Error checking URL:', error);
      sendResponse({ risk_score: 0, status: "Error connecting to KAWACH Backend" });
    });
    
    return true; 
  }
  
  if (request.action === "savePassword") {
    fetch(`${BACKEND_BASE_URL}/api/vault`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(request.data)
    })
    .then(response => {
      if (!response.ok) {
        return response.json().then(data => {
          throw new Error(data.message || `HTTP ${response.status}`);
        });
      }
      return response.json();
    })
    .then(data => {
      console.log('Password save response:', data);
      sendResponse({
        status: data.status === 'Success' ? 'Success' : 'Error',
        message: data.message || data.status || 'Password saved'
      });
    })
    .catch(error => {
      console.error('Error saving password to vault:', error);
      sendResponse({
        status: 'Error',
        message: `Failed to save password: ${error.message}`
      });
    });
    
    return true;
  }
});
