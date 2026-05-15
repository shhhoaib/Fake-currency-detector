import { create } from "zustand"

interface AuthState {
  user: null
  token: null
  loading: boolean
  login: (username: string, password: string) => Promise<void>
  register: (email: string, username: string, password: string) => Promise<void>
  logout: () => void
  loadUser: () => Promise<void>
  isAuthenticated: () => boolean
}

export const useAuthStore = create<AuthState>(() => ({
  user: null,
  token: null,
  loading: false,
  login: async () => {},
  register: async () => {},
  logout: () => {},
  loadUser: async () => {},
  isAuthenticated: () => true,
}))
