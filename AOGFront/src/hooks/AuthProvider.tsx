import React, { createContext, useContext, useEffect, useLayoutEffect, ReactNode } from "react";
import { useLocalStorage } from "./useLocalStorage";
import api from "../utils/api";

interface AuthContextProps {
  token: string | null;
  setToken: (newValue: string | null) => void;
}

const AuthContext = createContext<AuthContextProps | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [token, setToken] = useLocalStorage<string | null>({
    keyName: 'token',
    defaultValue: null,
  });


  useEffect(() => {
    const fetchToken = async () => {
      try {
        const response = await api.post('auth/token', {
          clientId: "your-client-id",
          clientSecret: "your-client-secret",
          grantType: "client_credentials",
          scope: "your-scope"
        });
        setToken(response.data.access);
      } catch (error) {
        setToken(null);
        console.error("Error fetching token:", error);
      }
    };

    if (!token) {
      fetchToken();
    }
  }, [token, setToken]);

  useLayoutEffect(() => {
    const authInterceptor = api.interceptors.request.use((config) => {
      if (token && !config._retry) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      console.log('from config', token)
      return config;
    });

    return () => {
      api.interceptors.request.eject(authInterceptor);
    };
  }, [token]);

  useLayoutEffect(() => {
    const refreshInterceptor = api.interceptors.response.use(
      (response) => response,
      async (error) => {
        const originalRequest = error.config;

        if (error.response?.status === 403 && error.response?.data?.message === 'Unauthorized') {
          try {
            const response = await api.post('auth/token/refresh', {
              token
            });

            console.log('sample token', response.data.access)
            setToken(response.data.access);

            originalRequest.headers.Authorization = `Bearer ${response.data.access}`;
            originalRequest._retry = true;

            return api(originalRequest);
          } catch (refreshError) {
            setToken(null);
            console.error("Error refreshing token:", refreshError);
          }
        }

        return Promise.reject(error);
      }
    );

    return () => {
      api.interceptors.response.eject(refreshInterceptor);
    };
  }, [token, setToken]);

  return (
    <AuthContext.Provider value={{ token, setToken }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const authContext = useContext(AuthContext);

  if (!authContext) {
    throw new Error('useAuth must be used within an AuthProvider');
  }

  return authContext;
};
