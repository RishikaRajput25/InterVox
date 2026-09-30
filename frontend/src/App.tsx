import { RouterProvider } from "react-router-dom";

import { router } from "./app/router";
import AppProviders from "./app/providers";

function App() {
  return (
    <AppProviders>
      <RouterProvider router={router} />
    </AppProviders>
  );
}

export default App;