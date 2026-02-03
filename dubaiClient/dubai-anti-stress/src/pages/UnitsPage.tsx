import { useMemo, useState } from 'react'
import { UnitCard } from '../components/UnitCard'
import type { Unit } from '../types/unit'

const MOCK_UNITS: Unit[] = [
  {
    property_id: 101001,
    area_id: 1,
    area_name_en: 'Downtown Dubai',
    unit_number: '1208',
    building_number: 'BLD-12',
    floor: '12',
    rooms: 2,
    rooms_en: '2 Beds',
    actual_area: 118,
    unit_balcony_area: 12,
    is_free_hold: 1,
    project_id: 2001,
    project_name_en: 'Burj Views',
    master_project_en: 'Emaar Downtown',
    developer_name: 'Emaar',
    price_aed: 1850000,
    cover_image_url:
      'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?ixlib=rb-4.0.3&auto=format&fit=crop&w=1400&q=80',
  },
  {
    property_id: 101002,
    area_id: 2,
    area_name_en: 'Business Bay',
    unit_number: '2203',
    building_number: 'BLD-22',
    floor: '22',
    rooms: 0,
    rooms_en: 'Studio',
    actual_area: 46,
    is_free_hold: 1,
    project_id: 2002,
    project_name_en: 'The Bay Gate',
    master_project_en: 'Business Bay District',
    developer_name: 'Select Group',
    price_aed: 820000,
    cover_image_url:
      'https://images.unsplash.com/photo-1497366754035-f200968a6e72?ixlib=rb-4.0.3&auto=format&fit=crop&w=1400&q=80',
  },
  {
    property_id: 101003,
    area_id: 3,
    area_name_en: 'Jumeirah Village Circle',
    unit_number: '0811',
    building_number: 'BLD-08',
    floor: '8',
    rooms: 1,
    rooms_en: '1 Bed',
    actual_area: 73,
    unit_balcony_area: 9,
    is_free_hold: 1,
    project_id: 2003,
    project_name_en: 'Bloom Towers',
    developer_name: 'DIFC Developments',
    price_aed: 920000,
    cover_image_url:
      'https://images.unsplash.com/photo-1505691938895-1758d7feb511?ixlib=rb-4.0.3&auto=format&fit=crop&w=1400&q=80',
  },
  {
    property_id: 101004,
    area_id: 4,
    area_name_en: 'Dubai Marina',
    unit_number: '5401',
    building_number: 'BLD-54',
    floor: '54',
    rooms: 3,
    rooms_en: '3 Beds',
    actual_area: 172,
    unit_balcony_area: 18,
    is_free_hold: 1,
    project_id: 2004,
    project_name_en: 'Marina Gate',
    developer_name: 'Select Group',
    price_aed: 3650000,
    cover_image_url:
      'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=1400&q=80',
  },
  {
    property_id: 101005,
    area_id: 5,
    area_name_en: 'Al Satwa',
    unit_number: 'V-07',
    building_number: 'VIL-01',
    floor: 'G',
    rooms: 4,
    rooms_en: '4 Beds',
    actual_area: 312,
    is_lease_hold: 1,
    project_id: 2005,
    project_name_en: 'Satwa Villas',
    developer_name: 'Meraas',
    price_aed: 3100000,
    cover_image_url:
      'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?ixlib=rb-4.0.3&auto=format&fit=crop&w=1400&q=80',
  },
]

function formatAed(value?: number) {
  if (value == null || Number.isNaN(value)) return '—'
  return new Intl.NumberFormat('en-AE', {
    style: 'currency',
    currency: 'AED',
    maximumFractionDigits: 0,
  }).format(value)
}

