// Background service worker to make API calls to our Python backend
const BACKEND_BASE_URL = 'https://kawach-ey6v.onrender.com';

async function confirmVaultSave(savedItem) {
  const response = await fetch(`${BACKEND_BASE_URL}/api/vault`);
  const data = await response.json();
  const vaultItems = Array.isArray(data.vault) ? data.vault : [];

  const matchedItem = vaultItems.find((item) => {
    return item.website === savedItem.website && item.username === savedItem.username && item.password === savedItem.password;
  });

  return {
    confirmed: Boolean(matchedItem),
    vault_size: vaultItems.length
  };
}

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
    .then(response => response.json())
    .then(async (data) => {
      if (data.status !== 'Success') {
        sendResponse({ status: 'Error', message: data.message || 'Vault save failed' });
        return;
      }

      const confirmation = await confirmVaultSave(request.data);
      sendResponse({
        status: confirmation.confirmed ? 'Success' : 'Warning',
        message: confirmation.confirmed
          ? `Saved to KAWACH Vault. Total entries: ${confirmation.vault_size}`
          : 'Password saved, but the vault list has not refreshed yet.',
        confirmed: confirmation.confirmed,
        vault_size: confirmation.vault_size
      });
    })
    .catch(error => {
      console.error('Error saving password:', error);
      sendResponse({ status: "Error", message: "Error connecting to KAWACH Backend" });
    });
    
    return true;
  }
});
