import axios from "axios";

const API_URL = process.env.REACT_APP_API_URL;

const api = axios.create({baseURL: API_URL});

// 请求拦截器，增加认证令牌
api.interceptors.request.use(
    function (config) {
        const token = localStorage.getItem("token");
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);
// 响应拦截器，处理认证错误
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response && error.response.status === 401) {
            localStorage.removeItem("token");
            localStorage.removeItem("user");
            window.location.href = "/login";
        }
        return Promise.reject(error);
    }
);
export default api;
