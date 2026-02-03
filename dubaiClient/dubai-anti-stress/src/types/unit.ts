export type UnitId = number

// Базовая форма под будущий API (таблица UNITS) + UI-поля для моков.
export interface Unit {
  // --- UNITS (backend) ---
  property_id: UnitId
  area_id: number
  area_name_en: string
  area_name_ar?: string

  unit_number?: string
  building_number?: string
  floor?: string
  rooms?: number
  rooms_en?: string
  rooms_ar?: string

  actual_area?: number
  unit_balcony_area?: number
  is_free_hold?: number
  is_lease_hold?: number

  project_id?: number
  project_name_en?: string
  project_name_ar?: string
  master_project_en?: string
  master_project_ar?: string

  // --- UI / mocks ---
  developer_name?: string
  price_aed?: number
  cover_image_url?: string
}

