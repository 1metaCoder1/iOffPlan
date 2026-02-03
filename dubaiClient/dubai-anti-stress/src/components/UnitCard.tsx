import type { Unit } from '../types/unit'

function formatAed(value?: number) {
  if (value == null || Number.isNaN(value)) return '—'
  return new Intl.NumberFormat('en-AE', {
    style: 'currency',
    currency: 'AED',
    maximumFractionDigits: 0,
  }).format(value)
}

function formatArea(value?: number) {
  if (value == null || Number.isNaN(value)) return '—'
  return `${value.toLocaleString()} sqm`
}

function getRoomsLabel(unit: Unit) {
  if (unit.rooms_en) return unit.rooms_en
  if (unit.rooms == null) return '—'
  if (unit.rooms === 0) return 'Studio'
  if (unit.rooms === 1) return '1 Bed'
  return `${unit.rooms} Beds`
}

export type UnitCardProps = {
  unit: Unit
  active?: boolean
  onSelect?: (unit: Unit) => void
}

export function UnitCard({ unit, active, onSelect }: UnitCardProps) {
  return (
    <button
      type="button"
      onClick={() => onSelect?.(unit)}
      className={[
        'card w-full text-left overflow-hidden group',
        'transition-all duration-300',
        active ? 'ring-2 ring-bayut-primary' : 'hover:shadow-card-hover',
      ].join(' ')}
    >
      <div className="relative h-40 overflow-hidden bg-gray-100">
        {unit.cover_image_url ? (
          <img
            src={unit.cover_image_url}
            alt={unit.unit_number ? `Unit ${unit.unit_number}` : `Unit ${unit.property_id}`}
            className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
            loading="lazy"
          />
        ) : (
          <div className="w-full h-full bg-gradient-to-r from-blue-50 to-orange-50" />
        )}
        <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />

        <div className="absolute top-3 left-3 flex flex-wrap gap-2">
          <span className="badge badge-primary">
            {unit.area_name_en || 'Area'}
          </span>
          {unit.is_free_hold ? <span className="badge badge-success">Freehold</span> : null}
          {unit.is_lease_hold ? <span className="badge badge-warning">Leasehold</span> : null}
        </div>

        <div className="absolute bottom-3 left-3 right-3 flex items-end justify-between gap-3">
          <div className="min-w-0">
            <div className="text-white font-bold text-lg leading-tight truncate">
              {unit.unit_number ? `Unit ${unit.unit_number}` : `Unit #${unit.property_id}`}
            </div>
            <div className="text-blue-100 text-sm truncate">
              {unit.project_name_en || unit.master_project_en || unit.building_number || '—'}
            </div>
          </div>
          <div className="text-right">
            <div className="text-white font-bold">{formatAed(unit.price_aed)}</div>
            <div className="text-blue-100 text-xs">{formatArea(unit.actual_area)}</div>
          </div>
        </div>
      </div>

      <div className="p-4">
        <div className="grid grid-cols-3 gap-3">
          <div className="text-center">
            <div className="font-bold text-bayut-dark">{getRoomsLabel(unit)}</div>
            <div className="text-xs text-bayut-gray">Rooms</div>
          </div>
          <div className="text-center">
            <div className="font-bold text-bayut-dark">{unit.floor ?? '—'}</div>
            <div className="text-xs text-bayut-gray">Floor</div>
          </div>
          <div className="text-center">
            <div className="font-bold text-bayut-dark truncate">
              {unit.developer_name ?? '—'}
            </div>
            <div className="text-xs text-bayut-gray">Developer</div>
          </div>
        </div>
      </div>
    </button>
  )
}

