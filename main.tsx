import { createRoot } from "react-dom/client";
import React from "react";
import { App } from "./src/App";


// Wrap your component with hot() to enable HMR

const container = document.getElementById("app");
console.log(container);
if (container) {
  const root = createRoot(container);
    root.render(
      <React.StrictMode>
        <App id="app" />
      </React.StrictMode>
    );
}
