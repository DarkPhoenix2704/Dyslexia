import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.tsx";
import "./index.css";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { VoiceIdentification } from "./routes/VoiceIdentification.tsx";
import { ImageRecognition } from "./routes/ImageRecognition.tsx";

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
  },
  {
    path: "/voice",
    element: <VoiceIdentification />,
  },
  {
    path: "/image",
    element: <ImageRecognition />,
  },
]);

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);
