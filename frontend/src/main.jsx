

import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

const rootElement = document.getElementById('root');

if (rootElement) {
  const root = ReactDOM.createRoot(rootElement);
  root.render(
    <React.StrictMode>
      <App />
    </React.StrictMode>
  );
} else {
  document.body.innerHTML = "<h2 style='color:white;text-align:center;'>❌ App failed to load. No #root element found.</h2>";
  console.error("❌ No root element found to mount React app.");
}
