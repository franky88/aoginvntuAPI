import Sidebar from "../components/Sidebar"
import Breadcrumbs from "../components/breadcrumbs/Breadcrumbs"
import BreadcrumbLink from "../components/UI/BreadcrumbLink"
import { jwtDecode } from "jwt-decode"
import { useAuth } from "../hooks/AuthProvider"

function Dashboard() {
  const { token } = useAuth()
  const decoded = jwtDecode(token)

  console.log(decoded.exp)
  return (
    <> 
        <div className="container-fluid">
            <Sidebar/>
            <main className=" ml-72 mr-72 mt-10">
                <h1 className=" text-3xl flex items-center">Dashboard</h1>
                <br />
                <Breadcrumbs>
                  <BreadcrumbLink link="/" name="Dashboard"></BreadcrumbLink>
                </Breadcrumbs>
            </main>
        </div>
    </>
  )
}

export default Dashboard