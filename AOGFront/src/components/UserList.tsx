import { useEffect, useState } from "react";
import api from "../utils/api";
import TableDataUI from "./UI/TableDataUI";
import GoogleIcon from "./UI/GoogleIcon";
import { User } from "../types/global";


function UserList() {
  const [users, setUsers] = useState<User[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const response = await api.get("users/");
        const data = response.data.results;
        console.log("data response", data);
        setUsers(data);
      } catch (error) {
        setError("Error fetching users: " + error.message);
        console.error("Error fetching users:", error);
      }
    };

    fetchUsers();
  }, []);

  return (
    <div className="font-sans overflow-x-auto mt-5">
      {error && <div className="text-red-500">{error}</div>}
      <table className="min-w-full bg-white">
        <thead className="bg-gray-100 whitespace-nowrap">
          <tr>
            <TableDataUI cls_name="p-4 text-left text-xs font-semibold text-gray-800" content="Username" />
            <TableDataUI cls_name="p-4 text-left text-xs font-semibold text-gray-800" content="Full Name" />
            <TableDataUI cls_name="p-4 text-left text-xs font-semibold text-gray-800" content="Email" />
            <TableDataUI cls_name="p-4 text-left text-xs font-semibold text-gray-800" content="Is Staff" />
            <TableDataUI cls_name="p-4 text-left text-xs font-semibold text-gray-800" content="Actions" />
          </tr>
        </thead>
        <tbody className="whitespace-nowrap">
          {users.map((user) => (
            <tr key={user.id} className="hover:bg-gray-50">
              <TableDataUI cls_name="p-4 text-[15px] text-gray-800" content={user.username} />
              <TableDataUI cls_name="p-4 text-[15px] text-gray-800" content={user.get_full_name} />
              <TableDataUI cls_name="p-4 text-[15px] text-gray-800" content={user.email} />
              <TableDataUI cls_name="p-4 text-[15px] text-gray-800" content={user.is_staff ? "Yes" : "No"} />
              <td className="p-4">
                <button className="mr-4" title="Edit">
                  <GoogleIcon iconName="edit_square" clsName="w-[18px] h-[18px] mr-4 flex items-center text-blue-500" />
                </button>
                <button className="mr-4" title="Delete">
                  <GoogleIcon iconName="delete" clsName="w-[18px] h-[18px] mr-4 flex items-center text-red-500" />
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default UserList;
