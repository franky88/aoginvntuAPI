import { useEffect, useState, ChangeEvent, FormEvent } from "react";
import { useParams } from "react-router-dom";
import api from "../utils/api";
import Card from "./UI/Card";
import { Item } from "../types/global";

interface Params {
    itemID: string;
}

function ItemDetails() {
    const { itemID } = useParams<Params>();
    const [item, setItem] = useState<Item | null>(null);
    const [itemHistory, setItemHistory] = useState(null);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);
    const [isEditing, setIsEditing] = useState<boolean>(false);
    const [formData, setFormData] = useState<Item | null>(null);

    useEffect(() => {
        if (itemID) {
            fetchItem(Number(itemID));
        }
    }, [itemID]);

    const fetchItem = async (itemID: number) => {
        try {
            const response = await api.get(`units/${itemID}/`);
            setItem(response.data);
            setFormData(response.data); // Initialize form data with fetched data
            console.log(response.data.history)
            setItemHistory(response.data.history)
        } catch (err) {
            setError("Error fetching item data");
        } finally {
            setLoading(false);
        }
    };

    const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setFormData((prevFormData) => prevFormData ? { ...prevFormData, [name]: value } : null);
    };

    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault();
        if (formData && itemID) {
            try {
                await api.put(`units/${itemID}/`, formData);
                setItem(formData); // Update the displayed item with new data
                setIsEditing(false); // Switch back to view mode
            } catch (err) {
                setError("Error updating item data");
            }
        }
    };

    if (loading) return <p>Loading...</p>;
    if (error) return <p>{error}</p>;

    return (
        <>
            {item ? (
                isEditing ? (
                    <form onSubmit={handleSubmit} className="space-y-4 font-[sans-serif] max-w-md float-start">
                        <div className="relative flex items-center">
                        <label className="text-[13px] bg-white text-black absolute px-2 top-[-10px] left-[18px]">Name</label>
                        <input
                            type="text"
                            name="name"
                            placeholder="Name"
                            className="px-4 py-3.5 bg-white text-black w-full text-sm border-2 border-gray-100 focus:border-blue-500 rounded outline-none"
                            value={formData?.name || ''}
                            onChange={handleInputChange}
                            required
                        />
                        </div>

                        <div className="relative flex items-center">
                        <label className="text-[13px] bg-white text-black absolute px-2 top-[-10px] left-[18px]">Model</label>
                        <input
                            type="text"
                            name="name"
                            placeholder="Model"
                            className="px-4 py-3.5 bg-white text-black w-full text-sm border-2 border-gray-100 focus:border-blue-500 rounded outline-none"
                            value={formData?.model || ''}
                            onChange={handleInputChange}
                            required
                        />
                        </div>
                        
                        {/* <input
                            type="text"
                            name="model"
                            placeholder="Model"
                            className="px-4 py-3 bg-gray-100 w-full text-sm outline-none border-b-2 border-blue-500 rounded"
                            value={formData?.model || ''}
                            onChange={handleInputChange}
                            required
                        /> */}
                        <input
                            type="date"
                            name="date_purchased"
                            placeholder="Date Purchased"
                            className="px-4 py-3 bg-gray-100 w-full text-sm outline-none border-b-2 border-blue-500 rounded"
                            value={formData?.date_purchased || ''}
                            onChange={handleInputChange}
                            required
                        />
                        <input
                            type="number"
                            name="cost"
                            placeholder="Cost"
                            className="px-4 py-3 bg-gray-100 w-full text-sm outline-none border-b-2 border-blue-500 rounded"
                            value={formData?.cost || 0}
                            onChange={handleInputChange}
                            required
                        />
                        <input
                            type="text"
                            name="serials"
                            placeholder="Serials"
                            className="px-4 py-3 bg-gray-100 w-full text-sm outline-none border-b-2 border-blue-500 rounded"
                            value={formData?.serials || ''}
                            onChange={handleInputChange}
                            required
                        />
                        <button
                            type="submit"
                            className="!mt-8 w-full px-4 py-2.5 mx-auto block text-sm bg-blue-500 text-white rounded hover:bg-blue-600"
                        >
                            Save
                        </button>
                        <button
                            type="button"
                            onClick={() => setIsEditing(false)}
                            className="mt-2 w-full px-4 py-2.5 mx-auto block text-sm bg-gray-500 text-white rounded hover:bg-gray-600"
                        >
                            Cancel
                        </button>
                    </form>
                ) : (
                    <>
                    <div className=" flex flex-row">
                        <div>
                            <Card
                                id={item.id}
                                name={item.name}
                                model={item.model}
                                date_purchased={item.date_purchased}
                                cost={item.cost}
                                serials={item.serials}
                                created={item.created}
                                updated={item.updated}
                            />
                            <button
                                onClick={() => setIsEditing(true)}
                                className="mt-8 px-4 py-2.5 mx-auto block text-sm bg-blue-500 text-white rounded hover:bg-blue-600 float-start"
                            >
                                Edit
                            </button>
                        </div>
                        <div className="ml-5">
                            <h1>Transaction history</h1>
                            {itemHistory.map((history) => (
                                <div>{history.changed_by} <br />
                                <span>{history.snapshot.name}</span></div>
                            ))}
                        </div>
                    </div>
                    </>
                )
            ) : (
                <p>No item data available</p>
            )}
        </>
    );
}

export default ItemDetails;
