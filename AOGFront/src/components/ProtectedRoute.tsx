import { useNavigate, useLocation } from "react-router-dom";
import { useAuth } from "../hooks/AuthProvider";
import { ProtectedRouteProps } from "../types/global";
import { useEffect } from "react";

function ProtectedRoute({ children }: ProtectedRouteProps) {
  const { token } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    if (token === null) {
      navigate('/login', { state: { from: location } });
    }
  }, [navigate, token, location]);

  return token ? children : null;
}

export default ProtectedRoute;
