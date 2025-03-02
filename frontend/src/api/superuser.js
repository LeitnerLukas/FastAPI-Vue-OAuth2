import axios from "axios";

export const deleteUser = (id) => axios.post(`/user/${id}`);