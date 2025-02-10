import request from './req';
import axios from 'axios';

export const getClasses = () => request('GET', '/classes/classes');
export const createClass = (data) => request('POST', '/classes/classes', data);
export const updateClass = (id, data) => request('PUT', `/classes/${id}`, data);
export const deleteClass = (id) => request('DELETE', `/classes/classes/${id}`);
