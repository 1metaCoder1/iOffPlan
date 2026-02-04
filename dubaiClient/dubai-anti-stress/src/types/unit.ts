export type UnitId = number

// Enhanced Unit interface matching backend UNITS table structure
export interface Unit {
  // --- Primary Keys ---
  property_id: UnitId
  
  // --- Area Information ---
  area_id: number
  area_name_en: string
  area_name_ar?: string
  
  // --- Location Details ---
  land_number?: string
  land_sub_number?: number
  building_number?: string
  unit_number?: string
  
  // --- Area Measurements ---
  unit_balcony_area?: number
  unit_parking_number?: string
  parking_allocation_type?: number
  parking_allocation_type_ar?: string
  parking_allocation_type_en?: string
  common_area?: number
  actual_common_area?: number
  actual_area?: number
  
  // --- Unit Details ---
  floor?: string
  rooms?: number
  rooms_en?: string
  rooms_ar?: string
  
  // --- Property Type ---
  property_type_id?: number
  property_type_ar?: string
  property_type_en?: string
  property_sub_type_id?: number
  property_sub_type_ar?: string
  property_sub_type_en?: string
  
  // --- Hierarchy ---
  parent_property_id?: number
  grandparent_property_id?: number
  creation_date?: string
  
  // --- Municipality Info ---
  munc_zip_code?: string
  munc_number?: string
  parcel_id?: number
  
  // --- Property Status ---
  is_free_hold?: number
  is_lease_hold?: number
  is_registered?: number
  
  // --- Registration ---
  pre_registration_number?: string
  
  // --- Project Information ---
  master_project_id?: number
  master_project_en?: string
  master_project_ar?: string
  project_id?: number
  project_name_ar?: string
  project_name_en?: string
  
  // --- Land Type ---
  land_type_id?: number
  land_type_ar?: string
  land_type_en?: string

  // --- UI / mocks ---
  developer_name?: string
  price_aed?: number
  cover_image_url?: string
}

