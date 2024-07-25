import { useState } from "react";

interface LocalStorageProp<T> {
  keyName: string;
  defaultValue: T;
}

export const useLocalStorage = <T,>({ keyName, defaultValue }: LocalStorageProp<T>) => {
  const [storedValue, setStoredValue] = useState<T>(() => {
    const value = window.localStorage.getItem(keyName);
    return value ? JSON.parse(value) as T : defaultValue;
  });

  const setValue = (newValue: T) => {
    window.localStorage.setItem(keyName, JSON.stringify(newValue));
    setStoredValue(newValue);
  };

  return [storedValue, setValue] as const;
};
