import { configureStore } from '@reduxjs/toolkit'
import { propertySlice } from './features/propertySlice'
import { userSlice } from './features/userSlice'
import { uiSlice } from './features/uiSlice'

export const store = configureStore({
  reducer: {
    properties: propertySlice.reducer,
    user: userSlice.reducer,
    ui: uiSlice.reducer,
  },
})

// Infer the `RootState` and `AppDispatch` types from the store itself
export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch