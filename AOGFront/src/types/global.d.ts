import { PropsWithChildren } from "react";

type Item = {
    id: number;
    name: string;
    date_purchased: string;
    model: string;
    cost: number;
    serials: string;
    created: string;
    updated: string;
};

type ProtectedRouteProps = PropsWithChildren

interface ItemProp {
    item: Item;
}

interface ItemProps {
    items: Item[];
}

type User = {
    id: number;
    username: string;
    get_full_name: string;
    email: string;
    is_staff: boolean;
}

interface UserProp {
    user: User
}

interface UserProps {
    users: User[]
}

interface AuthContextProps {
    token: string | null;
    setToken: (token: string | null) => void;
  }

// Define the interface for the hook properties
interface LocalStorageProps<T> {
    keyName: string;
    defaultValue: T;
}
  
  // Define the interface for the hook return value setter function
interface SetValueProps<T> {
    newValue: T;
}