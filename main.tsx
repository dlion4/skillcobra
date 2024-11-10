import { createRoot } from "react-dom/client";
import React from "react";
import { App } from "./src/App";
import { hot } from 'react-hot-loader/root';  // Import HMR functionality


// Wrap your component with hot() to enable HMR

const container = document.getElementById("app");
if (container) {
  const root = createRoot(container);
    root.render(
      <React.StrictMode>
        <App id="app"  />
      </React.StrictMode>
    );
}
