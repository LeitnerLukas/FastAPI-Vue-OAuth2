import request from './req';
import axios from 'axios';

export const apiGetActivities = () => request('GET', `/activities?${token}`);
export const apiGetActivity = (activityId, token) =>
  request('GET', `/activities/${activityId}?token=${token}`);
export const createActivity = (activity, token) =>
  request('POST', `/activities?token=${token}`, activity);
export const updateActivity = (activity) =>
  request('PUT', `/activities/${activity.id}`, activity);
