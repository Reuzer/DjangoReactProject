import { RouteObject } from "react-router";
import HomePage from "../pages/homePage/HomePage";
import Reports from "../pages/reports/Reports";

export const routesConfig: RouteObject[] = [
    {
        path: '/',
        element: <HomePage />
    },
    {
        path: '/reports',
        element: <Reports />
    }
]