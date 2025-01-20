import request from "./req";
import axios from "axios";

export const apiGetRolesList = () => axios.get("/roles");
