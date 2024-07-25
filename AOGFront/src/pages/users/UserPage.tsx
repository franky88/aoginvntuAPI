import Sidebar from "../../components/Sidebar"
import UserList from "../../components/UserList"
import Breadcrumbs from "../../components/breadcrumbs/Breadcrumbs";
import BreadcrumbLink from "../../components/UI/BreadcrumbLink";
import EvenOdd from "../../components/UI/EvenOdd";

function UserPage() {
  return (
    <> 
        <div className="container-fluid">
            <Sidebar/>
            <main className=" ml-72 mr-72 mt-10">
                <h1 className=" text-3xl">Employees</h1>
                <br />
                <Breadcrumbs>
                    <BreadcrumbLink link="/" name="Dashboard"></BreadcrumbLink>
                    <EvenOdd></EvenOdd>
                    <BreadcrumbLink link="/users" name="Employees"></BreadcrumbLink>
                </Breadcrumbs>
                <UserList/>
            </main>
        </div>
    </>
  )
}

export default UserPage