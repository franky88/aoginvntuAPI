import { createBrowserRouter } from "react-router-dom"
import Dashboard from "../pages/Dashboard"
import ItemPage from "../pages/items/ItemPage"
import ItemDetailsPage from "../pages/items/ItemDetailsPage"
import UserPage from "../pages/users/UserPage"
import ItemKitPage from "../pages/itemkits/ItemKitPage"
import LoginPage from "../pages/login/LoginPage"
import ProtectedRoute from "../components/ProtectedRoute"

const router = createBrowserRouter([
    {
        path: '/',
        element: <ProtectedRoute><Dashboard/></ProtectedRoute>
    },
    {
        path: '/login',
        element: <LoginPage/>
    },
    {
        path: '/item-kits',
        element: <ProtectedRoute><ItemKitPage/></ProtectedRoute>
    },
    {
        path: '/items',
        element: <ProtectedRoute><ItemPage/></ProtectedRoute>
    },
    {
        path: '/items/:itemID',
        element: <ProtectedRoute><ItemDetailsPage/></ProtectedRoute>
    },
    {
        path: '/users',
        element: <ProtectedRoute><UserPage/></ProtectedRoute>
    },
])

export default router