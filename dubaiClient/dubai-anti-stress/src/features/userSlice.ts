
import { createSlice, type PayloadAction } from '@reduxjs/toolkit'

export interface User {
  id: string
  email: string
  phone: string
  name: string
  userType: 'seller' | 'buyer' | 'investor'
  isVerified: boolean
  subscriptionPlan: 'free' | 'premium' | 'pro_seller'
  subscriptionExpiry: string | null
  createdAt: string
}

interface UserState {
  user: User | null
  isAuthenticated: boolean
  loading: boolean
  error: string | null
}

const initialState: UserState = {
  user: null,
  isAuthenticated: false,
  loading: false,
  error: null,
}

export const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {
    setUser: (state, action: PayloadAction<User>) => {
      state.user = action.payload
      state.isAuthenticated = true
      state.loading = false
      state.error = null
    },
    clearUser: (state) => {
      state.user = null
      state.isAuthenticated = false
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload
    },
    setError: (state, action: PayloadAction<string>) => {
      state.error = action.payload
      state.loading = false
    },
    updateUser: (state, action: PayloadAction<Partial<User>>) => {
      if (state.user) {
        state.user = { ...state.user, ...action.payload }
      }
    },
  },
})

export const {
  setUser,
  clearUser,
  setLoading,
  setError,
  updateUser,
} = userSlice.actions

export default userSlice.reducer