import request from "./req";
import axios from "axios";

export const getClasses = () => request('GET', '/classes');
export const createClass = (data) => request('POST', '/classes', data);
export const updateClass = (classId, data) => request("PUT", `/classes/${classId}`, data);
export const deleteClass = (id) => request("DELETE", `/classes/${id}`);