export default function UnitsPage() {
  const [selectedUnitId, setSelectedUnitId] = useState<number | null>(MOCK_UNITS[0]?.property_id ?? null)

  const [area, setArea] = useState<string>('all')
  const [developer, setDeveloper] = useState<string>('all')
  const [minPrice, setMinPrice] = useState<string>('')
  const [maxPrice, setMaxPrice] = useState<string>('')

  const areas = useMemo(() => {
    const unique = Array.from(new Set(MOCK_UNITS.map(u => u.area_name_en).filter(Boolean)))
    unique.sort((a, b) => a.localeCompare(b))
    return unique
  }, [])

  const developers = useMemo(() => {
    const unique = Array.from(new Set(MOCK_UNITS.map(u => u.developer_name).filter(Boolean))) as string[]
    unique.sort((a, b) => a.localeCompare(b))
    return unique
  }, [])

  const filteredUnits = useMemo(() => {
    const min = minPrice.trim() ? Number(minPrice) : null
    const max = maxPrice.trim() ? Number(maxPrice) : null

    return MOCK_UNITS.filter((u) => {
      if (area !== 'all' && u.area_name_en !== area) return false
      if (developer !== 'all' && u.developer_name !== developer) return false

      const price = u.price_aed ?? null
      if (min != null && !Number.isNaN(min)) {
        if (price == null || price < min) return false
      }
      if (max != null && !Number.isNaN(max)) {
        if (price == null || price > max) return false
      }

      return true
    })
  }, [area, developer, minPrice, maxPrice])

  const selectedUnit = useMemo(() => {
    if (selectedUnitId == null) return null
    return MOCK_UNITS.find(u => u.property_id === selectedUnitId) ?? null
  }, [selectedUnitId])

  const clearFilters = () => {
    setArea('all')
    setDeveloper('all')
    setMinPrice('')
    setMaxPrice('')
  }

  return (
    <div className="py-10">
      <div className="container">
        <div className="mb-8">
          <div className="inline-block bg-blue-50 px-4 py-1 rounded-full mb-4">
            <span className="text-bayut-primary font-medium">Objects / Units</span>
          </div>
          <h2 className="section-title">Units directory</h2>
          <p className="section-subtitle">
            Моки под будущий API. Выбирай объект слева — детали откроются справа.
          </p>
        </div>

        <div className="card p-6 mb-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div>
              <label className="block text-sm font-medium text-bayut-dark mb-2">Area</label>
              <select className="form-control" value={area} onChange={(e) => setArea(e.target.value)}>
                <option value="all">All areas</option>
                {areas.map(a => (
                  <option key={a} value={a}>{a}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-bayut-dark mb-2">Developer</label>
              <select className="form-control" value={developer} onChange={(e) => setDeveloper(e.target.value)}>
                <option value="all">All developers</option>
                {developers.map(d => (
                  <option key={d} value={d}>{d}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-bayut-dark mb-2">Min price (AED)</label>
              <input
                className="form-control"
                inputMode="numeric"
                placeholder="e.g. 800000"
                value={minPrice}
                onChange={(e) => setMinPrice(e.target.value)}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-bayut-dark mb-2">Max price (AED)</label>
              <input
                className="form-control"
                inputMode="numeric"
                placeholder="e.g. 2500000"
                value={maxPrice}
                onChange={(e) => setMaxPrice(e.target.value)}
              />
            </div>
          </div>

          <div className="mt-4 flex flex-col sm:flex-row gap-3 sm:items-center sm:justify-between">
            <div className="text-sm text-bayut-gray">
              Showing <span className="font-bold text-bayut-dark">{filteredUnits.length}</span> units
            </div>
            <div className="flex gap-3">
              <button type="button" className="btn btn-outline" onClick={clearFilters}>
                Clear filters
              </button>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {filteredUnits.map((u) => (
                <UnitCard
                  key={u.property_id}
                  unit={u}
                  active={u.property_id === selectedUnitId}
                  onSelect={(unit) => setSelectedUnitId(unit.property_id)}
                />
              ))}
            </div>
            {filteredUnits.length === 0 ? (
              <div className="mt-6 bg-yellow-50 text-yellow-900 p-4 rounded-xl border border-yellow-200">
                Ничего не найдено по выбранным фильтрам.
              </div>
            ) : null}
          </div>

          <aside className="lg:col-span-1">
            <div className="card p-6 sticky top-6">
              <div className="flex items-start justify-between gap-3 mb-4">
                <div className="min-w-0">
                  <div className="text-sm text-bayut-gray">Selected unit</div>
                  <div className="text-xl font-bold text-bayut-dark truncate">
                    {selectedUnit?.unit_number ? `Unit ${selectedUnit.unit_number}` : selectedUnit ? `Unit #${selectedUnit.property_id}` : '—'}
                  </div>
                </div>
              </div>

              {selectedUnit ? (
                <div className="space-y-4">
                  <div className="grid grid-cols-2 gap-3">
                    <div className="bg-bayut-light rounded-xl p-3">
                      <div className="text-xs text-bayut-gray">Price</div>
                      <div className="font-bold text-bayut-dark">{formatAed(selectedUnit.price_aed)}</div>
                    </div>
                    <div className="bg-bayut-light rounded-xl p-3">
                      <div className="text-xs text-bayut-gray">Area</div>
                      <div className="font-bold text-bayut-dark">{selectedUnit.actual_area ?? '—'} sqm</div>
                    </div>
                    <div className="bg-bayut-light rounded-xl p-3">
                      <div className="text-xs text-bayut-gray">Rooms</div>
                      <div className="font-bold text-bayut-dark">{selectedUnit.rooms_en ?? selectedUnit.rooms ?? '—'}</div>
                    </div>
                    <div className="bg-bayut-light rounded-xl p-3">
                      <div className="text-xs text-bayut-gray">Floor</div>
                      <div className="font-bold text-bayut-dark">{selectedUnit.floor ?? '—'}</div>
                    </div>
                  </div>

                  <div>
                    <div className="text-sm font-medium text-bayut-dark mb-2">Location</div>
                    <div className="text-bayut-gray">
                      {selectedUnit.area_name_en}
                      {selectedUnit.project_name_en ? ` · ${selectedUnit.project_name_en}` : ''}
                    </div>
                  </div>

                  <div>
                    <div className="text-sm font-medium text-bayut-dark mb-2">Developer</div>
                    <div className="text-bayut-gray">{selectedUnit.developer_name ?? '—'}</div>
                  </div>

                  <div className="flex flex-wrap gap-2">
                    {selectedUnit.is_free_hold ? <span className="badge badge-success">Freehold</span> : null}
                    {selectedUnit.is_lease_hold ? <span className="badge badge-warning">Leasehold</span> : null}
                    <span className="badge badge-primary">Area ID: {selectedUnit.area_id}</span>
                  </div>

                  <button type="button" className="btn btn-primary w-full">
                    Open unit details (next step)
                  </button>
                  <div className="text-xs text-bayut-gray">
                    Дальше сюда можно добавить просмотр всех полей UNITS и связанные таблицы (Projects/Buildings/Transactions).
                  </div>
                </div>
              ) : (
                <div className="text-bayut-gray">Выбери юнит из списка.</div>
              )}
            </div>
          </aside>
        </div>
      </div>
    </div>
  )
}

