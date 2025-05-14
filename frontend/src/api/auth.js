import api from './index';

export const login = (credentials) => {
    return api.post('/auth/login/', credentials);
};


export const register = (userData) => {
    return api.post('/auth/register/', userData)
};

export const getCurrentUser = () => {
    return api.post('/auth/me/');
};
