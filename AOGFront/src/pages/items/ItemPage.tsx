import Sidebar from "../../components/Sidebar"
import ItemList from "../../components/ItemList"
import Breadcrumbs from "../../components/breadcrumbs/Breadcrumbs";
import BreadcrumbLink from "../../components/UI/BreadcrumbLink";
import EvenOdd from "../../components/UI/EvenOdd";

function ItemPage() {
  return (
    <> 
        <div className="container-fluid">
            <Sidebar/>
            <main className=" ml-72 mt-10">
                <h1 className=" text-3xl flex items-center">
                  Items
                </h1>
                <br />
                <Breadcrumbs>
                    <BreadcrumbLink link="/" name="Dashboard"></BreadcrumbLink>
                    <EvenOdd></EvenOdd>
                    <BreadcrumbLink link="/items" name="Items"></BreadcrumbLink>
                </Breadcrumbs>
                <ItemList />
            </main>
        </div>
    </>
  )
}

export default ItemPage