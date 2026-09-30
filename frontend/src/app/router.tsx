import { createBrowserRouter } from "react-router-dom";
import Dashboard from "../pages/Dashboard";
import Documents from "../pages/Documents";


export const router = createBrowserRouter([
  {
    path: "/",
    element: <Dashboard />,
  },
  {
    path: "/documents",
    element: <Documents />,
  },
]);