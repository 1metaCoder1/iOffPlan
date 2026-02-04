export interface ListingFormData {
  // --- Basic Information ---
  property_type_id: number
  property_type_en: string
  property_sub_type_id: number
  property_sub_type_en: string
  
  // --- Location Information ---
  area_id: number
  area_name_en: string
  land_number?: string
  land_sub_number?: number
  building_number?: string
  unit_number?: string
  
  // --- Property Details ---
  actual_area: number
  unit_balcony_area?: number
  rooms: number
  rooms_en: string
  floor?: string
  
  // --- Project Information ---
  project_id?: number
  project_name_en?: string
  master_project_id?: number
  master_project_en?: string
  
  // --- Ownership Information ---
  is_free_hold: number
  is_lease_hold: number
  is_registered: number
  
  // --- Land Information ---
  land_type_id: number
  land_type_en: string
  
  // --- Contact Information ---
  developer_name?: string
  contact_person?: string
  contact_phone?: string
  contact_email?: string
  
  // --- Description ---
  description: string
  
  // --- Pricing ---
  asking_price?: number
  price_per_sqm?: number
  
  // --- Additional Features ---
  parking_allocation_type?: number
  parking_allocation_type_en?: string
  unit_parking_number?: string
  
  // --- Images ---
  images: File[]
  
  // --- Status ---
  listing_status: 'draft' | 'active' | 'pending' | 'rejected'
}

export interface AreaOption {
  area_id: number
  area_name_en: string
  area_name_ar?: string
}

export interface PropertyTypeOption {
  property_type_id: number
  property_type_en: string
  property_type_ar?: string
}

export interface PropertySubTypeOption {
  property_sub_type_id: number
  property_sub_type_en: string
  property_sub_type_ar?: string
}

export interface LandTypeOption {
  land_type_id: number
  land_type_en: string
  land_type_ar?: string
}

export interface ProjectOption {
  project_id: number
  project_name_en: string
  project_name_ar?: string
  master_project_id?: number
  master_project_en?: string
}