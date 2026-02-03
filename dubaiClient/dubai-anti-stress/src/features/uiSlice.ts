import { createSlice, type PayloadAction } from '@reduxjs/toolkit'

interface UIState {
  sidebarOpen: boolean
  modalOpen: boolean
  modalContent: string | null
  toastMessage: string | null
  toastType: 'success' | 'error' | 'info' | null
}

const initialState: UIState = {
  sidebarOpen: false,
  modalOpen: false,
  modalContent: null,
  toastMessage: null,
  toastType: null,
}

export const uiSlice = createSlice({
  name: 'ui',
  initialState,
  reducers: {
    toggleSidebar: (state) => {
      state.sidebarOpen = !state.sidebarOpen
    },
    openModal: (state, action: PayloadAction<string>) => {
      state.modalOpen = true
      state.modalContent = action.payload
    },
    closeModal: (state) => {
      state.modalOpen = false
      state.modalContent = null
    },
    showToast: (state, action: PayloadAction<{ message: string; type: 'success' | 'error' | 'info' }>) => {
      state.toastMessage = action.payload.message
      state.toastType = action.payload.type
    },
    hideToast: (state) => {
      state.toastMessage = null
      state.toastType = null
    },
  },
})

export const {
  toggleSidebar,
  openModal,
  closeModal,
  showToast,
  hideToast,
} = uiSlice.actions

export default uiSlice.reducer