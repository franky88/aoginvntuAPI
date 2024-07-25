import { Link } from "react-router-dom";
import { ItemProp } from "../types/global";

function ItemCard({ item }: ItemProp) {
  return (
    <div
      className="bg-white shadow-[0_4px_12px_-5px_rgba(0,0,0,0.4)] w-full max-w-sm rounded-lg overflow-hidden mx-auto font-[sans-serif] mt-4">
      <div className="min-h-[256px]">
        <img src="https://readymadeui.com/Imagination.webp" className="w-full" />
      </div>

      <div className="p-6">
        <h3 className="text-gray-800 text-xl font-bold">{item.name}</h3>
        <p className="mt-4 text-sm text-gray-500 leading-relaxed">
            {item.model}
        </p>
        <Link to={`/items/${item.id}`}
          className="mt-6 px-5 py-2.5 rounded-lg text-white text-sm tracking-wider border-none outline-none bg-blue-600 hover:bg-blue-700 active:bg-blue-600">
            View
        </Link>
      </div>
    </div>
  )
}

export default ItemCard