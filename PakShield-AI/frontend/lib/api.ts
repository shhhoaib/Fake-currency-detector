import axios from "axios"

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

const api = axios.create({
  baseURL: API_URL,
  headers: { "Content-Type": "application/json" },
})

export const detectAPI = {
  upload: (file: File) => {
    const form = new FormData()
    form.append("file", file)
    return api.post("/api/detect", form, {
      headers: { "Content-Type": "multipart/form-data" },
    })
  },
  variants: (file: File) => {
    const form = new FormData()
    form.append("file", file)
    return api.post("/api/detect/variants", form, {
      headers: { "Content-Type": "multipart/form-data" },
      timeout: 30000,
    })
  },
}

export const chatAPI = {
  send: (message: string) => api.post("/api/chat", { message }),
  history: () => api.get("/api/chat/history"),
}

export const historyAPI = {
  get: (page = 1, pageSize = 10) =>
    api.get(`/api/history?page=${page}&page_size=${pageSize}`),
}

export const currencyAPI = {
  timeline: () => api.get("/api/currency/timeline"),
  denominations: () => api.get("/api/currency/denominations"),
  rates: () => api.get("/api/currency/rates"),
}

export default api
