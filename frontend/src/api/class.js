import request from './req';
import axios from 'axios';

export const getClasses = (token) => request('GET', `/classes?token=${token}`);
export const createClass = (data, token) => request('POST', `/classes?token=${token}`, data);
export const updateClass = (classId, data, token) => request("PUT", `/classes/${classId}?token=${token}`, data);
export const deleteClass = (id, token) => request("DELETE", `/classes/${id}?token=${token}`);