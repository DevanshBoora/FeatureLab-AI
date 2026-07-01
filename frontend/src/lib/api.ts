import axios from "axios";

// Hardcoded workspace for this demo to avoid Auth complexity
export const DEFAULT_WORKSPACE_ID = "00000000-0000-0000-0000-000000000001";

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1",
});

export const workspaceApi = {
  get: (id: string) => api.get(`/workspaces/${id}`).then(res => res.data),
  create: (name: string) => api.post(`/workspaces`, { name }).then(res => res.data),
};

export const datasetApi = {
  upload: async (workspaceId: string, name: string, file: File, description?: string) => {
    const formData = new FormData();
    formData.append("workspace_id", workspaceId);
    formData.append("name", name);
    if (description) formData.append("description", description);
    formData.append("file", file);
    
    return api.post(`/datasets`, formData, {
      headers: { "Content-Type": "multipart/form-data" }
    }).then(res => res.data);
  },
  list: (workspaceId: string) => api.get(`/datasets/workspace/${workspaceId}`).then(res => res.data),
  get: (id: string) => api.get(`/datasets/${id}`).then(res => res.data),
};

export const jobApi = {
  submit: (workspaceId: string, datasetId: string, taskType: string, config: any) => {
    return api.post(`/jobs`, {
      workspace_id: workspaceId,
      dataset_id: datasetId,
      task_type: taskType,
      configuration: config
    }).then(res => res.data);
  },
  get: (id: string) => api.get(`/jobs/${id}`).then(res => res.data),
  list: (workspaceId: string) => api.get(`/jobs/workspace/${workspaceId}`).then(res => res.data),
};

export default api;
