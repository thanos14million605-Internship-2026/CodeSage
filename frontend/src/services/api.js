import axios from "axios";
import toast from "react-hot-toast";

const isProduction = true;
const API_BASE_URL =
  isProduction === true
    ? "https://codesage-h1pb.onrender.com/api"
    : "http://localhost:5000/api";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("token");
      window.location.href = "/login";
      toast.error("Session expired. Please login again.");
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: (credentials) => api.post("/auth/login", credentials),
  signup: (userData) => api.post("/auth/signup", userData),
  getProfile: () => api.get("/auth/profile"),
};

// Analysis API
export const analysisAPI = {
  analyze: (data) => api.post("/analysis", data),
};

// History API
export const historyAPI = {
  getHistory: (params) => api.get("/history", { params }),
  getHistoryById: (id) => api.get(`/history/${id}`),
  deleteHistory: (id) => api.delete(`/history/${id}`),
};

export default api;
