import Sidebar from "../../components/Sidebar"
import ItemDetails from "../../components/ItemDetails"
import Breadcrumbs from "../../components/breadcrumbs/Breadcrumbs";
import BreadcrumbLink from "../../components/UI/BreadcrumbLink";
import BreadcrumbEnd from "../../components/UI/BreadcrumbEnd";
import EvenOdd from "../../components/UI/EvenOdd";

function ItemDetailsPage() {
  return (
    <>
        <div className="container-fluid">
            <Sidebar/>
            <main className=" ml-72 mr-72 mt-10">
                <h1 className=" text-3xl">Item Details</h1>
                <br />
                <Breadcrumbs>
                  <BreadcrumbLink link="/" name="Dashboard"/>
                  <EvenOdd />
                  <BreadcrumbLink link="/items" name="Items" />
                  <EvenOdd />
                  <BreadcrumbEnd name="Item details" />
                </Breadcrumbs>
                <ItemDetails/>
            </main>
        </div>
    </>
  )
}

export default ItemDetailsPage