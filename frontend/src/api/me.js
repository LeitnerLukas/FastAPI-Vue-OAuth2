import request from './req';

export const apiGetMyself = () => request('GET', '/api/me');
export const apiUpdatePass = (data) => request('PUT', '/api/me/password', data);
export const apiUpdateBirth = (data) =>
  request('PUT', '/api/me/birthday', data);
export const apiDelateAccount = () => request('DELETE', '/api/me');
