import request from './req';
import axios from 'axios';

export const apiGetActivities = (token) => request('GET', `/activities?token=${token}`);
export const apiGetActivity = (activityId, token) =>
  request('GET', `/activities/${activityId}?token=${token}`);
export const createActivity = (activity, token) =>
  request('POST', `/activities?token=${token}`, activity);
export const updateActivity = (activity) =>
  request('PUT', `/activities/${activity.id}`, activity);
export const approveActivity = (activityId, token) =>
  request('POST', `/approve/activities/${activityId}/approve?token=${token}`);
export const superapproveActivity = (activityId, token) =>
  request('POST', `/approve/activities/${activityId}/super_approve?token=${token}`);
