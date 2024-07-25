import { useEffect, useState } from "react"
import ItemCard from "./ItemCard"
import api from "../utils/api"
import { Item } from "../types/global"
import TableDataUI from "./UI/TableDataUI"


function ItemList() {
    const [items, setItems] = useState<Item[]>([])
    const [error, setError] = useState<string | null>(null);
    const [totalItem, setTotalItem] = useState<number | null>(null)
    useEffect(()=> {
        const getItems = async () => {
            try {
                const response = await api.get('units/');
                if (Array.isArray(response.data.results)) {
                    const data = response.data.results
                    setItems(data);
                    setTotalItem(response.data)
                    console.log(response)
                } else {
                  console.error("Unexpected response format:", response.data.results);
                }
            } catch (error) {
                setError("Error fetching items: " + error.message);
                console.error("Error fetching items:", error)
            }
        }
        getItems()
    }, [])

  return (
    <>  
        <h1 className=" text-3xl">TOTAL Items {(totalItem) ? totalItem.count : ("")}</h1>
        <div className="font-sans flex flex-wrap overflow-x-auto mt-5">
            {error && <div className="text-red-500">{error}</div>}
            
            {items.map(item => (
                // <ItemCard key={item.id} item={item}></ItemCard>
                <TableDataUI key={item.id} item={item}/>
            ))}
        </div>
    </>
    
  )
}

export default ItemList