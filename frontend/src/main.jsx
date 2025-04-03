//import { StrictMode } from 'react'
import React from 'react';
import { createRoot } from 'react-dom/client';
import './index.css'
import App from './App.jsx'
import LoginPage from './components/login.jsx';


const container = document.getElementById('root');
const root = createRoot(container);
root.render(<LoginPage/>);
/*ReactDOM.render(<App/>, document.getElementById('root'))
.render(
  <StrictMode>
    <App />
  </StrictMode>,
)
*/