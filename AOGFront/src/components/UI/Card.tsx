import { Item } from "../../types/global"


function Card({name, date_purchased, model, cost, serials, created, updated}: Item) {
    
    return (
    <>
        <div className="bg-white grid sm:grid-cols-2 items-center shadow-[0_4px_12px_-5px_rgba(0,0,0,0.4)] w-full max-w-2xl max-sm:max-w-sm rounded-lg font-[sans-serif] overflow-hidden mt-4">
            <div className="p-6">
                <h3 className="text-xl font-semibold">{name}</h3>
                <p className="mt-3 text-sm text-gray-500 leading-relaxed">
                    <strong>Date purchased: </strong> <span>{date_purchased}</span>
                    <br />
                    <strong>Model: </strong> <span>{model}</span>
                    <br />
                    <strong>Cost: </strong> <span>{cost}</span>
                    <br />
                    <strong>Serial: </strong> <span>{serials}</span>
                    <br />
                    <strong>Created: </strong> <span>{created}</span>
                    <br />
                    <strong>Updated: </strong> <span>{updated}</span>
                </p>
            </div>
        </div>
    </>
  )
}

export default Card