import { RouteObject } from "react-router";
import HomePage from "../pages/homePage/HomePage";
import Reports from "../pages/reports/Reports";
import Report from "../pages/report/Report";
import PostReport from "../pages/post_report/PostReport";
import Blogs from "../pages/blogs/Blogs";
import Login from "../pages/login/Login";
import Profile from "../pages/profile/Profile";
import Register from "../pages/register/Register";

export const routesConfig: RouteObject[] = [
    {
        path: '',
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
    },
    {
        path: '/blogs',
        element: <Blogs />
    },
    {
        path: '/login',
        element: <Login />
    },
    {
        path: '/profile',
        element: <Profile />
    },
    {
        path: '/register',
        element: <Register />
    }
]