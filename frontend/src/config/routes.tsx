import { RouteObject } from "react-router";
import HomePage from "../pages/homePage/HomePage";
import Reports from "../pages/reports/Reports";
import Report from "../pages/report/Report";
import PostReport from "../pages/post_report/PostReport";

export const routesConfig: RouteObject[] = [
    {
        path: '/',
        element: <HomePage />
    },
    {
        path: '/reports',
        element: <Reports />
    },
    {
        path: '/reports/:id',
        element: <Report />
    },
    {
        path: '/post/reports',
        element: <PostReport />
    }
]