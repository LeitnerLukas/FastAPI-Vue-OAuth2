import request from './req';
import axios from 'axios';

export const apiGetActivities = () => request('GET', '/activities');
export const apiGetActivity = (activityId) =>
  request('GET', `/activities/${activityId}`);
export const createActivity = (activity) =>
  request('POST', '/activities', activity);
export const updateActivity = (activity) =>
  request('PUT', `/activities/${activity.id}`, activity);
