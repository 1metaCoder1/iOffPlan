import { createSlice, type PayloadAction } from '@reduxjs/toolkit'

export interface Property {
  id: string
  title: string
  description: string
  propertyType: 'apartment' | 'villa' | 'townhouse' | 'office' | 'shop'
  location: string
  area: number // in sqm
  bedrooms: number
  bathrooms: number
  price: number
  amenities: string[]
  images: string[]
  sellerId: string
  isVerified: boolean
  createdAt: string
  noBrokerReason: string
}

interface PropertyState {
  properties: Property[]
  loading: boolean
  error: string | null
  filters: {
    minPrice: number | null
    maxPrice: number | null
    propertyType: string | null
    location: string | null
    bedrooms: number | null
    bathrooms: number | null
    noBrokerOnly: boolean
  }
}

const initialState: PropertyState = {
  properties: [],
  loading: false,
  error: null,
  filters: {
    minPrice: null,
    maxPrice: null,
    propertyType: null,
    location: null,
    bedrooms: null,
    bathrooms: null,
    noBrokerOnly: true,
  },
}

export const propertySlice = createSlice({
  name: 'properties',
  initialState,
  reducers: {
    setProperties: (state, action: PayloadAction<Property[]>) => {
      state.properties = action.payload
      state.loading = false
      state.error = null
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload
    },
    setError: (state, action: PayloadAction<string>) => {
      state.error = action.payload
      state.loading = false
    },
    setFilters: (state, action: PayloadAction<Partial<PropertyState['filters']>>) => {
      state.filters = { ...state.filters, ...action.payload }
    },
    addProperty: (state, action: PayloadAction<Property>) => {
      state.properties.unshift(action.payload)
    },
    updateProperty: (state, action: PayloadAction<Property>) => {
      const index = state.properties.findIndex(p => p.id === action.payload.id)
      if (index !== -1) {
        state.properties[index] = action.payload
      }
    },
    deleteProperty: (state, action: PayloadAction<string>) => {
      state.properties = state.properties.filter(p => p.id !== action.payload)
    },
  },
})

export const {
  setProperties,
  setLoading,
  setError,
  setFilters,
  addProperty,
  updateProperty,
  deleteProperty,
} = propertySlice.actions

export default propertySlice.reducer