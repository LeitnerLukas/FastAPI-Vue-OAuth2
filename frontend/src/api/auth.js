import axios from 'axios';
import qs from 'qs';

export const apiLogin = (form) =>
  axios.post('/api//login', qs.stringify(form), {
    headers: { 'content-type': 'application/x-www-form-urlencoded' },
  });
export const apiRefresh = () => axios.post('/api/auth/refresh');
export const apiLogout = () => axios.post('api//auth/logout');
