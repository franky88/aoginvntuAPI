import { useState, ChangeEvent, FormEvent } from "react";
import { useAuth } from "../../hooks/AuthProvider";
import { useNavigate, useLocation } from "react-router-dom";
import api from "../../utils/api";

interface LoginResponse {
  message?: string;
  access?: string;
  refresh?: string;
  error?: string;
}

function Login() {
  const [username, setUsername] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [error, setError] = useState<string>('');
  const { setToken } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const handleUsernameChange = (e: ChangeEvent<HTMLInputElement>) => {
    setUsername(e.target.value);
  };

  const handlePasswordChange = (e: ChangeEvent<HTMLInputElement>) => {
    setPassword(e.target.value);
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    try {
      const response = await api.post<LoginResponse>('auth/token', {
        username,
        password,
      });
      if (response.data.access && response.data.refresh) {
        setToken(response.data.access); // set the access token
        sessionStorage.setItem('refreshToken', response.data.refresh); // set the refresh token in session storage
        const redirectPath = location.state?.from?.pathname || '/'; // Navigate to the original page or home if undefined
        navigate(redirectPath);
      } else {
        setError(response.data.error || 'Unknown error');
      }
    } catch (error) {
      setError('Invalid username or password');
      console.error('There was an error!', error);
    }
  };

  return (
    <div className="flex flex-col mt-20">
      <h2 className="text-3xl mx-auto mb-10">Login</h2>
      <form onSubmit={handleSubmit} className="space-y-4 font-[sans-serif] max-w-md mx-auto">
        <input
          type="text" 
          placeholder="Username"
          className="px-4 py-3 bg-gray-100 w-full text-sm outline-none border-b-2 border-blue-500 rounded"
          value={username}
          onChange={handleUsernameChange}
          required
        />

        <input
          type="password"
          placeholder="Enter Password"
          className="px-4 py-3 bg-gray-100 w-full text-sm outline-none border-b-2 border-transparent focus:border-blue-500 rounded"
          value={password}
          onChange={handlePasswordChange}
          required
        />

        <div className="flex">
          <input type="checkbox" className="w-4" />
          <label className="text-sm ml-4">Remember me</label>
        </div>
        {error && <p className="error">{error}</p>}
        <button type="submit"
          className="!mt-8 w-full px-4 py-2.5 mx-auto block text-sm bg-blue-500 text-white rounded hover:bg-blue-600">Submit</button>
      </form>
    </div>
  );
}

export default Login;
