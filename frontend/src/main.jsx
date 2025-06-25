import { StytchB2BProvider } from '@stytch/react/b2b';
import { StytchB2BUIClient } from '@stytch/vanilla-js/b2b';
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.jsx";

// optional object for configuring SDK cookie behavior, currently showing defaults
const stytchOptions = {
  cookieOptions: {
    opaqueTokenCookieName: "stytch_session",
    jwtCookieName: "stytch_session_jwt",
    path: "",
    availableToSubdomains: false,
    domain: "",
  }
}

const stytch = new StytchB2BUIClient(
  import.meta.env.STYTCH_PUBLIC_TOKEN, // or process.env.STYTCH_PUBLIC_TOKEN for non-Vite based projects
  stytchOptions
);

const root = ReactDOM.createRoot(document.getElementById("root"));

root.render(
  <React.StrictMode>
    <StytchB2BProvider stytch={stytch}>
      <App />
    </StytchB2BProvider>
  </React.StrictMode>
);
